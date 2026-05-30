# PR144 — add-next-kit-plan-skill

## 概要

next-kit プラグインに **`/next-kit:plan` スキル** を追加する。

ユーザーが「こんなページ/機能/APIを作りたい」と伝えると、next-kit の references を参照して **設計計画書（ISSUE ファイル形式）** を生成する 1 スキル。実際のファイルを scaffold するのではなく、「何をどう作るか」の計画書を出力することで、AI が直接コードを書く前にユーザーがレビューできる形にする。

3 用途（新規プロジェクト / feature 追加 / API 追加）を 1 スキルで検知・処理する。

**PR135 からの引き継ぎ背景**:
PR135 で next-kit references を 90 ファイルに整備した。references が確定したので、それを読んで計画書を生成するスキルを作る準備が整った。

### 実施条件

即時実施可（PR135 がマージ済み、references が安定）

### 関連PR

| PR番号 | 概要 |
|---|---|
| #135 | review-next-kit-plugin (references 整備、本 PR の入力) |
| #129 | create-py-kit-plugin (py-project スキルの参考実装) |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する（計画書フォーマット・用途検知方法など） | `.work/tasks/.../PR144/QA.md` |
| 済 | py-kit の `py-project` SKILL.md を参考にスキル設計・実装 | `plugins/next-kit/skills/plan/SKILL.md` (+ `.jp.md`) |
| 済 | plugin.json バンプ (3.3.0 → 3.4.0) | `plugins/next-kit/.claude-plugin/plugin.json` |
| 済 | marketplace.json 同期 | `.claude-plugin/marketplace.json` |
| 済 | next-kit references/CLAUDE.md にスキル記載を追記 | `plugins/next-kit/references/CLAUDE.md` (+ `.jp.md`) |

## 参考ドキュメント

- `.work/notes/next-kit-plan-skill.md`: 本 PR の設計メモ（旧設計からの変更経緯）
- `plugins/py-kit/skills/py-project/SKILL.md`: py-kit の参考実装（スキル構造・ステップ設計）
- `plugins/next-kit/references/`: scaffold 元となる規約集（90 ファイル）
- `plugins/next-kit/references/index.yaml` + `injection_rules.yaml`: ファイル種別 → reference マップ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |

## QA

なし
