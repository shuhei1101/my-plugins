# referencesサブフォルダ分割

> ブランチ: `refactor/references-subfolder-split`

## 概要

`plugins/*/references/` 配下のリファレンスを、平置きからカテゴリ別サブフォルダへ分割する。

### このブランチが必要な理由・前ブランチとの関係

- 前ブランチ `refactor/notes-spec-and-ref-inject`（ノート再定義＋specs統合）の QA-003 で、references / notes のカテゴリ化を別ブランチへ分離することに合意した。本ブランチはその references 側。
- **重要**: master の別ブランチで「全プラグインの references ファイル名を日本語化」が既に実施済み（例: `work-dot-work-dir.md` → `ドットワークディレクトリ構成.md`）。リネームは完了しているため、**本ブランチの残スコープはサブフォルダ分割のみ**。
- 注入機構（`inject_references.py`）は既にサブフォルダ配下のリファレンスを解決できる（claude-kit の `references/markdown/...` 等で稼働実績あり）。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | x | 未解決事項を `## QA` に記録 |
| 2 | x | work プラグイン references のカテゴリ分類を決める（例: `notes/`＝ノート命名規則・ノート記述内容ルール、`work-dir/`＝ドットワークディレクトリ構成、`skill-sync/`＝マージスキル同期・スタートスキル同期・ストッププロンプト同期・TODOテンプレート同期）。日本語/英語フォルダ名の方針も確認 |
| 3 | x | 各 `.md`/`.jp.md` をカテゴリサブフォルダへ `git mv`。`_index.yaml`/`_index.jp.yaml`/`_injection_rules.yaml` のパスをサブフォルダ込みに更新 |
| 4 | x | リファレンス内部リンク（相互参照・`Japanese mirror:` 等）のパスを更新 |
| 5 | x | `inject_references.py` がサブフォルダ配下を正しく注入することを確認（実ファイル編集で検証） |
| 6 | x | 他プラグイン（claude-kit/dev-kit 等）の references 構造と規約を揃えるか確認。揃える場合は別作業として切り出すか本ブランチ範囲を明示 |
| 7 | x | バージョン bump（plugin.json/marketplace.json/CLAUDE.md changelog 同期） |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/references/notes/` | 新規 | ノート命名規則・ノート記述内容ルール を移動 | git mv |
| 2 | `plugins/work/references/work-dir/` | 新規 | ドットワークディレクトリ構成 を移動 | git mv |
| 3 | `plugins/work/references/skill-sync/` | 新規 | マージスキル同期・スタートスキル同期・ストッププロンプト同期・TODOテンプレート同期 を移動 | git mv |
| 4 | `plugins/work/references/.ref-injects/_index.yaml` | 編集 | path をサブフォルダ込みに更新 | |
| 5 | `plugins/work/references/.ref-injects/_index.jp.yaml` | 編集 | 〃 | |
| 6 | `plugins/work/references/.ref-injects/_injection_rules.yaml` | 編集 | required パスをサブフォルダ込みに更新 | |
| 7 | 各 `.md`（7ファイル）| 編集 | `Japanese mirror:` パスをサブフォルダ込みに更新 | |
| 8 | `plugins/work/.claude-plugin/plugin.json` | 編集 | v2.53.1 にバンプ | |
| 9 | `.claude-plugin/marketplace.json` | 編集 | 〃 | |
| 10 | `plugins/work/CLAUDE.md` / `CLAUDE.jp.md` | 編集 | changelog に v2.53.1 を追加 | |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | サブフォルダ配下リファレンスが編集時に注入される | inject_references.py を直接実行し skill-sync/マージスキル同期.md の注入を確認 | OK |

## QA

（現時点で未解決事項なし。Step 2 のカテゴリ分類は着手時に確定する）

## 参考ドキュメント

- `.work/notes/リファレンスファイル名日本語化.md`: master の references 日本語リネームの現在仕様
- `.work/notes/claude-kit-references-structure.md`: サブフォルダ分割の設計メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | refactor/notes-spec-and-ref-inject | 前ブランチ。ノート再定義＋specs統合。QA-003 で本ブランチを分離合意 |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | templates廃止＋タスク生成REF-inject化＋タスクフォルダ日本語名化 | `plugins/work/templates/` 削除。`setup.py`/`setup-task.py`/`setup`/`start`/`plugin-migrate` をテンプレート非依存・REF-inject 参照へ改修。`.work/` 各フォルダの構成定義リファレンスを追加し編集時に注入。`.work/tasks/` のタスクフォルダ名を日本語化（生成ロジック・スキル・リファレンスを合わせて修正） | 即時実施可 |
