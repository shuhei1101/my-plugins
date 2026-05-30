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

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/common.md` | 編集 | `CLAUDE_KIT_JP_MIRROR` の動作分岐を JP/EN mirror rules セクションに追記 | - |
| `plugins/claude-kit/references/common.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/CLAUDE.md` | 編集 | 環境変数テーブルに `CLAUDE_KIT_JP_MIRROR` を追加 | - |
| `plugins/claude-kit/CLAUDE.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | バージョンバンプ | MINOR |
| `.claude-plugin/marketplace.json` | 編集 | バージョンバンプ | MINOR |

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
| - | - | - |
