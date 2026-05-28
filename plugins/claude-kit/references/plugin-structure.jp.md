<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# プラグイン作成ガイド

Claude Code プラグインを作成または更新する方法。本ガイドは自己完結している: （`plugin.json` または
`marketplace.json` を編集しているため）注入されたら、これに従って変更を直接執筆すること。
`common.md` を併読すること。
英語原本: `references/plugin-structure.md`

---

## 標準ディレクトリ構成

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (required)
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md         # Skill definition (English, auto-loaded)
│       └── SKILL.jp.md      # Japanese mirror (reference only)
├── agents/
│   └── <agent-name>.md      # Agent definitions (optional)
├── hooks/
│   └── hooks.json           # Hook configuration (optional)
├── references/              # Shared reference docs (optional)
│   └── <topic>.md
├── .mcp.json                # MCP server config (optional)
└── changelogs/              # Version history (required)
    ├── v1.0.0.md            # Initial release
    └── v1.1.0.md            # Subsequent versions
```

---

## 作成ワークフロー

### ステップ 1 — モードを判定する: 作成か更新か

- **モード**: 新規プラグインか、既存プラグインの更新か？
- **プラグイン名**: kebab-case（例: `code-reviewer`, `claude-kit`）
- **更新の場合**: 現在のバージョンを既存の `plugins/<name>/.claude-plugin/plugin.json` で読む。

### ステップ 2 — 変更内容を集める

**作成**: 説明（1 行）、含めるスキル（名前 + 目的、最低 1 つ）、その他のコンポーネント（agents/hooks/MCP）。

**更新**: 何が変わったか（スキルの追加/変更/削除、構造変更、修正）、およびバージョンバンプを
決定するための**変更種別**。

### ステップ 3 — ファイル変更を適用する

- **作成**: 上記のディレクトリ構成を生成する。agents/hooks/MCP ディレクトリは要求された場合のみ追加する。
- **更新**: 変更したファイルだけを編集する。無関係なファイルには触れない。

### ステップ 4 — plugin.json + marketplace.json + changelog（バージョンを一致させる）

下記のフィールド/形式/バージョンのセクションを参照。**`plugin.json` のバージョン、
`.claude-plugin/marketplace.json` のエントリ、changelog のファイル名（`changelogs/v{X.Y.Z}.md`）は
常に一致していなければならない。** この 3 つを決して乖離させないこと。

> 2 つの並行 PR が同じプラグインをバンプし、一方が先にマージされたら、マージ前にもう一方を
> ブランチ上で次のバージョンに再バンプすること（incident `parallel-pr-version-bump-collision`）。

### ステップ 5 — 報告する

モード（作成/更新）、新バージョン、変更ファイル、ローカルでのテスト方法を報告する:

```bash
claude --plugin-dir ./plugins/<plugin-name>
/<skill-name>
```

---

## plugin.json のフィールド

| フィールド | 必須 | 説明 |
|---|---|---|
| `name` | はい | プラグイン識別子（kebab-case）。スキルの名前空間として使われる。 |
| `description` | はい | プラグインの説明 |
| `version` | はい | セマンティックバージョニング（例: `1.0.0`） |
| `author` | いいえ | 作者情報 |

```json
{
  "name": "<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

---

## marketplace.json のエントリ

`.claude-plugin/marketplace.json` の `plugins` 配列に追加する:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

---

## バージョンバンプのルール

| 変更種別 | バンプ |
|---|---|
| バグ修正 / 軽微な修正 | PATCH（`1.x.y` → `1.x.y+1`） |
| 新スキルや挙動変更 | MINOR（`1.x.0` → `1.x+1.0`） |
| 全面的な再設計 | MAJOR（`1.0.0` → `2.0.0`） |

---

## changelog ファイルの形式

ファイル: `changelogs/v{X.Y.Z}.md` — **`plugin.json` と同じバージョン**。

```markdown
# v{X.Y.Z} — {YYYY-MM-DD}

## 変更内容

- {変更点}

## 構造の変更

{ディレクトリ構造や設定ファイルの変更があれば記載。なければ「なし」と書く。}
```

「構造の変更」セクションは重要 — このプラグインに依存する他プロジェクトに、自分側で適用すべき
構造的な更新を知らせるためのもの。

---

## 環境変数

プラグインのフック/スクリプトは、`settings.json` の `env` ブロックで設定し `os.environ` で読む
環境変数によって設定可能にできる（詳細は `environment.md`）。プラグインが env 変数を読む場合は、
**そのプラグイン自身の `CLAUDE.md` に記載する**（名前・効果・デフォルト） — ソースを読まずとも何が
設定可能か分かるように。キーはプラグイン名で名前空間化する（例: `PY_KIT_INJECTION_TTL`）。
