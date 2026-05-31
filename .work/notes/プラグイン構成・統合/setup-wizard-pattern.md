# setup-wizard パターン — プラグイン初回オンボーディングの規約

## 概要

各プラグインに「初回起動時にユーザーが必要な設定とユースケースを把握できる」入口を必須化するための規約。`plugin-update` と同様、claude-kit が定義する **必須スキル** の一つとして位置づける。

## 動機

- 各プラグインの env トグル・初期設定がドキュメント（CLAUDE.md）に分散していて、ユーザーが能動的に読まないと気づけない
- インストール直後に何ができるかを示すフロー（オンボーディング）が無く、最初の一歩が大きい
- `plugin-update`（バージョン追従）と対になる「セットアップ」の規約が欠けていた

## 設計の核

| 要素 | 決定 | 理由 |
|---|---|---|
| フラグ保存先 | `.claude/{plugin}.local.md` の YAML frontmatter（`setup_done: true`） | 既存の `plugin-settings` の仕組みを再利用。env 変数より隔離されて衛生的 |
|  | version 情報は持たせない | 規約で「プラグイン更新時に setup-wizard も更新」を必須化することで対応（QA-001 決定） |
| フックタイミング | `SessionStart`（プラグインごとに個別） | `UserPromptSubmit` より早い。プラグイン横断の中央集権化は避け、各プラグインが自身の状態を所有 |
| setup-wizard の責務 | ユースケース別オンボーディングの **目次** | 本文（使い方の詳細）は CLAUDE.md に書く。重複管理を避けるため目次役に徹する |
| env 設定 | 各プラグインが必須スキル `plugin-config` を持ち、setup-wizard はそれを呼ぶ | 単一プラグインで責務完結。`workspace:config` を共有しない（QA-002 決定） |
| AskUserQuestion | options は 2〜4（公式 schema 上限） | tool schema で `minItems: 2`, `maxItems: 4` を確認済。"Other" は自動付与 |

## フロー（標準）

1. SessionStart フックが `.claude/{plugin}.local.md` を読み、`setup_done: true` でなければ「setup-wizard を実行してください」というプロンプトを注入
2. setup-wizard 起動
   1. プラグイン概要を 1 行で提示
   2. **env / 初期設定**: AskUserQuestion で「すべて設定 / 必須のみ / スキップ（後で `/workspace:config`）」を提示
   3. **ユースケース紹介**: AskUserQuestion で「最初に試したいユースケース」を 2〜4 件提示 → 選んだものの簡単な解説 + CLAUDE.md へのリンク
   4. **完了処理**: `.claude/{plugin}.local.md` の frontmatter に `setup_done: true` を書き込む
3. 再セットアップは `/{plugin}:setup-wizard` を明示的に呼ぶ

## QA 決定事項

- QA-001: version 情報は持たせない（規約でカバー）
- QA-002: 各プラグインが独自 `plugin-config` を持つことを必須化

## 関連

- **次 PR**: AskUserQuestion 制約の汎用リファレンス化
- **次 PR**: `workspace:config` → `workspace:plugin-config` リネーム
- **次 PR**: 既存プラグインへの setup-wizard 遡及追加
