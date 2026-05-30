# PR198 — dev-kit-markdown-frontmatter-rule

## 概要

`plugins/dev-kit/references/` に **マークダウン編集規約** を新規追加し、フロントマター付き md ファイルで「フロントマターの上に HTML コメント（`<!-- ... -->`）を置かない」というルールを明文化する。さらに違反を検出する PreToolUse(Edit/Write/MultiEdit) フックを dev-kit 同梱で追加する。

### 背景

PR184 で `plugins/claude-kit/skills/plugin-update/SKILL.jp.md` を新規作成した際、claude-kit の `references/common.md` の JP mirror 規約「Every JP mirror must start with the warning comment `<!-- This file is a Japanese mirror. ... -->`」に沿ってフロントマター(`---`) の上に HTML コメントを置いた結果、**Markdown プレビューがフロントマター（YAML 部分）を認識できず、フロントマターが本文として描画されて表示が崩れた**。

JP ミラー警告コメント自体は維持しつつ、配置位置を「フロントマターの上」ではなく「閉じ `---` の直後」に変更する必要がある。これは dev-kit / claude-kit の両方で守られるべき編集規約なので、より汎用な dev-kit 側に置く。

### 何をするか

- `plugins/dev-kit/references/markdown-editing.md` (+ `.jp.md`) を新規追加（短文）:
  - 「YAML フロントマター(`---` ブロック)を持つマークダウンファイルでは、開き `---` の上に HTML コメント・空行・本文を置かない」
  - 「警告コメント等が必要なら閉じ `---` の **直後** に書く」
  - Why: プレビューワがフロントマターを認識できなくなる
- `plugins/dev-kit/hooks/scripts/` に検出スクリプト（仮: `markdown_frontmatter_check.py`）を追加し、`hooks/hooks.json` に `PreToolUse(Edit | Write | MultiEdit)` のフックエントリを追加:
  - 対象: `*.md` への書き込み
  - 検出ロジック: 書き込み内容の先頭をスキャンし、最初の非空白行が `---` でなく、かつどこかに `---\n...\n---\n` の YAML ブロックが存在する場合に警告
  - ブロックではなく注意喚起（`block` ではなく `reason` のみで継続）
- claude-kit 側の規約更新:
  - `plugins/claude-kit/references/common.md` (+ jp) の JP mirror 規約セクションを「フロントマターの直後に置く」に書き換え
  - `plugins/claude-kit/references/provenance.md` 相当の説明文も同様に更新
- 既存の JP mirror ファイル（`*.jp.md` / `CLAUDE.jp.md` 等）でフロントマターの上にコメントを持つものを一括修正
  - `git grep -l '^<!-- This file is a Japanese mirror' -- '*.md'` で一覧化し、フロントマター直後に移す
- dev-kit を MINOR bump、changelog 追加

### 実施条件

即時実施可（PR184 のフロントマター上 HTML コメント修正コミット `052e42c` 以降）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | `## QA` の未決定事項を解消 | - 本ドキュメント |
| - | `.work/notes/` の関連ノート整備 | - 該当ノート |
| - | `plugins/dev-kit/references/markdown-editing.md` (+ jp) を作成 | - 新規 |
| - | `plugins/dev-kit/references/injection_rules.yaml` に新 reference を登録（注入対象パターン: `**/*.md`） | - 既存 yaml |
| - | `plugins/dev-kit/hooks/scripts/markdown_frontmatter_check.py` を作成 | - 新規 |
| - | `plugins/dev-kit/hooks/hooks.json` に PreToolUse(Edit/Write/MultiEdit) フックを追加 | - 既存 json |
| - | `plugins/claude-kit/references/common.md` (+ jp) の JP mirror セクションを「フロントマター直後に置く」へ更新 | - claude-kit references |
| - | 既存 `*.jp.md` / `CLAUDE.jp.md` でフロントマター上にコメントがあるものを一括修正 | - リポジトリ横断 |
| - | dev-kit を MINOR bump | - `plugins/dev-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | changelog 追加（`changelogs/v{X.Y.0}.md`） | - `plugins/dev-kit/changelogs/` |
| - | ルール / CLAUDE.md の更新（必要なら） | - 該当ファイル |
| - | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（フックは dev-kit/scripts 配下の検出ロジック、ドッグフードで動作確認） | - |

## QA

### QA-001: dev-kit-references-injection の `**/*.md` 注入はノイズが大きすぎないか

**背景**: `markdown-editing.md` を `**/*.md` で auto-inject すると、すべての md 編集時に注入される。フロントマターを持たない md（README 等）には不要な情報になる。

| 案 | 内容 |
|---|---|
| A | `**/*.md` で全注入し、リファレンス冒頭で「フロントマター無しなら無視してよい」と明示する |
| B | フロントマター付き md のみを狙う pattern が glob で書けないので、注入は行わず PreToolUse フック側だけで違反検出する（リファレンスは hook の reason 文に同梱） |
| C | `*.jp.md` と `CLAUDE.jp.md` と `SKILL.jp.md` 等 JP mirror 専用パターンに絞る |

**推奨方式**: B 案 — リファレンスは hook 違反時の `reason` にのみ流し、auto-inject はしない。普段のノイズを抑えつつ、違反を犯した瞬間だけ説明が出る。

**状態**: 未解決

**決定したら反映先**: `plugins/dev-kit/references/injection_rules.yaml`（B なら追加なし）、フック実装

### QA-002: フックの厳しさ（block か reason のみか）

**背景**: フロントマター上 HTML コメントは「プレビューが崩れるだけ」で機能上は壊れない。block 相当の厳しさが妥当か。

| 案 | 内容 |
|---|---|
| A | `reason` のみで継続を許可（注意喚起だけ） |
| B | `decision: block` で書き込みを止め、修正を強制する |

**推奨方式**: A 案 — ユーザー意図的に置きたいケースが将来出る可能性があり、まずは注意喚起ベースに留める。

**状態**: 未解決

**決定したら反映先**: `markdown_frontmatter_check.py` の出力 JSON

## 参考ドキュメント

- `plugins/claude-kit/references/common.md` — 現行の JP mirror 規約（更新対象）
- `plugins/dev-kit/references/injection_rules.yaml` — dev-kit の注入ルール（追加候補）
- `plugins/dev-kit/hooks/hooks.json` — dev-kit のフック設定

## 関連PR

| PR番号 | 概要 |
|---|---|
| #184 | claude-kit に plugin-update スキルを追加した際にフロントマター上 HTML コメントの問題が顕在化（本 PR の発端） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
