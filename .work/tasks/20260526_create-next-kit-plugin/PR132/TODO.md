# PR132 — create-next-kit-plugin

## 概要

Next.js 対応プラグイン next-kit を新規作成する。
現在フロントエンドはバニラ HTML を使用しているが、Next.js への移行計画があるため、
先行して実装規約・スキャフォールドスキルを整備する。
html-kit の後継として位置付け、Next.js 固有のパターンを対象にする。

**PR128 での設計決定事項**:
- next-kit: Next.js 実装規約・スキャフォールドを担当
- html-kit (ui-kit リネーム) とは別プラグインとして共存
- フロントエンド移行後に html-kit から next-kit に主軸を切り替える予定

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #128 | AIイシュー自動発見システム構想ノートの整備（プラグイン設計を確定） |
| #130 | ui-kit → html-kit リネーム（next-kit の前身整備） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260526_create-next-kit-plugin/PR132/QA.md` |
| 済 | plugins/next-kit/ を新規作成（plugin.json） | `plugins/next-kit/.claude-plugin/plugin.json` |
| 済 | Next.js 実装規約 references を作成 | `plugins/next-kit/references/` |
| 済 | 基本スキルを作成（implement） | `plugins/next-kit/skills/` |
| 済 | marketplace.json を更新 | `.claude-plugin/marketplace.json` |
| 済 | notes を更新する | `.work/notes/AIイシュー自動発見システム構想.md` |
| 済 | references/*.md の日本語ミラーを作成する | `plugins/next-kit/references/**/*.jp.md` |
| 済 | references をサブフォルダ分類に再構成（conventions/ ・ patterns/） | `plugins/next-kit/references/frontend/` |
| 済 | 編集/閲覧画面の命名規則を追加 | `plugins/next-kit/references/frontend/conventions/naming.md` |
| 済 | コメントの書き方ドキュメント追加 | `plugins/next-kit/references/frontend/conventions/comments.md` |
| 済 | 型定義パターンドキュメント追加 | `plugins/next-kit/references/frontend/conventions/types.md` |
| 済 | 使用ライブラリ一覧ドキュメント追加（Mantine / TanStack Query / Zod / react-hook-form / zustand / 他） | `plugins/next-kit/references/frontend/conventions/libraries.md` |
| 済 | 一覧画面パターン（フィルタ・ソート・QS） | `plugins/next-kit/references/frontend/patterns/list-screen.md` |
| 済 | 詳細・閲覧画面パターン | `plugins/next-kit/references/frontend/patterns/view-screen.md` |
| 済 | 編集画面パターン | `plugins/next-kit/references/frontend/patterns/edit-screen.md` |
| 済 | フォーム実装パターン（form.ts + Zod + react-hook-form + Mantine） | `plugins/next-kit/references/frontend/patterns/form.md` |
| 済 | ダイアログ・モーダルパターン | `plugins/next-kit/references/frontend/patterns/dialog.md` |
| 済 | URL ベースの画面状態管理（タブ・フィルタを QS に反映） | `plugins/next-kit/references/frontend/url-state.md` |
| 済 | components.md をカタログ形式に書き直し | `plugins/next-kit/references/frontend/components.md` |
| 済 | hooks.md を拡張（useQuery / useMutation / useXxxForm / フックの種類別パターン） | `plugins/next-kit/references/frontend/hooks.md` |
| 済 | state-management.md を拡張（zustand含む、エラー状態・ローディング統合の詳細） | `plugins/next-kit/references/frontend/state-management.md` |
| 済 | endpoints.md を見直し（オブジェクト形式の記述を実態確認） | `plugins/next-kit/references/frontend/endpoints.md` |
| 済 | environment.md を整理（YAML設定パターン追記、定数 vs 環境変数の判断基準） | `plugins/next-kit/references/shared/environment.md` |
| 済 | logger.md を JSON-L 形式に書き直し（aituberに合わせる） | `plugins/next-kit/references/shared/logger.md` |
| 済 | CLAUDE.md インデックスを新構成に合わせて更新 | `plugins/next-kit/references/CLAUDE.md` |
| 済 | 全 references の JP ミラー更新 | `plugins/next-kit/references/**/*.jp.md` |
| 済 | plugin.json / marketplace.json のバージョンを 1.1.0 にバンプ | `plugins/next-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | [id]/ 直下に page.tsx を置かないルールに変更（edit/ と view/ サブフォルダに） | `frontend/conventions/folder-structure.md`, `frontend/conventions/naming.md` |
| 済 | view-screen / edit-screen パターンを新フォルダ構造に対応 | `frontend/patterns/view-screen.md`, `frontend/patterns/edit-screen.md` |
| 済 | endpoints の URL 構造を更新（[id]/edit, [id]/view のルートに合わせる + オブジェクト形式案を検討） | `frontend/endpoints.md` |
| 済 | libraries.md のバージョン記述を削除（最新版を使う方針） | `frontend/conventions/libraries.md` |
| 済 | comments.md のルール変更：全フィールドコメント必須化、編集履歴コメント OK | `frontend/conventions/comments.md` |
| 済 | quest-pay / family / quest など特定ドメイン名を一般的なプレースホルダに置換 | `frontend/patterns/**.md`, `frontend/components.md`, `frontend/hooks.md`, `frontend/state-management.md`, `frontend/url-state.md` |
| 済 | 上記変更を JP ミラーにも反映 | `**/*.jp.md` |
| 済 | plugin.json / marketplace.json を 1.2.0 にバンプ | `plugins/next-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/AIイシュー自動発見システム構想.md`: next-kit 設計の背景

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| AIチューバー HTML→Next.js コンポーネント候補洗い出し | `/home/shuhei2441/repo/aituber` の各HTML画面を読み、共通化できそうな UI 部品を AI が洗い出して `next-kit/references/frontend/components.md` に追記する。ユーザーが採否を判断する流れ。 | PR132 完了後（next-kit の components.md が整備済みであること） |
| next-kit プラグイン自体のレビュー・改善提案 | Claude Code 一般のベストプラクティス知識で next-kit プラグインを評価し、改善提案を質問形式で QA.md に大量に書き出す。「このライブラリは別の方がいい」「この分割の方が保守性が高い」「この観点も書いた方がいい」等。ユーザーが一個ずつ判断して採用したものを実装。 | PR132 完了後（next-kit が一通り整備されていること） |
| next-kit に references 自動注入フックを追加 | 編集対象ファイルに応じて対応する references を Claude のコンテキストに自動注入する **PreToolUse** フックを `plugins/next-kit/hooks/` に追加。例: `form.ts` を Read/Edit/Write する直前に `references/frontend/patterns/form.md` を注入、`_hooks/use*.ts` には `references/frontend/hooks.md` を注入。UserPromptSubmit はプロンプトごとに毎回走ってしまうので不採用。`plugins/dev-kit/hooks/hooks.json` が設計の参考。ファイルパス → 注入する reference の対応表を設計し、`tool_input.file_path` の matcher 設計を行う。 | PR132 完了後（references が整備済みであること） |
