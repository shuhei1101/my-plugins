# SKILL.jp.md — plugin-creator スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: plugin-creator
**トリガー**: ユーザーが「新しいプラグインを作りたい」「プラグインを作って」「create a plugin」「make a new plugin」「plugin-creator して」と言ったとき

---

## 概要

標準ディレクトリ構造（`changelogs/` バージョン管理フォルダ含む）を持つプラグインを新規作成するスキル。

---

## 参考資料

- プラグイン構造とバージョンルール: このプラグインの `references/plugin-structure.md`
- 公式プラグインドキュメント: https://code.claude.com/docs/ja/plugins

---

## 作業内容

### ステップ1: プラグイン情報を収集する

#### 条件

- 常に — 最初に実行する

#### 実行内容

ユーザーに以下を確認する:

1. **プラグイン名** — kebab-case（例: `code-reviewer`, `my-tool`）
2. **説明** — プラグインの概要を1行で
3. **含めるスキル** — 各スキルの名前と目的（最低1つ）
4. **その他コンポーネント** — エージェント・フック・MCP サーバーは必要か？（任意）

#### 出力

- プラグイン名・説明・スキル一覧・コンポーネント一覧を確定

---

### ステップ2: ディレクトリ構造を生成する

#### 条件

- ステップ1 完了後

#### 実行内容

1. このプラグインの `references/plugin-structure.md` を読んで標準レイアウトを確認する
2. 以下を作成する（ステップ1で選んだコンポーネントに応じて調整）:

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── <skill-name>/
│       └── SKILL.md
└── changelogs/
    └── v1.0.0.md
```

3. エージェント・フック・MCP が要求された場合は該当ディレクトリとスタブファイルも作成する

#### 出力

- `plugins/<plugin-name>/` 以下にディレクトリ構造が作成される

---

### ステップ3: plugin.json を作成する

#### 条件

- ステップ2 完了後

#### 実行内容

`plugins/<plugin-name>/.claude-plugin/plugin.json` を作成する:

```json
{
  "name": "<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

#### 出力

- `plugin.json` を書き込み

---

### ステップ4: 各スキルの SKILL.md を作成する

#### 条件

- ステップ3 完了後

#### 実行内容

ステップ1で確認した各スキルについて `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` を作成する。

ステップ構造を使う:
- フロントマター: `name`、`description`（自動起動条件）
- セクション: 概要 → 作業内容（各ステップ: 条件 / 実行内容 / 出力）

簡潔にまとめる — 各ステップは他のファイルを読まなくても実行できる内容にする。

#### 出力

- 各スキルの `SKILL.md` を作成

---

### ステップ5: 初回 changelog を作成する

#### 条件

- ステップ4 完了後

#### 実行内容

`plugins/<plugin-name>/changelogs/v1.0.0.md` を作成する:

```markdown
# v1.0.0 — {YYYY-MM-DD}

## 変更内容

- 初回リリース
- {追加したスキル名} スキルを追加

## 構造の変更

初回リリースのため、ディレクトリ構造全体が新規作成。

```
plugins/<plugin-name>/
├── .claude-plugin/plugin.json
├── skills/<skill-name>/SKILL.md
└── changelogs/v1.0.0.md
```
```

#### 注意事項

「構造の変更」セクションが changelog で最も重要な部分。
将来このプラグインの構造が変わったとき、依存する他プロジェクトがここを読んで何を更新すべきか判断できる。

#### 出力

- `changelogs/v1.0.0.md` を書き込み

---

### ステップ6: marketplace.json に登録する

#### 条件

- ステップ5 完了後

#### 実行内容

1. リポジトリルートの `.claude-plugin/marketplace.json` を読む
2. `plugins` 配列に新しいエントリを追加する:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

3. ファイルを保存する

#### 出力

- `.claude-plugin/marketplace.json` を更新

---

### ステップ7: 報告と次のステップ案内

#### 実行内容

作成内容を報告する:

- ディレクトリ構造の概要
- ファイル一覧とパス
- ローカルテスト方法:

```bash
# ローカルテスト
claude --plugin-dir ./plugins/<plugin-name>
/<skill-name>
```

- 今後プラグインを更新するたびに `plugin.json` のバージョンをバンプし、`changelogs/v{X.Y.Z}.md` を追加するようユーザーに伝える
