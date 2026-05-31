# ノートインデックス

`.work/notes/` 配下の設計メモ・構想ノートの一覧。カテゴリ別に分類。

---

## コーディング規約・スタイル

コーディング規約・スタイルガイドに関するメモ。

| ファイル | タイトル |
|---|---|
| [Pythonスクリプトスタイル規約.md](Pythonスクリプトスタイル規約.md) | Python スクリプトスタイル規約 — my-plugins 内スクリプトの統一方針 |

---

## フック・自動化

フックの実装・設計・修正に関するメモ。

| ファイル | タイトル |
|---|---|
| [クリエータースキルフック-claude-kit.md](クリエータースキルフック-claude-kit.md) | クリエータースキルフック (claude-kit) — UserPromptSubmit フック設計メモ |
| [dev-kitフック設計メモ.md](dev-kitフック設計メモ.md) | dev-kit フック設計メモ |
| [注入フック修正メモ.md](注入フック修正メモ.md) | py-kit / next-kit 注入フック修正メモ |
| [フック直接差し戻し選択理由.md](フック直接差し戻し選択理由.md) | フック直接差し戻し方式の選択理由 — 設計判断メモ |
| [PreCompactフック.md](PreCompactフック.md) | PreCompact フック — conversation-to-claude 自動実行 |
| [フックインラインPython切り出し.md](フックインラインPython切り出し.md) | フックインライン Python 切り出し — hooks.json スクリプト分離 |
| [TypeScript型チェックフック.md](TypeScript型チェックフック.md) | TypeScript 型チェックフック (PR143) |
| [Jinja2テンプレート記法メモ.md](Jinja2テンプレート記法メモ.md) | Jinja2 テンプレート記法メモ — .j2 ファイル記述時の既知の罠と対処法 |
| [Jinja2テンプレート執筆ルール.md](Jinja2テンプレート執筆ルール.md) | Jinja2 テンプレート執筆ルール — Markdown 出力時の注意事項 (PR222) |
| [vscode-workspace-syncスキル.md](vscode-workspace-syncスキル.md) | vscode-workspace-syncスキル — VS Code ワークスペースと worktree の同期 |

---

## スキル設計

スキルの設計・実装に関するメモ。

| ファイル | タイトル |
|---|---|
| [ジェネレーターメタデータ.md](ジェネレーターメタデータ.md) | ジェネレーターメタデータ — creator スキル生成物の出自トレース機構 |
| [インタラクティブレビュースキル.md](インタラクティブレビュースキル.md) | インタラクティブレビュースキル — AskUserQuestion を使った 2 つのレビュー |
| [next-kitプランスキル.md](next-kitプランスキル.md) | next-kit:plan スキル — Next.js プロジェクト設計計画書生成 |
| [プラグイン設定スキル.md](プラグイン設定スキル.md) | プラグイン設定スキル — 設計メモ (PR167) |
| [plugin-config-reference.md](plugin-config-reference.md) | plugin-config リファレンス設計メモ — config スキル規約・ガイド (PR175) |
| [pr-showスキル.md](pr-showスキル.md) | pr-show スキル — 次 PR 候補一覧の状況表示 |
| [ref-injectジェネレータ.md](ref-injectジェネレータ.md) | ref-inject — リファレンス自動注入プラグインのジェネレータ |
| [work-kitスキル群.md](work-kitスキル群.md) | work-kit スキル群 — 設計メモ |
| [AskUserQuestion制約リファレンス.md](AskUserQuestion制約リファレンス.md) | AskUserQuestion 制約リファレンス — スキルからの呼び出しガイド |
| [claude-kit-plugin-update-sync.md](claude-kit-plugin-update-sync.md) | claude-kit 成果物同期 — plugin-update スキルによるリポジトリ規約同期 |
| [env-syncスキル.md](env-syncスキル.md) | env-syncスキル — WSL ↔ Windows 間の Claude Code 設定同期 |
| [debug-fabスキル.md](debug-fabスキル.md) | debug-fabスキル — 開発系画面のフロートデバッグボタン |
| [html-kitスキル群.md](html-kitスキル群.md) | html-kitスキル群 — dev-kit の HTML/UI 系スキル群と規約 |

---

## プラグイン構成・統合

プラグインの構成変更・統合・廃止に関するメモ。

| ファイル | タイトル |
|---|---|
| [ルール廃止とリファレンス移行.md](ルール廃止とリファレンス移行.md) | ルール廃止とリファレンス移行 — .claude/rules/ 削除方針 |
| [guard-kit統合メモ.md](guard-kit統合メモ.md) | guard-kit を workspace に統合 — PR169 |
| [言語プラグイン統合メモ.md](言語プラグイン統合メモ.md) | py-kit / html-kit / next-kit → dev-kit 統合 (PR166) |
| [プラグインCLAUDE標準構成.md](プラグインCLAUDE標準構成.md) | プラグイン CLAUDE.md 標準構成 — 標準セクション定義 |
| [claude-kit-references-structure.md](claude-kit-references-structure.md) | claude-kit リファレンス構造整理 — サブフォルダ分割設計メモ |
| [plugin-migrate-rename.md](plugin-migrate-rename.md) | plugin-migrate スキル命名規則 — plugin-update から plugin-migrate へのリネーム |
| [marketplace-upgradeコマンド.md](marketplace-upgradeコマンド.md) | marketplace-upgradeコマンド — インストール済みプラグインの一括更新 |
| [リファレンスファイル名日本語化.md](リファレンスファイル名日本語化.md) | リファレンスファイル名日本語化 — 全プラグインの references/ ファイル名を日本語に統一する |

---

## 環境・設定・ポリシー

env 設定・運用ポリシー・用語規約に関するメモ。

| ファイル | タイトル |
|---|---|
| [保護ブランチenv化.md](保護ブランチenv化.md) | 保護ブランチ env 化 — PR177 |
| [envトグル実装メモ.md](envトグル実装メモ.md) | env トグル実装メモ（PR164 / feat/commit-message-options） |
| [JPミラーポリシー.md](JPミラーポリシー.md) | JP ミラーポリシー — .md 作成時の .jp.md 強制 |
| [jpミラーファイルヘッダー規約.md](jpミラーファイルヘッダー規約.md) | JP ミラーファイルヘッダー規約 — HTML コメント形式に統一 |
| [PR用語廃止・ブランチ用語統一.md](PR用語廃止・ブランチ用語統一.md) | PR 用語廃止・ブランチ用語統一 |
| [ノートフロントマタースキーマ.md](ノートフロントマタースキーマ.md) | ノートフロントマタースキーマ — `.work/notes/` ファイルの YAML ヘッダー仕様 |

---

## バグ・不具合

バグ修正・不具合記録のメモ。

| ファイル | タイトル |
|---|---|
| [ステータスライン非表示バグ.md](ステータスライン非表示バグ.md) | ステータスライン非表示バグ — PR116 後の不具合メモ |

---

## ワークフロー・マージ

開発ワークフロー・マージフローに関するメモ。

| ファイル | タイトル |
|---|---|
| [インシデント判定基準.md](インシデント判定基準.md) | インシデント判定基準ノート (PR112) |
| [マージStep12-次PR一覧.md](マージStep12-次PR一覧.md) | マージ Step 12 — 次 PR 一覧の出力フォーマット |
| [ノートインデックス同期ルール.md](ノートインデックス同期ルール.md) | ノートインデックス同期ルール — _index.md 自動更新促進の設計メモ |
| [インシデント — マージスキルStep3スキップによるmaster上コンフリクト.md](インシデント — マージスキルStep3スキップによるmaster上コンフリクト.md) | インシデント — マージスキル Step 3 スキップによる master 上コンフリクト |

---

## 構想・企画

アイデア・構想段階のメモ。

| ファイル | タイトル |
|---|---|
| [AIイシュー自動発見システム構想.md](AIイシュー自動発見システム構想.md) | AI イシュー自動発見システム — 構想ノート |
