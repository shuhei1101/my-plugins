---
name: idea
description: Generate diverse perspectives on any topic using persona-based subagents. Use when users ask for opinions, ideas, evaluations, or multiple viewpoints on a topic. Trigger for ANY request that mentions perspectives, viewpoints, opinions, evaluations, reviews, alternatives, or asks for input from different angles. Also use when users mention specific persona categories like implementation, documentation, project management, code review, naming decisions, or AI development (model selection, cost, accuracy, inference, OpenAI updates, AI libraries). Also trigger when invoked with no arguments to show the agent menu. 「案だして」「意見考えて」「XXXの観点から評価して」「複数の視点で意見出して」「実装の観点から評価して」「命名候補を出して」「レビューして」「モデル選定して」「AIコスト比較して」「推論モード教えて」「OpenAI最新情報」「エージェント一覧」といった依頼で起動。引数なしで起動した場合はメニューを表示する。
---

# Idea — 多視点意見ジェネレーター

複数のペルソナをサブエージェントとして並列起動し、あらゆるトピックについて多角的な意見・評価・アイデアを生成するスキル。異なる視点からの意見を一覧にまとめ、より良い意思決定をサポートする。

## 動作の流れ

1. **入力受付** — トピック（必須）と観点カテゴリ（任意）を受け取る
2. **ペルソナ選択** — カテゴリに対応するペルソナを選択。未指定の場合は自動選択
3. **サブエージェント起動** — 各ペルソナを並列サブエージェントとして起動
4. **結果統合** — 全意見を表形式にまとめて提示

## 入力形式

- **トピック**（必須）: 意見を求めるテーマや内容
- **観点**（任意）: `implementation`・`docs`・`project`・`review`・`naming` から1つ以上
  - 未指定の場合、トピックの性質から最適な観点を2〜3個自動選択する
  - トピックが曖昧な場合は、具体的な内容を確認してから進む
- **ペルソナ選択モード**（任意）: `auto` / `manual` / `hybrid`
  - `auto`（デフォルト）: トピックに応じて自動選択
  - `manual`: ユーザー指定の観点・ペルソナのみ使用
  - `hybrid`: 指定分を優先しつつ不足分を自動補完
- **ペルソナ数**（任意）: 推奨 `3〜8`（デフォルト `4`）
  - 未指定時は `4`
  - 明示指定がある場合はその値を優先（極端値は実用範囲に丸めて提案）
- **モデル方針**（任意）: `current` / `platform-auto` / `random`（利用可能時）
  - `current`（デフォルト）: 現在の実行モデルを使用
  - `platform-auto`: 実行環境にモデル選択を委ねる
  - `random`: 実行環境がサブエージェントごとのモデル指定に対応している場合のみ有効
  - モデル指定ができない環境では `current` にフォールバックし、その旨を明示して続行

## 出力形式

結果は以下の表形式で提示する:

| 観点         | 意見       | 理由       |
| ------------ | ---------- | ---------- |
| [ペルソナ名] | [その意見] | [その根拠] |
| [ペルソナ名] | [その意見] | [その根拠] |

ユーザーが希望する場合は、詳細レポート形式や箇条書き形式にも対応する。

## エントリーポイント（引数なし・メニューモード）

トピックや観点が指定されていない状態で起動した場合、以下のメニューを表示する:

```
💡 Idea — 何をしますか？

1. トピックを入力して多視点意見を出す
2. 特定のエージェントと会話する（エージェント名を指定）
3. エージェント一覧を見る
4. エージェントを追加・調整する → /skill-wizard へ
5. その他（入力してください）
```

- **選択肢2**: エージェント名（例: `cost-conscious`、`model-selection`）を指定してもらい、そのエージェントを単体で会話モードで起動する。1対1の会話として機能し、ユーザーが「終了」と言うまで継続する
- **選択肢3**: 下記のエージェント一覧テーブルを表示する
- **選択肢4**: `/skill-wizard` スキルを起動し、カスタムサブエージェントの追加・調整フローへ移行する

---

## 使用可能なエージェント一覧

エージェントファイルは `agents/` フォルダにカテゴリ別で格納。サブエージェント起動時は対応する `.md` を読み込んで使用すること。

### agents/implementation/（実装系）

| エージェント名 | 概要 | パス |
|---|---|---|
| コスト重視 | 開発・運用コストの最小化、ROI優先 | `agents/implementation/cost-conscious.md` |
| 品質重視 | コード品質・保守性・拡張性の優先 | `agents/implementation/quality-first.md` |
| 工数最小 | 最短実装パス・MVP思考 | `agents/implementation/minimum-effort.md` |
| セキュリティ重視 | 脆弱性・リスク管理の優先 | `agents/implementation/security-first.md` |

### agents/docs/（ドキュメント系）

| エージェント名 | 概要 | パス |
|---|---|---|
| 作成者目線 | 網羅的・論理的な情報整理 | `agents/docs/author-perspective.md` |
| 初見読者目線 | わかりやすさ・親しみやすさ重視 | `agents/docs/first-time-reader.md` |
| 保守者目線 | 更新しやすさ・長期維持管理 | `agents/docs/maintainer-perspective.md` |

### agents/project/（プロジェクト系）

| エージェント名 | 概要 | パス |
|---|---|---|
| PL目線 | 全体最適・リスク管理・ステークホルダー調整 | `agents/project/project-leader.md` |
| 実装者目線 | 実現可能性・技術的課題・現実的工数 | `agents/project/implementer-perspective.md` |
| 新規参画者目線 | オンボーディング・知識共有のしやすさ | `agents/project/new-team-member.md` |

### agents/review/（レビュー系）

| エージェント名 | 概要 | パス |
|---|---|---|
| デバッガー | エッジケース・例外処理・バグ検出 | `agents/review/debugger.md` |
| パフォーマンス重視 | 速度・メモリ・スケーラビリティ | `agents/review/performance-enthusiast.md` |
| UX重視 | 使いやすさ・直感性・ユーザー満足度 | `agents/review/ux-focused.md` |

### agents/naming/（命名系）

| エージェント名 | 概要 | パス |
|---|---|---|
| キャッチー重視 | 記憶に残る・印象的な名前 | `agents/naming/catchy-focus.md` |
| シンプル重視 | 短くて簡潔（1〜2単語） | `agents/naming/simplicity-focus.md` |
| 機能明瞭 | 名前から機能が伝わる | `agents/naming/function-clarity.md` |
| 検索性重視 | ユニークで検索しやすい | `agents/naming/searchability-focus.md` |

### agents/ai-dev/（AI開発特化）

> 最新情報取得にはContext7 MCPまたはWebFetchを使用すること。各エージェントに関連リンク一覧あり。

| エージェント名 | 概要 | パス |
|---|---|---|
| モデル選定 | 用途・精度・コストからモデルを比較・推薦 | `agents/ai-dev/model-selection.md` |
| コスト視点 | トークン単価・コスト削減策・試算 | `agents/ai-dev/cost-perspective.md` |
| 精度視点 | プロンプト・RAG・FT・評価手法のTips | `agents/ai-dev/accuracy-perspective.md` |
| 推論重視 | reasoning_effort・extended thinkingの使い分け | `agents/ai-dev/inference-perspective.md` |
| 外部ライブラリ | LangChain・LlamaIndex・Ollama・Whisper・CLIP等 | `agents/ai-dev/external-libraries.md` |
| OpenAI最新情報 | 最新モデル・API機能を公式リンクから取得 | `agents/ai-dev/openai-latest.md` |

---

## 実行ワークフロー

### Step 1: 入力のパース

ユーザーのリクエストからトピック・観点カテゴリ・ペルソナ数・モデル方針を抽出する:

- **引数なし / トピック未指定** → エントリーポイントのメニューを表示する
- 「案だして」→ 観点を自動選択
- 「実装の観点から意見出して」→ `implementation` を使用
- 「ドキュメントとプロジェクトの視点で評価して」→ `docs` + `project` を使用
- 「モデル選定したい」「コスト比較して」「推論モード教えて」→ `ai-dev` を使用
- トピックが曖昧・不明確な場合は、具体的な内容をユーザーに確認してから進む

抽出できなかったオプションは以下をデフォルト適用:
- ペルソナ選択モード: `auto`
- ペルソナ数: `4`
- モデル方針: `current`

### Step 2: ペルソナの選択

指定された（または自動選択された）カテゴリごとに、要求されたペルソナ数に合わせてペルソナを選択する。同一カテゴリ内でも多様性を意識して選ぶ。

**自動選択ロジック**（カテゴリ未指定の場合）:
- 技術的なトピック: `implementation` + `review`
- ドキュメント関連: `docs`
- プロジェクト計画: `project` + `implementation`
- 命名・名前決め: `naming`
- AIモデル・API・ライブラリ関連: `ai-dev`
- 多岐にわたるトピック: 最適な2〜3カテゴリを選択

**件数調整ルール**:
- デフォルト件数は `4`
- 速さ重視は `3〜4`、深掘りは `6〜8`
- ユーザーが件数を指定した場合はそれを優先

### Step 2.5: モデル方針の適用

モデル方針オプションを解釈し、サブエージェント実行設定に反映する。

- `current`: 現在の実行モデルで統一
- `platform-auto`: 実行環境が自動で選択
- `random`: サブエージェントごとのモデル指定が可能な実行環境でのみ適用

**フォールバック**:
- サブエージェントのモデル指定ができない実行環境では、`current` に自動フォールバックする
- このときユーザーには「モデルは環境制約により固定、代替としてペルソナ/観点のランダム化は可能」と明示する

### Step 3: サブエージェントの起動

選択した各ペルソナに対して、対応する `agents/*.md` ファイルを読み込み、以下の形式でサブエージェントを起動する:

```
agents/{persona-slug}.md を読み込み、そのペルソナとして以下のトピックを評価してください: [トピック]

ファイルに記載された「コアバリュー」「推論スタイル」「回答形式」に従って回答すること。
具体的かつ実践的に。一般論は避けること。
```

エージェントファイルが読めない環境では、`references/personas.md` の定義を直接プロンプトに組み込む従来の形式にフォールバックする。

**重要**: 全サブエージェントを同じターンで並列起動すること。1つが終わるまで待たない。

### Step 4: 結果の統合と提示

全サブエージェントの完了後:
1. 各サブエージェントの回答を読み取る
2. 意見と根拠を抽出する
3. 上記の表形式にまとめる
4. ユーザーに提示する

## Tips

- **トピックは具体的に**: 「この新機能の実装方針」の方が「意見ください」より良い結果になる
- **カテゴリは適切に**: 命名の議論に `naming` 以外は使わない
- **ペルソナ数の調整**: 素早いフィードバックなら3〜4体、徹底的な分析なら6〜8体
- **具体的な根拠を促す**: ペルソナは一般論ではなく、具体的な考慮事項を挙げること

## 柔軟な対応

- 標準リストにない観点をユーザーが求めた場合、アドホックなペルソナを追加する
- トピックの複雑さに応じてカテゴリを自由に組み合わせる
- 出力形式はユーザーの要望に応じて変更できる（例: 詳細レポート形式、箇条書き形式）
- モデル指定が制限される環境では、代替として「観点ランダム化」「ペルソナランダム化」「件数調整」で多様性を確保する

## 使用例

**例1: 自動選択**
ユーザー: 「この機能追加の案、評価して」
→ `implementation` + `review` を選択し、4〜6体のペルソナを起動して表を提示

**例2: カテゴリ指定**
ユーザー: 「実装の観点から、この設計について意見だして」
→ `implementation` カテゴリを使用し、3〜4体の実装系ペルソナを起動

**例3: 複数カテゴリ**
ユーザー: 「プロジェクトとドキュメントの視点で、この仕様書をレビューして」
→ `project` + `docs` を使用し、合計4〜6体を起動

**例4: 命名**
ユーザー: 「このスキルの名前、いくつか候補考えて」
→ `naming` カテゴリを使用し、命名系ペルソナを全体起動
