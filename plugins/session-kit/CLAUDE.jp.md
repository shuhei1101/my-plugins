<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# session-kit プラグイン開発ガイド

session-kit は Claude Code のセッションごとに **セッションマーカー** を 1 つ維持し、
`/compact` でコンテキストがリセットされたことを他プラグインが検知して、消えた内容を
再注入できるようにする。あわせて古いセッション一時ファイルを掃除する。

---

## 何をするか

| フック | 動作 |
|---|---|
| `PreCompact` | **セッションマーカー**を touch（compact 直前にコンテキストが落ちる） |
| `SessionStart` | **TTL 掃除**: 1 日以上前の古いセッション一時ファイルを削除 |

それ以外は **何もしない** — プロンプト注入もブロックも出力もなし。

### なぜ `/clear` を扱わないか

`/clear` は `session_id` 自体を変えるため、新セッションは自然に再注入される（新しい
`session_id` にはトークンが無く、旧トークンは旧 `session_id` のもの）。`session_id` が
同じまま残るリセットは `/compact` だけなので、マーカーは `PreCompact` でのみ touch する。

`resume` は `session_id` が同じだが会話が復元される（注入済み内容もコンテキストに戻る）
ため、マーカー更新は不要。

---

## セッションマーカー規約（他プラグインとの共有契約）

| | 値 |
|---|---|
| パス | `/tmp/claude-session-ctx-gen-{session_id}`（`tempfile.gettempdir()` 経由） |
| 意味 | mtime = このセッションで最後にコンテキストがリセット（`/compact`）された時刻 |
| 生成側 | session-kit（`hooks/ctx_marker.py`、`PreCompact` 時） |
| 利用側 | per-file の「注入トークン」を持つプラグイン — 例: py-kit / next-kit の `inject_references.py` |

### 利用側の使い方

per-file の注入トークンを書くプラグインは mtime を比較する:

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

## TTL 掃除（SessionStart）

空のマーカー/トークンファイルは放置すると `/tmp` に溜まり続ける（セッションごとに
`session_id` 単位のファイルが残る）。`SessionStart` のたびに、session-kit は以下に
マッチする **1 日**以上前のファイルを削除する:

| glob（`tempfile.gettempdir()` 下） | 持ち主 | 内容 |
|---|---|---|
| `claude-session-ctx-gen-*` | session-kit | セッションマーカー |
| `*-references-injection-*` | py-kit / next-kit / 将来の `*-kit` | 注入トークン |

1 日にする理由: それほど長いセッションは無く、アクティブなセッションのファイルは新しい
（< 1 日）ので消されない。並行セッションも同様に守られる。掃除が早すぎた場合の最悪でも
無害な再注入が走るだけ。

> 他プラグインの注入トークンを削除するのは **ファイル名規約の結合のみ**（session-kit は
> `/tmp` を glob するだけで、他プラグインのコードは実行しない）。掃除対象の glob は上表と
> `hooks/ctx_marker.py`（`_CLEANUP_GLOBS`）に明記。

---

## なぜ専用プラグインか（フックロジックの集約ではない）

ここでのクロスプラグイン契約は **ファイルパス / ファイル名規約のみ** — 利用側はマーカーを
`stat()` するだけで、session-kit のスクリプトを実行しない。これにより `refs-inject-kit` が
却下された `${CLAUDE_PLUGIN_ROOT}` のクロスプラグイン・パス解決問題（incident
`premature-cross-plugin-centralization`）を回避できる。コンテキスト世代という事実は
本質的に **セッション単位の単一の事実**（セッションにつき 1 つ）なので、生成側を 1 つに
する設計が自然。

---

## バージョン

| バージョン | 主な変更 |
|---|---|
| 1.1.0 | SessionStart を `/clear` マーカーバンプから 1 日 TTL の一時ファイル掃除へ役割変更。マーカーは PreCompact でのみ touch（PR151） |
| 1.0.0 | 初版: PreCompact + SessionStart(clear) のコンテキスト世代マーカー（PR150） |
