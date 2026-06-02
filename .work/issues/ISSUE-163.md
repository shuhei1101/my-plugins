# ISSUE-163: JP ミラー7件の「英語原文」パス参照がサブフォルダ分割前の旧パスのまま

**作成日**: 2026-06-02

## 問題

v2.53.1 で `references/` がサブフォルダ（`notes/`・`work-dir/`・`skill-sync/`）に分割されたが、JP ミラーの「英語原文」参照行が旧パス（サブフォルダなし）のまま残っている。これは人間が手動で参照する際に混乱を招く（ファイルは実際には別の場所にある）。

## 対応方針

各 JP ミラーの「英語原文」行を現行の実際のパスに合わせて修正する。

## 対象ファイル

- `plugins/work/references/skill-sync/スタートスキル同期.jp.md`: `references/スタートスキル同期.md` → `references/skill-sync/スタートスキル同期.md`
- `plugins/work/references/skill-sync/ストッププロンプト同期.jp.md`: `references/ストッププロンプト同期.md` → `references/skill-sync/ストッププロンプト同期.md`
- `plugins/work/references/skill-sync/マージスキル同期.jp.md`: `references/マージスキル同期.md` → `references/skill-sync/マージスキル同期.md`
- `plugins/work/references/notes/ノート記述内容ルール.jp.md`: `references/ノート記述内容ルール.md` → `references/notes/ノート記述内容ルール.md`
- `plugins/work/references/work-dir/ワークディレクトリ構成.jp.md`: `ワークディレクトリ構成.md` → `references/work-dir/ワークディレクトリ構成.md`
- `plugins/work/references/work-dir/タスクインデックス.jp.md`: `タスクインデックス.md` → `references/work-dir/タスクインデックス.md`
- `plugins/work/references/work-dir/イシュー.jp.md`: `イシュー.md` → `references/work-dir/イシュー.md`

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
