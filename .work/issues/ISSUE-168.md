# ISSUE-168: html-debug-fab / html-logging / html-implement がスキルフォルダ名を誤参照

**作成日**: 2026-06-02

## 問題

複数スキルの `References` セクションおよび手順内で、存在しないフォルダ名を参照している。実際のスキルフォルダは `html-debug-fab` / `html-logging` / `html-mock` だが、参照では旧名または短縮名が使われている。

### html-debug-fab/SKILL.md（および SKILL.jp.md）

- `{plugin_root}/skills/logging/SKILL.md` → 実パスは `skills/html-logging/SKILL.md`
- `{plugin_root}/skills/debug-fab/templates/uidev.css` → 実パスは `skills/html-debug-fab/templates/uidev.css`
- References: `{plugin_root}/skills/debug-fab/templates/CLAUDE.md` → 実パスは `skills/html-debug-fab/templates/CLAUDE.md`

### html-logging/SKILL.md（および SKILL.jp.md）

- References: `{plugin_root}/skills/debug-fab/SKILL.md` → 実パスは `skills/html-debug-fab/SKILL.md`

### html-implement/SKILL.md（および SKILL.jp.md）

- References: `{plugin_root}/skills/mock/SKILL.md` → 実パスは `skills/html-mock/SKILL.md`
- References: `{plugin_root}/skills/logging/SKILL.md` → 実パスは `skills/html-logging/SKILL.md`

## 対応方針

各ファイルの誤ったパスを正しいフォルダ名（`html-debug-fab` / `html-logging` / `html-mock`）に修正する。英語版と JP ミラーの両方を更新する。

## 対象ファイル

- `plugins/dev-kit/skills/html-debug-fab/SKILL.md`: `skills/logging/` → `skills/html-logging/`、`skills/debug-fab/` → `skills/html-debug-fab/`
- `plugins/dev-kit/skills/html-debug-fab/SKILL.jp.md`: 同上
- `plugins/dev-kit/skills/html-logging/SKILL.md`: `skills/debug-fab/SKILL.md` → `skills/html-debug-fab/SKILL.md`
- `plugins/dev-kit/skills/html-logging/SKILL.jp.md`: 同上
- `plugins/dev-kit/skills/html-implement/SKILL.md`: `skills/mock/SKILL.md` → `skills/html-mock/SKILL.md`、`skills/logging/SKILL.md` → `skills/html-logging/SKILL.md`
- `plugins/dev-kit/skills/html-implement/SKILL.jp.md`: 同上

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
