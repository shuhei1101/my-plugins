# ISSUE-153: プラグイン設定.md の reference implementation が不適切かつ opt-in 極性の記述が欠落

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/claude-kit/references/plugin/プラグイン設定.md` に 2 点の問題がある。

### 問題 1: reference implementation pointer が work を指しているが実態が不適切

`reference implementation: plugins/work/skills/plugin-config/SKILL.md` と記述されているが、work の plugin-config は 8 変数・CLAUDE.md との名前乖離（ISSUE-151 参照）・`AITUBER_NOTIFY` 特例など複雑な状態にあり、標準的な 5-step パターンの参照実装として適切ではない。

### 問題 2: opt-in 極性（デフォルト OFF）の記述が欠落

`## Managed toggle convention` セクションは normal polarity（absent = ON）のみを定義している。しかし `dev-kit:plugin-config` は opt-in polarity（absent = OFF、truthy で ON）を `DEV_KIT_PYTHON / HTML / NEXT / MARKDOWN` に使用している。このパターンがリファレンスに記載されていないため、新しい plugin-config 実装時に opt-in トグルの扱いを誤るリスクがある。

## 対応方針

1. `reference implementation` 行を `claude-kit:plugin-config` に変更するか、ポインタ行を削除して汎用的に保つ
2. `## Managed toggle convention` に opt-in polarity（absent = OFF、truthy で ON）のパターンを追記する
3. JP ミラーを同期する

## 対象ファイル

- `plugins/claude-kit/references/plugin/プラグイン設定.md`: reference implementation 修正、opt-in polarity セクション追記
- `plugins/claude-kit/references/plugin/プラグイン設定.jp.md`: JP ミラー同期

