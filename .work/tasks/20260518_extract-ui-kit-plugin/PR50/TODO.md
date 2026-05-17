# PR50 — extract-ui-kit-plugin

## 概要

`dev-kit` から UI 関連を分離し、新プラグイン **`ui-kit`** を新設する。
さらに新スキル `logging`(ログ整備)と `flocss-apply`(FLOCSS 適用)を追加する。

役割分担:
- **dev-kit**: 開発規約全般(Python・YAML・将来の他言語規約)
- **ui-kit**: 開発用 UI コンポーネント提供 + UI 規約

合わせて dev-kit の空 references は削除し、現状有効な内容のみ残す。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260518_extract-ui-kit-plugin/PR50/QA.md` |
| 済 | 仕様書 `ui-kit-design.md` を新規作成 | - `.work/specs/ui-kit-design.md` |
| 済 | 仕様書 `dev-kit-design.md` を更新(UI 関連を削除) | - `.work/specs/dev-kit-design.md` |
| 済 | `ui-kit` プラグインスケルトン作成 | - `plugins/ui-kit/.claude-plugin/plugin.json` |
| 済 | `ui-kit/references/principles.md` 作成(DRY/FLOCSS/JS 規約/frontend-design 必須) | - `plugins/ui-kit/references/principles.md`, `principles.jp.md` |
| 済 | dev-kit `skills/ui-dev/` を ui-kit に移動・改名 `debug-fab/` | - `plugins/ui-kit/skills/debug-fab/` |
| 済 | `ui-kit/skills/logging/` 新規作成(ログ規約・出力レベル別ガイド) | - `plugins/ui-kit/skills/logging/SKILL.md`, `SKILL.jp.md` |
| 済 | `ui-kit/skills/flocss-apply/` 新規作成(新規/既存両対応) | - `plugins/ui-kit/skills/flocss-apply/SKILL.md`, `SKILL.jp.md` |
| 済 | dev-kit から空 references を削除 | - `plugins/dev-kit/references/{backend,vscode-extension,html,css,js,frontend,common}.{md,jp.md}` |
| 済 | dev-kit `skills/ui-dev/` を削除(ui-kit 側に移動済) | - `plugins/dev-kit/skills/ui-dev/` |
| 済 | dev-kit バージョン更新(1.1.0 → 2.0.0、破壊的変更) | - `plugins/dev-kit/.claude-plugin/plugin.json` |
| 済 | marketplace.json に ui-kit 追加、dev-kit バージョン更新 | - `.claude-plugin/marketplace.json` |
| 済 | CSS-JS 紐付けルールを `/rule-creator` で作成 | - `.claude/rules/{name}.md`(rule-creator が決定) |
| 済 | `ui-kit/references/ui-design.md` 新規作成(画面設計規約・画面タイプ別パターン・レスポンシブ) | - `plugins/ui-kit/references/ui-design.md`, `ui-design.jp.md` |
| 済 | `ui-kit/skills/mock/` 新規作成(モック画面生成スキル・案 A〜E のタブ切替形式) | - `plugins/ui-kit/skills/mock/SKILL.md`, `SKILL.jp.md` |
| 済 | `mock` スキル用テンプレート(タブ切替モック雛形 HTML) | - `plugins/ui-kit/skills/mock/templates/` |
| 済 | ui-kit-design.md 仕様書に mock スキル + ui-design.md を追記 | - `.work/specs/ui-kit-design.md` |
| 済 | principles.md 強化(JSDoc リテラル/型エイリアス/アロー関数/引数注入、AI 前提の拡張性、ルーティング集約、定数集約) | - `plugins/ui-kit/references/principles.md`, `principles.jp.md` |
| 済 | ui-design.md に「共通コンポーネント化必須」の方針を明記(状態系/入力系/a11y/モーション) | - `plugins/ui-kit/references/ui-design.md`, `ui-design.jp.md` |
| 済 | 共通コンポーネント先読み強制ルールテンプレを追加 | - `plugins/ui-kit/templates/rules/common-component-first.md` |
| 済 | 既存スキル(mock/flocss-apply/debug-fab/logging)に「最終ステップで rule-creator でリンク」「最初に共通コンポーネント/定数/ルーティング確認」を追記 | - `plugins/ui-kit/skills/*/SKILL.md`, `SKILL.jp.md` |
| 済 | 新スキル `ui-kit:implement` 作成(モック → 実装フェーズ用、最初に constants / routing / common-components を確認 → 設計 → 実装 → ルール連携) | - `plugins/ui-kit/skills/implement/SKILL.md`, `SKILL.jp.md` |
| 済 | ルールテンプレートに日本語版を追加(`.jp.md` ペア。`.claude/rules-jp/` へコピー) | - `plugins/ui-kit/templates/rules/{css-js-link,common-component-first}.jp.md` |
| 済 | flocss-apply / implement スキルの「ルール導入」ステップを EN+JP の両方コピーに更新 | - `plugins/ui-kit/skills/flocss-apply/SKILL.md`, `implement/SKILL.md` (各 JP も) |
| 済 | `flocss-apply` を `implement` に統合(FLOCSS セットアップ手順を implement の Step 3 に挿入) | - `plugins/ui-kit/skills/implement/SKILL.md`, `SKILL.jp.md` |
| 済 | `flocss-apply/` スキル削除 | - `plugins/ui-kit/skills/flocss-apply/`(削除) |
| 済 | spec ui-kit-design.md から flocss-apply を削除し implement に統合された旨を記載 | - `.work/specs/ui-kit-design.md` |
| 済 | mock スキルから flocss-apply 参照を implement へ修正 | - `plugins/ui-kit/skills/mock/SKILL.md`, `SKILL.jp.md` |
| 済 | ui-design.md の「共通コンポーネント一覧」に Header / Button / FAB を明示し、運用ガイド(「よく使うものはここに集約」)を追加 | - `plugins/ui-kit/references/ui-design.md`, `ui-design.jp.md` |
| 済 | spec ui-kit-design.md を最終構成に更新 | - `.work/specs/ui-kit-design.md` |
| 済 | 「URL クエリストリングで画面状態反映」必須ルールを principles.md / ui-design.md に追加 | - `plugins/ui-kit/references/principles.md`, `principles.jp.md`, `ui-design.md`, `ui-design.jp.md` |
| 済 | debug-fab に要素ピッカー機能追加(クリックした要素の XPath + URL を JSON コピー、XPath フル/短縮を設定で切替) | - `plugins/ui-kit/skills/debug-fab/templates/uidev.css`, `uidev.js`, `CLAUDE.md`, `CLAUDE.jp.md`, `SKILL.md`, `SKILL.jp.md` |
| 済 | debug-fab の files カテゴリを `html`/`css`/`js` のみに簡略化(backend/other は JS から辿れるため削除) | - `plugins/ui-kit/skills/debug-fab/templates/*`, `SKILL.md`, `SKILL.jp.md` |
| 済 | 要素ピッカーを多選択 + コピーペイロード共通化に変更(elements 配列を通常コピーに合流。XPath は short 固定) | - `plugins/ui-kit/skills/debug-fab/templates/uidev.css`, `uidev.js`, `CLAUDE.md`, `CLAUDE.jp.md`, `SKILL.md`, `SKILL.jp.md` |
| 済 | ルール・CLAUDE.md を整備する | - `CLAUDE.md`, `CLAUDE.jp.md`(必要に応じて) |

## 参考ドキュメント

- `.work/specs/ui-kit-design.md`: ui-kit 設計仕様(本 PR で作成)
- `.work/specs/dev-kit-design.md`: dev-kit 設計仕様(本 PR で更新)
