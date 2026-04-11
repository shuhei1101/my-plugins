# エージェントファイル仕様

Claude Code のカスタムエージェント（`.md` ファイル）のフロントマターとボディの仕様一覧。

---

## フロントマター

YAML形式で `---` で囲んで記述する。

### 必須フィールド

| フィールド | 型 | 説明 |
|---|---|---|
| `name` | string | エージェントの一意識別子。kebab-case（例: `cost-conscious`） |
| `description` | string | エージェントの説明。**最重要フィールド**。Claude Code はこの内容を見て呼び出しを判断する。「いつ使うか」を明確に含めること |

### オプションフィールド

| フィールド | 型 | 説明 | 例 |
|---|---|---|---|
| `model` | string | 使用モデル。短縮形OK | `haiku`, `sonnet`, `opus` |
| `tools` | string[] | 許可するツール一覧 | `["Read", "Edit", "Glob"]` |
| `disallowedTools` | string[] | 禁止するツール。パターン指定可 | `["Bash(rm)", "Bash(DROP)"]` |
| `permissionMode` | string | 権限プロンプト処理方法 | `auto`, `plan`, `dontAsk`, `bypassPermissions` |
| `effort` | string | 推論の深さ | `minimal`, `balanced`, `max` |
| `maxTurns` | number | 最大実行ターン数 | `10` |
| `color` | string | UI上の識別色 | `blue`, `green`, `red` |
| `skills` | string[] | エージェントに与えるスキル | スキルファイルへのパス |

### プラグイン内エージェントの制限

プラグイン内（`plugin/agents/`）では以下のフィールドはセキュリティ上**無視される**:
- `hooks`
- `mcpServers`
- `permissionMode`

---

## モデル選択ガイド

| タスクの種類 | 推奨モデル | 理由 |
|---|---|---|
| 意見生成・ペルソナ | `haiku` | 軽量・高速。トークンコスト最小 |
| 分析・評価・採点 | `sonnet` | 高精度。コスト/品質のバランス良 |
| 調査型（WebFetch利用） | `sonnet` | ツール利用+判断が必要 |
| 複雑な設計・アーキテクチャ | `opus` | 最高品質の推論 |
| タスク実行（ファイル操作） | `sonnet` | ツール操作の安定性 |

---

## tools よく使う組み合わせ

| エージェントタイプ | tools |
|---|---|
| ペルソナ型（意見生成のみ） | なし（省略） |
| 調査型（外部情報参照） | `WebFetch`, `WebSearch` |
| タスク実行型 | `Bash`, `Read`, `Edit`, `Glob`, `Grep` |
| 分析型（ファイル読み取り） | `Read`, `Glob`, `Grep` |
| フルアクセス | 省略（全ツール使用可能） |

---

## ボディ構成パターン

### ペルソナ型（意見生成）

```markdown
# {ペルソナ名}

あなたは{役割}です。{最優先事項}を最優先します。

## コアバリュー
- ...

## 推論スタイル
- ...

## 典型的な懸念
- ...

## 回答形式
1. 意見（1〜2文）
2. 根拠（2〜3文）
```

### 調査型（外部情報参照）

```markdown
# {エージェント名}

あなたは{役割}です。最新情報はWebFetchで関連リンクを確認してから回答すること。

## 関連リンク一覧
- 公式ドキュメント: https://...
- リリースノート: https://...
- 料金ページ: https://...

## 熟知している知識
- ...

## 推論スタイル
- 回答前に必ず関連リンクをWebFetchで確認する
- ...

## 回答形式
1. 最新情報（WebFetch結果反映）
2. 推奨アクション
3. 参照したURL
```

### 分析型（採点・評価）

```markdown
# {エージェント名}

あなたは{役割}です。

## 入力
- ...

## プロセス
1. ...
2. ...
3. ...

## 出力形式
- 評価結果
- 証拠
- pass/fail
```

---

## description のベストプラクティス

description はエージェントのトリガー精度に直結する最重要フィールド。

**良い例**:
```
Use this agent for comprehensive code reviews, security audits, and performance analysis. Trigger when the user asks to review code, check for bugs, improve quality, or audit for security issues.
```

**悪い例**:
```
A helpful code review agent
```

**ポイント**:
- 何ができるかを具体的に書く
- いつ使うべきかを明示する（"Use when...", "Trigger when..."）
- 曖昧すぎると呼ばれない、広すぎると誤爆する

---

## 配置場所とスコープ

| スコープ | パス | 共有範囲 | 名前空間 |
|---|---|---|---|
| ユーザーレベル | `~/.claude/agents/` | 全プロジェクト（個人用） | プレフィックスなし |
| プロジェクトレベル | `.claude/agents/` | プロジェクト内 | プレフィックスなし |
| プラグイン内 | `plugin/agents/` | プラグイン利用者 | `plugin-name:agent-name` |

- サブフォルダ構成もサポートされる（自動探索）
- プロジェクトレベルはユーザーレベルをオーバーライドする
