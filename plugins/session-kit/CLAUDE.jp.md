<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# session-kit プラグイン開発ガイド

session-kit は Claude Code のセッションごとに **コンテキスト世代マーカー** を 1 つ維持し、
`/compact` や `/clear` でコンテキストがリセットされたことを他プラグインが検知して、
消えた内容を再注入できるようにする。

---

## 何をするか

| フック | 動作 |
|---|---|
| `PreCompact` | マーカーを touch（compact 直前にコンテキストが落ちる） |
| `SessionStart`（source=`clear`） | マーカーを touch（`/clear` でコンテキストが消えた） |

それ以外は **何もしない** — プロンプト注入もブロックも出力もなし。フックはマーカーの
mtime を更新するだけ。

`startup` と `resume` はあえて touch しない:
- `startup`: 新規セッションは `session_id` が新しく、無効化すべき古いトークンが無い。
- `resume`: 会話が復元されるため、注入済み内容もコンテキストに戻る。

---

## マーカー規約（他プラグインとの共有契約）

| | 値 |
|---|---|
| パス | `/tmp/claude-session-ctx-gen-{session_id}`（`tempfile.gettempdir()` 経由） |
| 意味 | mtime = このセッションで最後にコンテキストがリセットされた時刻（compact / clear） |
| 生成側 | session-kit（`hooks/ctx_marker.py`） |
| 利用側 | 「1 セッション 1 回」注入トークンを持つプラグイン — 例: py-kit / next-kit の `inject_references.py` |

### 利用側の使い方

per-file の「注入済み」トークンを書くプラグインは mtime を比較する:

```python
marker = pathlib.Path(tempfile.gettempdir()) / f"claude-session-ctx-gen-{session_id}"
if token.exists():
    # 直近の注入後にリセットが起きた場合だけ再注入
    if not (marker.exists() and marker.stat().st_mtime_ns > token.stat().st_mtime_ns):
        return  # まだ有効 → スキップ
token.touch()  # （再）注入してトークンの mtime を更新
```

**グレースフルフォールバック**: session-kit が未インストールならマーカーは存在しないので、
利用側は素の once-per-session として動く（session-kit 導入前の挙動）。session-kit は
**任意の companion** であり、利用側は未インストール時にハードフェイルしてはならない。

---

## なぜ専用プラグインか（フックロジックの集約ではない）

ここでのクロスプラグイン契約は **ファイルパス規約のみ** — 利用側はマーカーを `stat()` する
だけで、session-kit のスクリプトを実行しない。これにより `refs-inject-kit` が却下された
`${CLAUDE_PLUGIN_ROOT}` のクロスプラグイン・パス解決問題（incident
`premature-cross-plugin-centralization`）を回避できる。コンテキスト世代という事実は
本質的に **セッション単位の単一の事実**（セッションにつき 1 つ）なので、生成側を 1 つに
する設計が自然。

---

## バージョン

| バージョン | 主な変更 |
|---|---|
| 1.0.0 | 初版: PreCompact + SessionStart(clear) のコンテキスト世代マーカー（PR150） |
