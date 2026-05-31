---
name: plugin-migrate
description: |
  プロジェクト内の claude-kit 由来成果物（`.claude/skills/**` / `.claude/rules/**` /
  `.claude/hooks/**` / `**/CLAUDE.md` / `**/.claude-plugin/{plugin,marketplace}.json`）を、
  現在インストール済みの claude-kit リファレンス規約と照合し、逸脱があれば最小限の差分を
  当て込む。また `~/.claude/settings.json` の `statusLine` が claude-kit 由来であれば
  最新定義で再適用する。手動起動のみ — `/claude-kit:plugin-migrate`。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# claude-kit:plugin-migrate — claude-kit 規約への追従

dev-kit / work プラグインの plugin-migrate は **静的テンプレの再コピー** だが、
claude-kit はテンプレを project に展開しない（各 creator スキルは「現行リファレンスに沿って
ファイルを生成・編集する」薄いラッパであり、規約自体は `references/*.md` に集約されている）。
したがって claude-kit の plugin-migrate は **「規約 vs プロジェクト既存成果物」の照合 + 差分適用**
というセマンティック・マイグレーションを行う。

照合のキモは「対象ファイルを `Read` で開けば、`claude-kit-references-injection` フックが
該当リファレンスを自動注入する」点。スキル本文で規約を再掲する必要はなく、
**注入されたリファレンスを規約のソース・オブ・トゥルースとして扱う**。

他プラグインの成果物には踏み込まない。ブランチ運用（コミット・マージ）はユーザー責任。

---

## 同期対象（プロジェクト成果物 → 照合に使う claude-kit リファレンス）

| プロジェクト側パターン | リファレンス（auto-inject される） |
|---|---|
| `**/skills/*/SKILL{.jp,}.md` | `references/skill/skills.md` + `common/common.md` |
| `**/.claude/rules/**/*.md`, `**/.claude/rules-jp/**/*.md` | `references/claude-md/rules.md` + `common/common.md` |
| `**/CLAUDE{.local,.jp,}.md` | `references/claude-md/claude-md.md` + `common/common.md` |
| `plugins/*/CLAUDE{.jp,}.md` | `references/plugin/plugin-claude-md.md` + `references/plugin/version-sync.md` 追加 |
| `**/hooks/hooks.json` | `references/hook/hooks.md` + `common/common.md` + `common/environment.md` |
| `**/.claude/settings{.local,}.json` | `references/hook/hooks.md` + `common/common.md` + `common/environment.md` |
| `**/hooks/prompts/*.md` | `references/hook/hooks.md` |
| `**/.claude-plugin/{plugin,marketplace}.json` | `references/plugin/plugin-structure.md` + `common/common.md` + `plugin/version-sync.md` |
| `~/.claude/settings.json` の `statusLine` ブロック | `scripts/apply-statusline.py` の定義 |

`agents/` は claude-kit に対応リファレンスがないため、common.md の「ファイル種別判定 +
JP/EN ミラー規約」のみが適用される（agents.md は将来追加予定）。

---

## タスク

### ステップ 1: 各カテゴリを巡回し、規約逸脱を修正

#### 条件

- 常に最初に実行する

#### 処理

以下のカテゴリを **この順番で** 巡回する。各カテゴリで「列挙 → 1 ファイルずつ Read → 差分を当てる」を繰り返す:

1. **Skills** — `find . -type f -path '*/skills/*/SKILL.md' -not -path '*/node_modules/*' -not -path '*/.git/*'`
2. **Rules** — `find .claude/rules .claude/rules-jp -type f -name '*.md' 2>/dev/null`（ディレクトリ無ければスキップ）
3. **CLAUDE.md** — `find . -type f \( -name 'CLAUDE.md' -o -name 'CLAUDE.jp.md' -o -name 'CLAUDE.local.md' \) -not -path '*/node_modules/*' -not -path '*/.git/*'`
4. **Hooks (manifest)** — `find . -type f -name 'hooks.json' -not -path '*/node_modules/*' -not -path '*/.git/*'` および `.claude/settings.json` / `.claude/settings.local.json`
5. **Hook prompts** — `find . -type f -path '*/hooks/prompts/*.md' -not -path '*/node_modules/*' -not -path '*/.git/*'`
6. **Plugin manifests** — `find . -type f \( -name 'plugin.json' -o -name 'marketplace.json' \) -path '*/.claude-plugin/*' -not -path '*/node_modules/*' -not -path '*/.git/*'`（マーケットプレイスリポジトリのみ該当）

各ファイルについて:

a. `Read` ツールで開く → 注入フックが該当 references を自動注入する
b. 注入されたリファレンス本文を **規約の決定版** として読み取る
c. ファイル内容と照らし合わせ、欠落・古い記法・規約違反を列挙
d. `Edit` で **最小限の差分** を適用（既存のユーザーコンテンツを保持。全面書き換えは禁止）
e. JP mirror（`*.jp.md` / `CLAUDE.jp.md` / `rules-jp/`）は英語版を直した後、対応箇所を同様に更新
f. 既に規約準拠ならそのファイルはスキップ

→ ステップ 2 へ

#### 注意事項

##### 分岐

- カテゴリごとの巡回中に「内容が完全に陳腐化していて差分でなく再生成が妥当」と判断したら、ユーザーに「再生成を含めますか？」と確認してから進める（デフォルトは差分適用のみ）

##### 禁止事項

- ファイル全体の置き換え（差分マイグレーションでなくテンプレ展開になるため）
- 他プラグインの成果物（例: `plugins/work/skills/*/SKILL.md`）への変更 — それらは各プラグインの `plugin-migrate` の責務

---

### ステップ 2: statusline を必要に応じて再適用

#### 条件

- ステップ 1 完了

#### 処理

1. `~/.claude/settings.json` を Read（無ければスキップ）
2. `statusLine.command` の文字列内に claude-kit の statusline 識別子（例: `ctx ` リテラルや `ml=m.lower()` など `apply-statusline.py` の特徴）が含まれているか確認
3. 含まれている場合 → `python ${CLAUDE_PLUGIN_ROOT}/scripts/apply-statusline.py` を実行して最新定義で書き換え
4. 含まれていない場合 → スキップ（claude-kit の statusline を使っていないユーザー）

→ ステップ 3 へ

---

### ステップ 3: 差分を報告

#### 条件

- ステップ 2 完了

#### 処理

1. `git status` と `git diff`（巨大なら抜粋）を提示
2. 変更がなければ「claude-kit 由来の成果物はすべて v{N} に準拠しています」と報告して終了
3. 変更があれば、編集したファイル一覧 と 推奨コミットメッセージ を提示:
   - 例: `chore: sync claude-kit-authored artifacts to v{N}`
4. `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` から現行バージョン `{N}` を読み取る
5. **このスキルは自分でコミットしない**。コミット / マージ判断はユーザーの責任

→ 完了

#### 注意事項

##### 禁止事項

- 自動コミット（dev-kit / work の plugin-migrate と同じ方針）
