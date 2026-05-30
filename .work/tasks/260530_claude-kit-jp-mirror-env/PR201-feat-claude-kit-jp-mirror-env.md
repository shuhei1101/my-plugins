# PR201 — claude-kit-jp-mirror-env

## 概要

`CLAUDE_KIT_JP_MIRROR` 環境変数を追加し、JP ミラーファイル（`.jp.md`）を作るかどうかをユーザーが制御できるようにする。

- **デフォルト（`true` または未設定）**: 現行の動作を維持。`.jp.md` ミラーを別ファイルとして作成する
- **`false` の場合**: `.jp.md` を作らず、本体の `.md` ファイルを日本語で直接書く

`references/common.md` の JP/EN mirror rules セクションに分岐条件を追記し、
`CLAUDE.md` の環境変数テーブルに新変数を追加する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - |
| 済 | `.work/notes/` の関連ノートを確認・更新する | - |
| 済 | `CLAUDE_KIT_JP_MIRROR` の動作説明を JP/EN mirror rules セクションに追記する | - `references/common.md`<br>- `references/common.jp.md` |
| 済 | 環境変数テーブルに `CLAUDE_KIT_JP_MIRROR` を追加する | - `plugins/claude-kit/CLAUDE.md`<br>- `plugins/claude-kit/CLAUDE.jp.md` |
| 済 | バージョンをバンプする | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | ルール・CLAUDE.md を更新する | - |
| 済 | inject_references.py に CLAUDE_KIT_JP_MIRROR 読み取りを追加し jp_mirror をテンプレートに渡す | - `hooks/scripts/inject_references.py` |
| 済 | 注入テンプレートに jp_mirror=false 時の1行通知を追加する | - `hooks/templates/injection.md.j2`<br>- `hooks/templates/injection.jp.md.j2` |
| 済 | common.md の echo アプローチを削除し「注入通知に従う」形に書き直す | - `references/common.md`<br>- `references/common.jp.md` |
| 済 | 「マークダウンは env var 読めない」知見を plugin-structure.md に追記する | - `references/plugin-structure.md`<br>- `references/plugin-structure.jp.md` |
| - | jp_mirror 通知の改行構造を修正（trim_blocks との相互作用） | - `hooks/templates/injection.md.j2`<br>- `hooks/templates/injection.jp.md.j2` |
| - | `{% if optional %}` 直後 `---` の setext heading バグを修正（元からのバグ） | - `hooks/templates/injection.md.j2`<br>- `hooks/templates/injection.jp.md.j2` |
| - | `## {{ ref.path }}` 末尾に `<!-- -->` を追加してレンダリングバグを抑制する | - `hooks/templates/injection.md.j2`<br>- `hooks/templates/injection.jp.md.j2` |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/common.md` | 編集 | JP/EN mirror rules を書き直し（注入ヘッダーを確認する形に） | - |
| `plugins/claude-kit/references/common.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/references/plugin-structure.md` | 編集 | 「マークダウンは env var 読めない」知見と2パターンを追記 | - |
| `plugins/claude-kit/references/plugin-structure.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/hooks/scripts/inject_references.py` | 編集 | `CLAUDE_KIT_JP_MIRROR` 読み取り・`jp_mirror` をテンプレートに渡す | - |
| `plugins/claude-kit/hooks/templates/injection.md.j2` | 編集 | `jp_mirror=false` 時の1行通知を追加 | - |
| `plugins/claude-kit/hooks/templates/injection.jp.md.j2` | 編集 | 同上の日本語版 | - |
| `plugins/claude-kit/CLAUDE.md` | 編集 | 環境変数テーブルに `CLAUDE_KIT_JP_MIRROR` を追加、Changelog 追加 | - |
| `plugins/claude-kit/CLAUDE.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | バージョン `3.43.1` → `3.44.0` | MINOR |
| `.claude-plugin/marketplace.json` | 編集 | claude-kit バージョン `3.43.1` → `3.44.0` | MINOR |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| (テストなし) | - | - | - |

## QA

QA 事項なし。

## 参考ドキュメント

- `plugins/claude-kit/references/environment.md`: 環境変数の設計規約
- `.work/notes/jp-mirror-policy.md`: JP ミラーポリシーのメモ

## 関連PR

| PR番号 | 概要 |
|---|---|
| - | - |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| `claude-kit-markdown-env-var-audit` | 他のマークダウンファイル（SKILL.md・ルール・references）で「`echo $VAR` で env var を確認せよ」等の誤った指示がないか全量調査し、あれば修正する | 即時実施可 |
