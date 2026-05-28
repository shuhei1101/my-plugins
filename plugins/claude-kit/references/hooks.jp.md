<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
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

## reference 自動注入パターン（j2 テンプレート）

Claude がこれから触るファイルに応じた規約・ドキュメントを注入する
`PreToolUse(Edit|Write|MultiEdit|Read)` フック。代表実装は py-kit / next-kit
（`hooks/inject_references.py` + `hooks/templates/injection.md.j2` +
`references/injection_rules.yaml`）。

### 仕組み

1. Edit/Write/MultiEdit/Read で stdin の `tool_input.file_path` から対象パスを読む。
2. `injection_rules.yaml` の glob パターンと照合し、そのパスの `required` /
   `optional` reference を集める。
3. Jinja2 テンプレートで整形し `decision: block` の reason に出す。Claude は
   それを読んで従い、ツール呼び出しを再試行する。
4. `Read` も対象にすると、読み取りのみの経路（コードスキャン等）でも案内が効く。

### 注意 1 — 本文ではなくポインタを注入する

各 reference の本文全体を reason に展開しては**いけない**。フックは**マッチする
ファイル操作のたびに**発火するため、本文全量注入だと毎回全文が再注入され、
すぐにコンテキストを圧迫する。**path + 1 行 description** だけを注入し、本文は
Claude が必要なものを `Read` する。（incident: `injection-hook-full-body-bloat`）

### 注意 2 — 注入するポインタは絶対パスにする

`${CLAUDE_PLUGIN_ROOT}` は **hooks.json の中でのみ**展開される。フックが print する
reason テキスト内では展開されない。`references/foo.md` のような相対パスは
*編集対象プロジェクト* の cwd 基準で解決され（プラグインキャッシュではない）失敗する。
フックスクリプト自身が**絶対パス**を生成して出す必要がある。例:

```python
abs_path = (refs_dir / rel_path).as_posix()   # refs_dir は CLAUDE_PLUGIN_ROOT から導出
```

### 注意 3 — パターン単位トークンで注入を重複排除

重複排除しないとマッチするファイル操作のたびに再注入される。トークンを**マッチした
ルールのパターン単位**（ファイルパスではない）にすると、同じパターンにマッチする全ファイルで
共有され、未注入（トークンが無い）パターンの reference だけを注入できる:

```python
token_dir = pathlib.Path.home() / '.claude' / 'tokens' / 'my-kit'   # プラグインごとにサブフォルダ
required, optional, new_tokens = [], [], []
for rule in matched_rules:
    pat_hash = hashlib.sha1(rule['pattern'].encode('utf-8')).hexdigest()[:12]
    token = token_dir / f'{session_id}-{pat_hash}'
    if token.exists():
        continue                      # このパターンは注入済み → reference をスキップ
    new_tokens.append(token)
    required += rule.get('required', [])
    optional += rule.get('optional', [])
if not required and not optional:
    sys.exit(0)                       # 新たに注入するものなし
token_dir.mkdir(parents=True, exist_ok=True)
for token in new_tokens:
    token.touch()                     # これらのパターンを注入済みにする（消費しない）
```

> トークンは `~/.claude/tokens/{plugin}/`（プラグインごとにサブフォルダ）に置く。こうすると
> session-kit が `~/.claude/tokens/*/...` の単一 glob でまとめて管理できる。

> パターン単位（ファイル単位ではない）の意味: あるパターンの reference がどれかのファイル
> 経由で一度注入されたら、同じパターンにマッチする他のファイルはそれをスキップする。
> *追加の*パターンにマッチするファイルは、その追加パターンの reference だけを注入する。

> ⚠️ **制約 — コンテキストのリセットとトークンの寿命。** トークンは「注入済み＝まだ
> コンテキストにある」を前提にするが、`/compact` は `session_id` を保ったままコンテキストを
> 要約する。また、トークンをセッション全体で持つと長すぎることが多い — 長い会話だと注入した
> 案内がずっと上に埋もれる。任意の `session-kit` プラグインは両方を解決する: **毎
> `UserPromptSubmit` でセッションのトークンを削除**し（キャッシュを会話*ターン*単位にする —
> `/compact` 後も含めターンごとに再注入）、`SessionStart` で古いトークンを 1 日 TTL で掃除する。
> 利用側は無自覚でよい: トークンを作って存在チェックするだけで、session-kit が外部から削除する。
> session-kit が無い場合はトークンがセッション全体で生きる（once-per-pattern）。`/clear` は
> 対応不要 — `session_id` が変わるので新セッションが自然に再注入する。

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
