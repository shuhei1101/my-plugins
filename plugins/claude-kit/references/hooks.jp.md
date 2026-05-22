# hooks.jp.md — フック設計ガイド（日本語ミラー）

> このファイルは `references/hooks.md` の日本語ミラーです。
> 変更する場合は JP ミラーを先に更新し、その後英語版にも反映してください。

---

# フック設計ガイド

`.claude/hooks/` と `settings.json` のフック設計・作成に使う知識をまとめたドキュメント。
プロンプト注入型フック（stdout にプロンプトを出力して Claude のコンテキストへ注入するタイプ）を対象とする。

---

## フックイベント一覧

| イベント | 発火タイミング | 用途 |
|---|---|---|
| `UserPromptSubmit` | ユーザーがプロンプトを送信するたびに | 毎回確認させたいルール・チェックリスト |
| `Stop` | Claude が応答を止めるたびに | 作業完了後のチェック・後処理の強制 |
| `PreToolUse` | ツール実行前 | 危険な操作のブロック・確認 |
| `PostToolUse` | ツール実行後 | 編集後の通知・検証 |
| `SessionStart` | セッション開始時 | 初期コンテキストの注入 |

---

## プロンプト注入の仕組み

| フック | stdout の形式 | Claude への影響 |
|---|---|---|
| `UserPromptSubmit` | テキストをそのまま出力 | `<system-reminder>` として注入 |
| `Stop` | `{"decision":"block","reason":"<プロンプト>"}` | Claude が作業を継続する |
| `PreToolUse` | `{"decision":"block","reason":"<プロンプト>"}` | ツール実行をブロックして指示注入 |

---

## フックを使うべきケース

以下の性質があれば、rules / CLAUDE.md よりフックの方が適切:

- 「プロンプト送信のたびに確認する」「毎回チェックする」 → `UserPromptSubmit`
- 「Claude が止まるたびに〜する」「作業完了後に確認する」 → `Stop`
- 「ツール実行前に確認する」 → `PreToolUse`
- 「ファイル編集後に通知する」 → `PostToolUse`

---

## NG パターン

- 一度だけ確認すればよい内容 → フックは毎回発火するため過剰
- 長文プロンプト → `Stop` フックの `reason` はユーザー画面に表示されるため極力短くする
- ループ対策なしのブロック系フック → `Stop` は `stop_hook_active`、`PreToolUse` はワンタイムトークンで防止する

---

## ループ防止

### Stop フック

`stdin JSON` に `stop_hook_active: true` が含まれる場合は再発火中なので `exit(0)` で抜ける:

```python
d = json.loads(sys.stdin.read())
if d.get('stop_hook_active'):
    sys.exit(0)  # 再発火 → スルー
```

### PreToolUse フック（ワンタイムトークン）

```python
session_id = d.get('session_id', 'default')
token = pathlib.Path(tempfile.gettempdir()) / f'my-guard-token-{session_id}'
if token.exists():
    token.unlink()   # トークンを消費して通過
    sys.exit(0)
token.touch()        # ブロック + トークン作成
```

---

## 配置場所

| 配置場所 | ファイル | 共有 |
|---|---|---|
| プラグイン | `plugins/{name}/hooks/hooks.json` | ✅ プラグインに同梱 |
| プロジェクト（チーム共有） | `.claude/settings.json` の `hooks` セクション | ✅ git にコミット |
| プロジェクト（ローカル限定） | `.claude/settings.local.json` の `hooks` セクション | ❌ `.gitignore` 推奨 |

---

## パス変数

| 変数 | 使える場所 | 意味 |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | プラグインの hooks.json のみ | プラグインのインストール先ルート |
| `${CLAUDE_PROJECT_DIR}` | settings.json / settings.local.json | プロジェクトルート |
