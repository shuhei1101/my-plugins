# ノートインデックス

`.work/notes/` 配下の設計メモ・構想ノートの一覧。カテゴリ別に分類。

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

---

## スキル設計

スキルの設計・実装に関するメモ。

| ファイル | タイトル |
|---|---|
| [ジェネレーターメタデータ.md](ジェネレーターメタデータ.md) | ジェネレーターメタデータ — creator スキル生成物の出自トレース機構 |
| [インタラクティブレビュースキル.md](インタラクティブレビュースキル.md) | インタラクティブレビュースキル — AskUserQuestion を使った 2 つのレビュー |
| [next-kitプランスキル.md](next-kitプランスキル.md) | next-kit:plan スキル — Next.js プロジェクト設計計画書生成 |
| [プラグイン設定スキル.md](プラグイン設定スキル.md) | プラグイン設定スキル — 設計メモ (PR167) |
| [pr-showスキル.md](pr-showスキル.md) | pr-show スキル — 次 PR 候補一覧の状況表示 |
| [ref-injectジェネレータ.md](ref-injectジェネレータ.md) | ref-inject — リファレンス自動注入プラグインのジェネレータ |
| [work-kitスキル群.md](work-kitスキル群.md) | work-kit スキル群 — 設計メモ |
| [AskUserQuestion制約リファレンス.md](AskUserQuestion制約リファレンス.md) | AskUserQuestion 制約リファレンス — スキルからの呼び出しガイド |

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

---

## 環境・設定・ポリシー

env 設定・運用ポリシー・用語規約に関するメモ。

| ファイル | タイトル |
|---|---|
| [保護ブランチenv化.md](保護ブランチenv化.md) | 保護ブランチ env 化 — PR177 |
| [envトグル実装メモ.md](envトグル実装メモ.md) | env トグル実装メモ — PR164 |
| [JPミラーポリシー.md](JPミラーポリシー.md) | JP ミラーポリシー — .md 作成時の .jp.md 強制 |
| [PR用語廃止・ブランチ用語統一.md](PR用語廃止・ブランチ用語統一.md) | PR 用語廃止・ブランチ用語統一 |

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

---

## 構想・企画

アイデア・構想段階のメモ。

| ファイル | タイトル |
|---|---|
| [AIイシュー自動発見システム構想.md](AIイシュー自動発見システム構想.md) | AI イシュー自動発見システム — 構想ノート |
