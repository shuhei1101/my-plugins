<!-- This file is a Japanese mirror of CLAUDE.md. When updating the English original, update this file too. -->
# claude-kit references

Claude Code 指示ファイル（skill / rule / CLAUDE.md / hook / plugin）のオーサリングガイド集。
`claude-kit-references-injection` フックが編集対象ファイルパスに応じて自動注入する。

これらの reference が各ファイル種別の **正本（オーサリング手順の単一情報源）**。creator スキル
（`skill-creator` / `rule-creator` / `hook-creator` / `claude-creator` / `plugin-creator`）は
これらに委譲する薄いラッパーになっており、対象ファイルを編集すれば該当ガイドが直接注入される
ため、スキルを起動せずにファイルを書ける。

## 手動で読む場合

- `_index.yaml` — 全 reference の一覧（path + 1 行 description。フックがパースする）
- `_injection_rules.yaml` — 編集パスパターン → `required` / `optional` reference

## 自動で読まれる場合

`PreToolUse(Edit | Write | MultiEdit | Read)` で `hooks/scripts/inject_references.py` が:

1. 編集対象ファイルパスを `_injection_rules.yaml` のパターンと照合
2. マッチした `required` reference は **本文全量**、`optional` は **パス + description のみ** を注入
3. `~/.claude/tokens/claude-kit/{session_id}.yaml` の二層 TTL トークンで重複排除
   （`CLAUDE_KIT_INJECTION_TTL` 秒経過で再注入。デフォルト 3600）:
   - `patterns`: そのパターンが期限内なら丸ごとスキップ
   - `references`: 本セッションで（どのパターン経由であれ）既に本文注入済みの `required` は
     **パスのみ**表示。これで複数パターンで共有されるリファレンス本文の二重注入を防ぐ

`CLAUDE_KIT_INJECTION_LANG=jp` で日本語 description を注入（`_index.jp.yaml` + `injection.jp.md.j2`）。

## パス → reference 対応

| 編集ファイル | 注入されるガイド |
|---|---|
| `**/skills/*/SKILL.md` | `common/common.md` + `skill/skills.md` |
| `**/CLAUDE{.local,.jp,}.md` | `common/common.md` + `claude-md/claude-md.md` |
| `plugins/*/CLAUDE{.jp,}.md` | ↑ + `plugin/plugin-claude-md.md` + `plugin/version-sync.md` |
| `**/hooks/hooks.json`、`**/.claude/settings.json` | `common/common.md` + `hook/hooks.md` + `common/environment.md` |
| `**/hooks/prompts/*.md` | `hook/hooks.md` |
| `**/.claude-plugin/{plugin,marketplace}.json` | `common/common.md` + `plugin/plugin-structure.md` + `plugin/version-sync.md` |
| `plugins/*/references/**/*.md` | `common/references-sync.md` |
| `plugins/*-kit/hooks/scripts/*.py` | `hook/kit-hooks-sync.md` |
| `plugins/*-kit/hooks/templates/*.j2` | `hook/kit-hooks-sync.md` + `hook/jinja2/authoring.md` |
| `**/hooks/templates/*.j2` | `hook/jinja2/templates.md` |

## メンテナンス

- reference 追加: ファイルを作り、`_index.yaml`（+ `_index.jp.yaml`）に追加し、`_injection_rules.yaml` のパターンに紐付ける
- `1 reference = 1 ユースケース` を保ち、1 ファイル編集で無関係なドキュメントを巻き込まない
- `_injection_rules.yaml` 編集後は orphan（index にあるのにパターン未紐付け、またはその逆）が無いか確認
- この注入構造は全 `*-kit` プラグインで共通 — `kit-hooks-index-sync` ルール参照。構造変更は足並みを揃える
