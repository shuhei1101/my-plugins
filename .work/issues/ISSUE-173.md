# ISSUE-173: py-project / py-script / html-implement の SKILL.jp.md に YAML frontmatter がない（不統一）

**作成日**: 2026-06-02

## 問題

`SKILL.jp.md` に YAML frontmatter（`name` / `description`）を持つスキルと持たないスキルが混在している。`html-implement` / `html-logging` / `html-mock` / `py-script` の `SKILL.jp.md` には frontmatter がなく、代わりに `**スキル名**:` / `**トリガー**:` 等のインライン Markdown 記述でメタデータを表現している。

JP ミラーは通常 auto-load されないので実害は小さいが、フォーマット不統一は保守コストになる。

## 対応方針

各 `SKILL.jp.md` の先頭に YAML frontmatter（`name` と日本語 `description`）を追加して統一する。

## 対象ファイル

- `plugins/dev-kit/skills/html-implement/SKILL.jp.md`: YAML frontmatter 追加
- `plugins/dev-kit/skills/html-logging/SKILL.jp.md`: YAML frontmatter 追加
- `plugins/dev-kit/skills/html-mock/SKILL.jp.md`: YAML frontmatter 追加
- `plugins/dev-kit/skills/py-script/SKILL.jp.md`: YAML frontmatter 追加

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
