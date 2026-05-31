# ノート再定義とspecs統合（現在の仕様書化）

> ブランチ: `refactor/notes-spec-and-ref-inject`

## 概要

ノートの意味を「現在の仕様書（スナップショット）」へ再定義し、`.work/specs/` を `.work/notes/` へ統合して廃止する。本ブランチは一連の大規模リファクタの**起点**であり、references / notes のカテゴリフォルダ化、templates 廃止＆タスク生成の REF-inject 化は後続ブランチへ分離した（`## 次ブランチ候補` 参照）。

**ノートの新しい意味**: ノートは「今どういう仕様・構成になっているか」だけを書くスナップショット仕様書。本文には過去の経緯・「なぜこうなったか」を書かない。何かが変わったら本文の古い記述はさっぱり消して上書きする。変更の足跡は末尾の `## 変更履歴` テーブルにのみ残す。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `## QA`（テンプレート案・specs統合方針・カテゴリ分類）をユーザーと解決する |
| 2 | 済 | 本ブランチの作業を反映（ノートの定義・ルールは references に集約。`work-dot-work-dir.md`/`notes-content-rules.md`） |
| 3 | 済 | `work-dot-work-dir.md` の `notes/` 節を全面改稿（旧 lifecycle・廃止済み `notes-to-claude` 記述を削除、「現在の仕様書」定義へ）。`.jp.md` も更新 |
| 4 | 済 | `notes-naming-rules.md` を改稿（命名規則は維持しつつ「現在の仕様書」前提に。`_index.md` 規則も）。`.jp.md` も更新 |
| 5 | 済 | 新規 `notes-content-rules.md` 作成（ノートに書く内容のルール＋固定テンプレート）。`.jp.md` も。`_index.yaml`/`_index.jp.yaml`/`_injection_rules.yaml` 登録 |
| 6 | 済 | `.work/specs/*`（20件）を精査し、新規ノート5件・既存マージ3系統・破棄9件に振り分け（下記） |
| 7 | 済 | `.work/specs/` 削除。`work-merge-skill-sync.md` の参照を notes へ付け替え |
| 8 | 済 | CLAUDE.md changelog 更新、バージョン bump（plugin.json/marketplace.json/CLAUDE.md+jp を v2.53.0 同期） |

### specs 処理結果

- **新規ノート化（5）**: `env-syncスキル` / `marketplace-upgradeコマンド` / `vscode-workspace-syncスキル` / `debug-fabスキル` / `html-kitスキル群`
- **既存ノートへマージ（3系統）**: `言語プラグイン統合メモ`（dev-kit-design・py-kit-design）/ `work-kitスキル群`（branch-index-cleanup・work-kit-merge-flow）/ `フックインラインPython切り出し`（work-kit-stop-hook）
- **破棄（9）**: claude-kit-conversation-skills, guard-kit, plugin-kit, plugin-root-templates, plugin-split, rules-organizer, todo-next-pr-section, work-kit-update-skill, xxx

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | (着手時に記入) | - | - | - |

## テスト

手動テスト・動作確認の実施記録。

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `inject_references.py` が新規 `notes-content-rules.md` を `.work/notes/**` 編集時に注入する | (未実施) | - |

## QA

### QA-001: ノートの新「現在の仕様書」テンプレート（解決済）

**決定**: frontmatter は使わない（人がレビューする `.jp` ミラー等で frontmatter が見えにくいため）。構成は以下。本文は現在状態のみ。変更の足跡は末尾 `## 変更履歴` テーブルに集約し、`関連タスク` 列にはタスクフォルダ名（git ブランチ名ではない）を書く。

```markdown
# {対象名} — {一行サマリ}

## 概要

これは何か。今どういう仕様・構成になっているかを 1〜3 行で。

## {セクション名（自由）}

今の状態だけを箇条書き／表で記述する。経緯・「なぜこうなったか」は書かない。

## 参考ドキュメント

- `path/to/related`: 何の資料か

## 変更履歴

| # | 日付 | 変更内容 | 関連タスク |
|---|---|---|---|
| 1 | 260531 | 新規作成 | 260531_notes-spec-and-ref-inject |
```

**状態**: 解決済

**反映先**: `references/notes-content-rules.md`（新規）＋ `work-dot-work-dir.md` の notes 節

### QA-002: specs の notes 統合方針（解決済）

**決定**: 案 A。specs を 1 件ずつ精査し、現在仕様として有用な内容だけ新スタイルでノート化（履歴は捨てる）。既に notes・本体ドキュメントで賄えるものは破棄し、破棄リストを報告する。

**状態**: 解決済

**反映先**: `.work/notes/`（当面フラット。フォルダ化は後続 B2）

### QA-003: カテゴリ分類とブランチ分割（解決済）

**決定**: 推奨案（references=英語フォルダ `notes/`/`work-dir/`/`skill-sync/`、notes=既存 `_index.md` の日本語カテゴリ）。ただしカテゴリ化作業自体は別ブランチへ分離（B1・B2）。タスクフォルダ日本語名化も別ブランチ（B3）。順序は `## 次ブランチ候補` のとおり。

**状態**: 解決済

**反映先**: `## 次ブランチ候補`

## 参考ドキュメント

- `plugins/work/references/work-dot-work-dir.md`: `.work/` 構成定義（notes 節を全面改稿）
- `plugins/work/references/notes-naming-rules.md`: ノート命名・index 規則（改稿）
- `plugins/work/references/.ref-injects/_injection_rules.yaml`: REF-inject パターン定義

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | refactor/branch-doc-filename-to-ja-title | 直前ブランチ。ブランチ文書ファイル名を日本語タイトル基準に変更 |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | references カテゴリ化 | `plugins/work/references/` を `notes/`・`work-dir/`・`skill-sync/` のサブフォルダに分割。`_index.yaml`/`_index.jp.yaml`/`_injection_rules.yaml` のパス更新、`_index.md` 再構成、`inject_references.py` の解決確認。※master で既に一部実施済みの可能性あり要確認 | 「本ブランチ」が完了したら |
| 2 | notes カテゴリ化 | `.work/notes/` を `_index.md` のカテゴリごとに日本語名サブフォルダへ分割。各ノート移動、`_index.md` 追従、frontmatter 履歴除去 | 「本ブランチ」が完了したら（references カテゴリ化と並行可） |
| 3 | templates廃止＋タスク生成REF-inject化＋タスクフォルダ日本語名化 | `plugins/work/templates/` 削除。`setup.py`/`setup-task.py`/`setup`/`start`/`plugin-migrate` をテンプレート非依存・REF-inject 参照へ改修。`.work/` 各フォルダの構成定義リファレンスを追加し編集時に注入。`.work/tasks/` のタスクフォルダ名を日本語化（生成ロジック・start/setup スキル・リファレンスを合わせて修正） | 「references カテゴリ化」が完了したら |
