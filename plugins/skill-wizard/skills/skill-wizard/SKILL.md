---
name: skill-wizard
description: 対話形式（ステップ駆動型）および単発スキルを新規作成・編集するスキル。「対話スキルを作りたい」「ワークフロースキルを作りたい」「ステップ形式のスキルを作って」「スキルを作りたい」「既存のスキルを編集したい」「XXXのスキルのYYYを修正して」「file-summaryのdescriptionを変更して」「ideaスキルのステップ2.1を追加して」「フロー型スキルを設計して」といったリクエストで起動する。単発スキルの場合は `/skill-creator` に移譲し、対話形式スキルの場合はユーザーとの対話を通じてステップ構成を設計し、各ステップの詳細（条件・入力・AIタスク・出力・選択肢）を段階的に確定してSKILL.mdを出力する。スキル名と修正内容が直接指定された場合は、メインメニューをスキップして編集フローに直接入る。
---

# Skill Wizard — スキルウィザード

## このスキルについて

対話形式（ステップ駆動型）スキルおよび単発スキルを設計・生成するスキル。

- **対話形式スキル**: ユーザーとの対話を通じてステップを一つずつ練り上げ、最終的にSKILL.mdとして出力する
- **単発スキル**: `/skill-creator` に移譲し、効率的にスキルを作成する（ideaスキルのような1回のリクエストで完結するスキル）

新規作成と既存スキルの編集の両方に対応する。

---

## 対話形式スキルの前提知識

以下の内容は参照ドキュメントを参照すること：

### `references/workflow_guide.md`
- 基本原則
- ステップの構造テンプレート
- デフォルト選択肢
- 選択肢の提示形式
- 多角度質問の提示形式
- サブエージェント実行オプション
- ペルソナの活用（多角的な案出し）
- フロー制御

### `references/file_organization.md`
- ファイル配置ガイドライン
- scripts/ / references/ / examples/ の使い分け
- Progressive Disclosure（段階的な情報開示）

---

## 作業フロー

以下はこのスキル（skill-wizard）自体のワークフローである。各フェーズの詳細は必ず対応するファイルを読み込むこと。

### フェーズ1: 事前準備（スキル起動時、概要未確定時、編集対象未選択時）

📁 **必読**: `references/phases/00_prep.md`

**含まれるステップ**:
- ステップ1.1: メインメニュー（新規作成・編集・テストの選択）
- ステップ1.2: ランダムスキル案生成
- ステップ1.3: スキルタイプの確認（対話形式 or 単発）
- ステップ1.4: skill-creatorへの移譲（単発スキルの場合）
- ステップ1.5: 単発スキル微調整
- ステップ1.6: 改善項目選択
- ステップ1.7: 参考情報の収集

**重要タスク**:
- スキル作成セッション開始時に `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_skill_creation.md` を作成
- スキル情報（概要、タイプ、参考情報）を記録

---

### フェーズ2: メインフェーズ（対話形式スキルの詳細設計）

📁 **必読**: `references/phases/01_main.md`

**含まれるステップ**:
- ステップ2.1: スキル概要の理解とスキル名提案
- ステップ2.1b: メニュー構成案の提案（AI追加機能レコメンド付き）
- ステップ2.2: 質問ステップ（選択肢なし）
- ステップ2.3: 回答漏れの再確認
- ステップ2.4: 追加コンテキスト確認
- ステップ2.5: ステップ一覧の提案
- ステップ2.6: ステップ内容の詳細設計（ループ）
- ステップ2.7: ステップ一覧表示

**重要タスク**:
- `/idea` を積極的に活用（スキル名案、質問生成、改善案など）
- `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_skill_creation.md` に重要な決定事項を記録（スキル名候補、質問事項、ステップ構成案、詳細設計済みステップ）
- 案検討・機能設計段階では追加の `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_{内容}.md` を作成

---

### フェーズ3: 全ステップ確認完了後（関連ファイル整理、構造チェック、出力）

📁 **必読**: `references/phases/02_post.md`

**含まれるステップ**:
- ステップ3.1: 関連ファイルの確認
- ステップ3.2: 構造チェックと最適化（行数、重複、description形式）
- ステップ3.3: 出力先確認
- ステップ3.4: SKILL.md出力

**重要タスク**:
- 500行超過時の分離提案
- 出力完了時に `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_skill_creation.md` を更新（完了情報、出力パス、最終スキル情報）

---

### フェーズ4: 既存スキル編集フロー（編集モードで起動時）

📁 **必読**: `references/phases/03_edit.md`

**含まれるステップ**:
- ステップ4.1: 編集対象の特定
- ステップ4.2: ステップ編集
- ステップ4.3: 編集内容の確認
- ステップ4.4: SKILL.md更新

**重要タスク**:
- 編集セッション開始時に `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_skill_edit.md` を作成
- 変更内容を詳細に記録

---

### フェーズ5: テストフェーズ（構造チェック・テストモードで起動時）

📁 **必読**: `references/phases/04_test.md`

**含まれるステップ**:
- ステップ5.1: 構造チェック
- ステップ5.2: テストケース生成
- ステップ5.3: テスト実行と結果確認

**重要タスク**:
- テスト実行時に `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_test_run.md` を作成
- テスト結果を詳細に記録

---

### フェーズ6: カスタムサブエージェント管理フェーズ

📁 **必読**: `references/phases/05_agents.md`  
📁 **補足**: `references/custom_agents_guide.md`（エージェントの書き方ガイド）

**起動条件**:
- メインメニューで選択肢5「スキルのカスタムサブエージェントを調整する」が選択された場合
- ステップ2.6bから「エージェントを新規作成/紐づける」が選択された場合

**含まれるステップ**:
- ステップ6.1: カスタムサブエージェント管理（対象スキルと既存エージェントの確認）
- ステップ6.2: エージェント詳細設計（新規作成 or 編集）
- ステップ6.3: エージェントファイル出力 & タスク紐づけ

**重要タスク**:
- 対象スキルの `agents/` フォルダを確認・作成
- エージェントファイルにフロントマターを必ず記述（将来の正式エージェント格上げに備えて）
- `/idea` の `agents/` 構造（`idea:cost-conscious` 等）を参考にする
- 管理セッション開始時に `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_agent_management.md` を作成

---

## Memory活用ルール

スキル作成中の重要な情報は `~/.claude/skill-memory/skill-wizard/` に保存すること。
pluginはインストール/アンインストールされるため、スキル配下ではなくホームディレクトリ配下に保存する。

### 保存先
`~/.claude/skill-memory/{スキル名}/` — スキル名ごとにディレクトリを分ける。
ディレクトリが存在しない場合は自動作成すること。

### ディレクトリ構造
用途に応じてサブフォルダを作成する:
- `history/` — セッション履歴（作成・編集・テスト・エージェント管理の記録）
- 必要に応じて他のフォルダを追加（例: `config/` でユーザー設定、`templates/` でカスタムテンプレートなど）

```
~/.claude/skill-memory/{スキル名}/
├── history/                    # セッション履歴
│   ├── {YYYYMMDDHHMMSS}_skill_creation.md
│   ├── {YYYYMMDDHHMMSS}_skill_edit.md
│   └── ...
└── {その他必要なフォルダ}/      # スキルが記憶しておきたい情報
```

### セッション管理（history/）
- **スキル作成**: `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_skill_creation.md`（セッション開始〜完了まで）
- **スキル編集**: `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_skill_edit.md`
- **テスト実行**: `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_test_run.md`
- **エージェント管理**: `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_agent_management.md`

### 重要な決定事項の記録
案検討・機能設計など重要な段階では追加のmemoryファイルをhistory/に作成：
- `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_feature_design.md`（機能設計）
- `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_architecture_ideas.md`（アーキテクチャ案）
- `~/.claude/skill-memory/skill-wizard/history/{YYYYMMDDHHMMSS}_{作業内容の概要}.md`（その他重要な決定）

**圧縮コマンドやセッション中断に備え、大事な内容だけを記録すること。**

---

## 設計思想

詳細は `references/design_philosophy.md` を参照。
