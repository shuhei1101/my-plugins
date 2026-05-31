# ノートインデックス

`.work/notes/` 配下の設計メモ・構想ノートの一覧。カテゴリ別サブフォルダに分類。

---

## コーディング規約・スタイル

コーディング規約・スタイルガイドに関するメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [Pythonスクリプトスタイル規約.md](コーディング規約・スタイル/Pythonスクリプトスタイル規約.md) | Python スクリプトスタイル規約 — my-plugins 内スクリプトの統一方針 |
| 2 | [マークダウンテーブル規約.md](コーディング規約・スタイル/マークダウンテーブル規約.md) | マークダウンテーブル規約 — Noカラムと繰り返し値の記法 |
| 3 | [JPミラーコードブロック同期規約.md](コーディング規約・スタイル/JPミラーコードブロック同期規約.md) | JPミラーコードブロック同期規約 — コードブロック内容は英語ソースと完全一致を維持する |
| 4 | [JPミラーヘッダーコメント規約.md](コーディング規約・スタイル/JPミラーヘッダーコメント規約.md) | JPミラーヘッダーコメント規約 — 標準形式と配置ルール |
| 5 | [JPミラー作成規約.md](コーディング規約・スタイル/JPミラー作成規約.md) | JPミラー作成規約 — .jp.md ファイルの作成ルールと既知の問題 |
| 6 | [E2Eテスト設計方針.md](コーディング規約・スタイル/E2Eテスト設計方針.md) | E2Eテスト設計方針 — ユースケース駆動設計 |
| 7 | [dev-kitリファレンス関数型スタイル規約.md](コーディング規約・スタイル/dev-kitリファレンス関数型スタイル規約.md) | dev-kit リファレンス関数型スタイル規約 — function-first / type 優先の徹底 |

---

## フック・自動化

フックの実装・設計・修正に関するメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [クリエータースキルフック-claude-kit.md](フック・自動化/クリエータースキルフック-claude-kit.md) | クリエータースキルフック (claude-kit) — UserPromptSubmit フック設計メモ |
| 2 | [dev-kitフック設計メモ.md](フック・自動化/dev-kitフック設計メモ.md) | dev-kit フック設計メモ |
| 3 | [注入フック修正メモ.md](フック・自動化/注入フック修正メモ.md) | py-kit / next-kit 注入フック修正メモ |
| 4 | [フック直接差し戻し選択理由.md](フック・自動化/フック直接差し戻し選択理由.md) | フック直接差し戻し方式の選択理由 — 設計判断メモ |
| 5 | [PreCompactフック.md](フック・自動化/PreCompactフック.md) | PreCompact フック — conversation-to-claude 自動実行 |
| 6 | [フックインラインPython切り出し.md](フック・自動化/フックインラインPython切り出し.md) | フックインライン Python 切り出し — hooks.json スクリプト分離 |
| 7 | [TypeScript型チェックフック.md](フック・自動化/TypeScript型チェックフック.md) | TypeScript 型チェックフック (PR143) |
| 8 | [Jinja2テンプレート記法メモ.md](フック・自動化/Jinja2テンプレート記法メモ.md) | Jinja2 テンプレート記法メモ — .j2 ファイル記述時の既知の罠と対処法 |
| 9 | [Jinja2テンプレート執筆ルール.md](フック・自動化/Jinja2テンプレート執筆ルール.md) | Jinja2 テンプレート執筆ルール — Markdown 出力時の注意事項 (PR222) |
| 10 | [vscode-workspace-syncスキル.md](フック・自動化/vscode-workspace-syncスキル.md) | vscode-workspace-syncスキル — VS Code ワークスペースと worktree の同期 |

---

## スキル設計

スキルの設計・実装に関するメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [ジェネレーターメタデータ.md](スキル設計/ジェネレーターメタデータ.md) | ジェネレーターメタデータ — creator スキル生成物の出自トレース機構 |
| 2 | [インタラクティブレビュースキル.md](スキル設計/インタラクティブレビュースキル.md) | インタラクティブレビュースキル — AskUserQuestion を使った 2 つのレビュー |
| 3 | [next-kitプランスキル.md](スキル設計/next-kitプランスキル.md) | next-kit:plan スキル — Next.js プロジェクト設計計画書生成 |
| 4 | [プラグイン設定スキル.md](スキル設計/プラグイン設定スキル.md) | プラグイン設定スキル — 設計メモ (PR167) |
| 5 | [plugin-config-reference.md](スキル設計/plugin-config-reference.md) | plugin-config リファレンス設計メモ — config スキル規約・ガイド (PR175) |
| 6 | [pr-showスキル.md](スキル設計/pr-showスキル.md) | pr-show スキル — 次 PR 候補一覧の状況表示 |
| 7 | [ref-injectジェネレータ.md](スキル設計/ref-injectジェネレータ.md) | ref-inject — リファレンス自動注入プラグインのジェネレータ |
| 8 | [work-kitスキル群.md](スキル設計/work-kitスキル群.md) | work-kit スキル群 — 設計メモ |
| 9 | [AskUserQuestion制約リファレンス.md](スキル設計/AskUserQuestion制約リファレンス.md) | AskUserQuestion 制約リファレンス — スキルからの呼び出しガイド |
| 10 | [claude-kit-plugin-update-sync.md](スキル設計/claude-kit-plugin-update-sync.md) | claude-kit 成果物同期 — plugin-update スキルによるリポジトリ規約同期 |
| 11 | [env-syncスキル.md](スキル設計/env-syncスキル.md) | env-syncスキル — WSL ↔ Windows 間の Claude Code 設定同期 |
| 12 | [debug-fabスキル.md](スキル設計/debug-fabスキル.md) | debug-fabスキル — 開発系画面のフロートデバッグボタン |
| 13 | [html-kitスキル群.md](スキル設計/html-kitスキル群.md) | html-kitスキル群 — dev-kit の HTML/UI 系スキル群と規約 |
| 14 | [skill-template-standards.md](スキル設計/skill-template-standards.md) | skill-template-standards — SKILL.jp.md テンプレート標準とサブエージェントガイド |

---

## プラグイン構成・統合

プラグインの構成変更・統合・廃止に関するメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [ルール廃止とリファレンス移行.md](プラグイン構成・統合/ルール廃止とリファレンス移行.md) | ルール廃止とリファレンス移行 — .claude/rules/ 削除方針 |
| 2 | [guard-kit統合メモ.md](プラグイン構成・統合/guard-kit統合メモ.md) | guard-kit を workspace に統合 — PR169 |
| 3 | [言語プラグイン統合メモ.md](プラグイン構成・統合/言語プラグイン統合メモ.md) | py-kit / html-kit / next-kit → dev-kit 統合 (PR166) |
| 4 | [プラグインCLAUDE標準構成.md](プラグイン構成・統合/プラグインCLAUDE標準構成.md) | プラグイン CLAUDE.md 標準構成 — 標準セクション定義 |
| 5 | [claude-kit-references-structure.md](プラグイン構成・統合/claude-kit-references-structure.md) | claude-kit リファレンス構造整理 — サブフォルダ分割設計メモ |
| 6 | [workリファレンスサブフォルダ構造.md](プラグイン構成・統合/workリファレンスサブフォルダ構造.md) | work リファレンスサブフォルダ構造 — notes/・work-dir/・skill-sync/ のカテゴリ定義と injection ルール |
| 7 | [plugin-migrate-rename.md](プラグイン構成・統合/plugin-migrate-rename.md) | plugin-migrate スキル命名規則 — plugin-update から plugin-migrate へのリネーム |
| 8 | [marketplace-upgradeコマンド.md](プラグイン構成・統合/marketplace-upgradeコマンド.md) | marketplace-upgradeコマンド — インストール済みプラグインの一括更新 |
| 9 | [リファレンスファイル名日本語化.md](プラグイン構成・統合/リファレンスファイル名日本語化.md) | リファレンスファイル名日本語化 — 全プラグインの references/ ファイル名を日本語に統一する |
| 10 | [remove-unused-references.md](プラグイン構成・統合/remove-unused-references.md) | remove-unused-references — claude-kit の未使用リファレンスファイル削除 |
| 11 | [setup-wizard-pattern.md](プラグイン構成・統合/setup-wizard-pattern.md) | setup-wizard パターン — プラグイン初回オンボーディングの規約 |
| 12 | [zero-plugin-dependency.md](プラグイン構成・統合/zero-plugin-dependency.md) | プラグイン間依存ゼロ — 棚卸しノート |

---

## 環境・設定・ポリシー

env 設定・運用ポリシー・用語規約に関するメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [保護ブランチenv化.md](環境・設定・ポリシー/保護ブランチenv化.md) | 保護ブランチ env 化 — PR177 |
| 2 | [envトグル実装メモ.md](環境・設定・ポリシー/envトグル実装メモ.md) | env トグル実装メモ（PR164 / feat/commit-message-options） |
| 3 | [jpミラーファイルヘッダー規約.md](環境・設定・ポリシー/jpミラーファイルヘッダー規約.md) | JP ミラーファイルヘッダー規約 — HTML コメント形式に統一 |
| 4 | [PR用語廃止・ブランチ用語統一.md](環境・設定・ポリシー/PR用語廃止・ブランチ用語統一.md) | PR 用語廃止・ブランチ用語統一 |
| 5 | [ノートフロントマタースキーマ.md](環境・設定・ポリシー/ノートフロントマタースキーマ.md) | ノートフロントマタースキーマ — `.work/notes/` ファイルの YAML ヘッダー仕様 |
| 6 | [スキル名プレフィックスポリシー.md](環境・設定・ポリシー/スキル名プレフィックスポリシー.md) | スキル名プレフィックスポリシー — SKILL.md の name フィールド命名規則 |

---

## バグ・不具合

バグ修正・不具合記録のメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [ステータスライン非表示バグ.md](バグ・不具合/ステータスライン非表示バグ.md) | ステータスライン非表示バグ — PR116 後の不具合メモ |
| 2 | [incident-marketplace-json-merge-conflict-sed-mistake.md](バグ・不具合/incident-marketplace-json-merge-conflict-sed-mistake.md) | インシデント — marketplace.json マージコンフリクトを sed で解消した結果 version 行が重複 |

---

## ワークフロー・マージ

開発ワークフロー・マージフローに関するメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [インシデント判定基準.md](ワークフロー・マージ/インシデント判定基準.md) | インシデント判定基準ノート (PR112) |
| 2 | [マージStep12-次PR一覧.md](ワークフロー・マージ/マージStep12-次PR一覧.md) | マージ Step 12 — 次 PR 一覧の出力フォーマット |
| 3 | [ノートインデックス同期ルール.md](ワークフロー・マージ/ノートインデックス同期ルール.md) | ノートインデックス同期ルール — _index.md 自動更新促進の設計メモ |
| 4 | [インシデント — マージスキルStep3スキップによるmaster上コンフリクト.md](ワークフロー・マージ/インシデント%20—%20マージスキルStep3スキップによるmaster上コンフリクト.md) | インシデント — マージスキル Step 3 スキップによる master 上コンフリクト |
| 5 | [ブランチインデックススキーマ.md](ワークフロー・マージ/ブランチインデックススキーマ.md) | ブランチインデックススキーマ — `.work/tasks/index.yaml` の構造と運用 |
| 6 | [イシューファイルテンプレート.md](ワークフロー・マージ/イシューファイルテンプレート.md) | イシューファイルテンプレート — 問題発生手順と修正案テーブル仕様 |

---

## 構想・企画

アイデア・構想段階のメモ。

| # | ファイル | タイトル |
|---|---|---|
| 1 | [AIイシュー自動発見システム構想.md](構想・企画/AIイシュー自動発見システム構想.md) | AI イシュー自動発見システム — 構想ノート |
