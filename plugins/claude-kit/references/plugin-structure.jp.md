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
├── CLAUDE.md                # Plugin developer guide (required)
├── CLAUDE.jp.md             # Japanese mirror (required)
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
└── .mcp.json                # MCP server config (optional)
```

---

## 必須スキル

### `plugin-update`（全プラグイン必須）

すべてのプラグインは、プロジェクトに展開したプラグイン生成物を現在インストール済みのプラグイン
バージョンに合わせて更新する `plugin-update` スキルを**必ず**同梱する。手動起動のみ
（`/<plugin>:plugin-update`）。

**理由**: プラグインがプロジェクトに静的テンプレ（`.work/CLAUDE.md`・フックプロンプト・サンプル
コンフィグ・`injection_rules.yaml` で注入する references など）を展開する場合、それらのコピーは
新バージョンが出るたびにプラグインソースに対して陳腐化していく。プラグイン専用の同期コマンドが
ないと、ユーザーは手で diff してコピーする羽目になる。各プラグインが自分の更新パスを持つのは、
プラグイン自身が自分のテンプレートと移行ルールを知っているから。

**標準仕様**:

| 項目 | 規約 |
|---|---|
| 名前 | `plugin-update`（kebab-case 固定 — `<plugin>-update` ではない） |
| トリガー | 手動のみ（`description` の自動トリガーなし。明示的に `/<plugin>:plugin-update`） |
| 最初の動作 | プロジェクトの PR ブランチ作成スキル（例: `/work:start`）を呼び、編集がレビュー可能なブランチに載るようにする |
| スコープ | このプラグイン自身の静的成果物のみ。他プラグインには絶対に手を出さない |
| 参考 | 標準的な実装例は `plugins/workspace/skills/plugin-update/SKILL.md` を参照 |

新規プラグインを作成するときは、workspace の実装を参考に `skills/plugin-update/SKILL.md`
（と `.jp.md`）を生成し、テンプレファイルのリストを自分のプラグインが展開する静的ファイルに
合わせて差し替える。

> **プラグインを更新するときは、必ず `setup-wizard` の内容も合わせて最新化すること**
> （ユースケース紹介・env 説明など）。`plugin-update` のチェックリストにも入れる。

### `setup-wizard`（全プラグイン必須）

すべてのプラグインは、初回利用時にユーザーをオンボーディングする `setup-wizard` スキルを**必ず**
同梱する。SessionStart フック + `.claude/{plugin}.local.md` の `setup_done` フラグで自動誘導し、
手動再実行は `/<plugin>:setup-wizard`。

**理由**: 各プラグインの env トグル・初期設定・ユースケースは `CLAUDE.md` に分散しており、
ユーザーが能動的に読まないと気づけない。初回起動時に対話的にセットアップとユースケース紹介を
提供することで、最初の一歩のコストを下げる。

**標準仕様**:

| 項目 | 規約 |
|---|---|
| 名前 | `setup-wizard`（kebab-case 固定 — `<plugin>-setup-wizard` ではない） |
| トリガー | 手動（`/<plugin>:setup-wizard`） + SessionStart フック自動誘導（フラグ未設定時のみ） |
| 完了マーク | `.claude/{plugin}.local.md` の YAML frontmatter に `setup_done: true` を書き込む |
| スコープ | このプラグイン自身の env / オンボーディングのみ。他プラグインには絶対に手を出さない |
| 関連スキル | env を持つなら `plugin-config` も必須実装（setup-wizard が委譲する） |
| 詳細ガイド | `references/setup-wizard.md`（フロー、skeleton、checklist） |

詳細な書き方・skeleton・SessionStart フックの実装は `setup-wizard.md` を参照。

### `plugin-config`（env を持つプラグインで必須）

プラグインが env 変数を持つ場合、ユーザーが `AskUserQuestion` で対話的に設定できる
`plugin-config` スキルを実装する。`setup-wizard` から委譲される。env を持たないプラグインでは
不要。

**標準仕様**:

| 項目 | 規約 |
|---|---|
| 名前 | `plugin-config`（kebab-case 固定 — `<plugin>-config` ではない） |
| トリガー | 手動（`/<plugin>:plugin-config`） + `setup-wizard` からの委譲呼び出し |
| スコープ | このプラグイン自身の env 変数のみ。他プラグインの env には絶対に触らない |

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
  `CLAUDE.md` と `CLAUDE.jp.md` は `plugin-claude-md.md` に従って作成する — 全プラグインで必須。
- **更新**: 変更したファイルだけを編集する。無関係なファイルには触れない。

### ステップ 4 — plugin.json + marketplace.json + changelog（バージョンを一致させる）

下記のフィールド/形式/バージョンのセクションを参照。**`plugin.json` のバージョン、
`.claude-plugin/marketplace.json` のエントリ、`CLAUDE.md` の `## Changelog` テーブルは
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

## Changelog

バージョン履歴はプラグインの `CLAUDE.md` 末尾の `## Changelog` テーブルに記録する
（`changelogs/` ディレクトリは使用しない）。バージョンは新しい順に記載し、概要は簡潔に。
詳細は git 履歴を参照。

詳細なオーサリングガイドは `plugin-claude-md.md` を参照。

---

## 環境変数

プラグインのフック/スクリプトは、`settings.json` の `env` ブロックで設定し `os.environ` で読む
環境変数によって設定可能にできる（詳細は `environment.md`）。プラグインが env 変数を読む場合は、
**プラグインの `CLAUDE.md` の `## Environment Variables` テーブルに記載する**（キー・値・デフォルト）。
キーはプラグイン名で名前空間化する（例: `PY_KIT_INJECTION_TTL`）。テーブル形式は `plugin-claude-md.md` 参照。
