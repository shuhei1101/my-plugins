# html-kitスキル群 — dev-kit の HTML/UI 系スキル群と規約

## 概要

`dev-kit` の `html-*` スキル群（PC 専用 — レスポンシブ／メディアクエリ／モバイルドロワーは生成しない）。開発支援画面向けの UI 規約（FLOCSS + Design Tokens、JS 規約）と、mock / implement / logging の各スキルを提供する。

## 対象スコープ

- 開発支援画面（管理パネル・内部ツール・デバッグページ）向け。
- PC 版のみをターゲット。ブレイクポイント・メディアクエリ・モバイル用ドロワーは生成しない。

## CSS アーキテクチャ（FLOCSS + Design Tokens）

| レイヤー | プレフィックス | 内容 |
|---|---|---|
| Foundation | (なし) | リセット + Design Tokens（`:root` の CSS Custom Properties） |
| Layout | `l-` | ページレイアウト・グリッド |
| Object — Component | `c-` | 再利用可能な小コンポーネント |
| Object — Project | `p-` | プロジェクト固有コンポーネント |
| Object — Utility | `u-` | 単機能ユーティリティ |

- 各コンポーネント内部は BEM 風（`c-button__icon--large`）。

## JS 規約

- 全ファイル先頭に `// @ts-check` + JSDoc 型注釈。
- HTML へのインラインスクリプト禁止。
- UI 層 / 状態層 / API 層を明確に分割。バックエンド通信は `api/` レイヤーへ。
- 関数型寄り（クラスではなく関数 + クロージャ）。
- CSS クラス名 ↔ JS の DOM アクセスは紐付けルールで監査。
- UI 設計判断は例外なく `frontend-design` スキルを使う。

## レイアウト原則

- サイドバーは常時表示（固定）。
- 2 ペイン（一覧 + 詳細）は PC の横並び表示のみ。
- トースト通知は右下固定。
- 一覧画面のアクションボタンはリスト上部右。

## スキル

### html-mock

単一画面タイプの複数デザイン案を上部タブ切替で単一 HTML に並べる。

- 各案は意味のあるデザイン軸（レイアウト・密度・ナビゲーション等）で差をつける（色違いだけは NG）。
- 出力先: サーバーあり → テンプレートディレクトリ（起動済みポート使用、または空きポートで起動）／サーバーなし → `tmp/mocks/` + `python -m http.server {空きポート}`。
- 生成後は必ずブラウザで即開ける URL をユーザーに通知する（ファイルパスだけ伝えない）。

### html-implement

UI 画面実装のエントリポイント。

1. 共通リソース（constants / routes / `c-*` / `p-*` / api/）の棚卸し（なければ空スキャフォールド作成）
2. FLOCSS + Design Tokens セットアップ
3. 再利用 / 拡張 / 新規追加の振り分け
4. JSDoc 型を先に書く（契約先行）
5. 実装
6. `.claude/rules/` にルールテンプレ導入

### html-logging

ログ整備規約スキル。

- JSON Lines 形式（必須フィールド: `ts` / `level` / `msg`）。
- レベル別: `debug`（開発時の詳細トレース）／ `info`（通常運用・ユーザー操作・状態遷移）／ `warn`（回復可能な異常・リトライ・フォールバック）／ `error`（要対応の失敗）／ `critical`（回復不能な障害）。
- 本番デフォルトレベルは `error`、開発時は `debug` に切替可能。

## 参考ドキュメント

- `plugins/dev-kit/skills/html-mock/SKILL.md` / `html-implement/SKILL.md` / `html-logging/SKILL.md`: 各スキル本体
- `debug-fabスキル.md`: 同じ html 系のフロートデバッグボタン

## 変更履歴

| # | 日付 | 変更内容 | 関連タスク |
|---|---|---|---|
| 1 | 260531 | 新規作成（specsから統合） | 260531_notes-spec-and-ref-inject |
