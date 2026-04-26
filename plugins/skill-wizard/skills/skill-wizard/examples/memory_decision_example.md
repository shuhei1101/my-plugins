# フォルダ構成変更の判断 - 20260426 143000

## 対象スキル
skill-wizard（全プラグイン共通）

## 決定事項の種類
- [x] アーキテクチャ案 (architecture_ideas)

## 決定内容
assets/ フォルダを examples/ にリネームし、ファイル内容をプレースホルダー形式から具体例形式に変更することを決定。

## 判断の根拠
- 公式 Claude Code ドキュメントは scripts/ と examples/ のみ言及
- AI は空白テンプレートよりも具体的な例から Few-shot 的に学習しやすい
- examples/ に統一することでフォルダの意図が明確になる

## 影響範囲
- py-wizard: 2ファイル
- skill-wizard: 8ファイル
- wiki-wizard: 5ファイル
- 各 SKILL.md / references/ の参照パスを更新

## 決定日
2026-04-26
