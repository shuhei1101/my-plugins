# ISSUE-032: dev-kit 内で `name` フィールドのプレフィックス付与が不統一

**作成日**: 2026-05-31

## 問題

`plugins/dev-kit/skills/` 配下の9スキルのうち7つは `name` フィールドに `dev-kit:` プレフィックスを付与しているが、`plugin-config` と `plugin-migrate` だけが裸の名前を使っており、命名規則が不統一になっている。

| No | スキルディレクトリ | 現在の `name` | 期待される `name` |
|---|---|---|---|
| 1 | `skills/html-debug-fab/SKILL.md` | `dev-kit:html-debug-fab` | `dev-kit:html-debug-fab`（問題なし） |
| 2 | `skills/html-implement/SKILL.md` | `dev-kit:html-implement` | `dev-kit:html-implement`（問題なし） |
| 3 | `skills/html-logging/SKILL.md` | `dev-kit:html-logging` | `dev-kit:html-logging`（問題なし） |
| 4 | `skills/html-mock/SKILL.md` | `dev-kit:html-mock` | `dev-kit:html-mock`（問題なし） |
| 5 | `skills/next-implement/SKILL.md` | `dev-kit:next-implement` | `dev-kit:next-implement`（問題なし） |
| 6 | `skills/next-plan/SKILL.md` | `dev-kit:next-plan` | `dev-kit:next-plan`（問題なし） |
| 7 | `skills/py-script/SKILL.md` | `dev-kit:py-script` | `dev-kit:py-script`（問題なし） |
| 8 | `skills/plugin-config/SKILL.md` | `plugin-config` | **`dev-kit:plugin-config`** |
| 9 | `skills/plugin-migrate/SKILL.md` | `plugin-migrate` | **`dev-kit:plugin-migrate`** |

`dev-kit/CLAUDE.md` の Skills 一覧では `dev-kit:plugin-migrate`、`dev-kit:plugin-config` と記載されており、`name` フィールドとの乖離が生じている。また、`work` プラグインや `ref-inject` プラグインにも同名の `plugin-migrate` / `plugin-config` スキルが存在するため（ISSUE-033 参照）、裸の `name` だと競合リスクがある。

## 修正案

`plugins/dev-kit/skills/plugin-config/SKILL.md` と `plugins/dev-kit/skills/plugin-migrate/SKILL.md` の `name` フィールドをそれぞれ `dev-kit:plugin-config`、`dev-kit:plugin-migrate` に変更する。対応する `SKILL.jp.md` も同時に更新する。

```yaml
# plugin-config/SKILL.md
name: dev-kit:plugin-config

# plugin-migrate/SKILL.md
name: dev-kit:plugin-migrate
```

## 水平展開

`claude-kit`、`work`、`ref-inject` の各プラグインでも同名スキル (`plugin-config` / `plugin-migrate`) が裸の `name` で登録されている（ISSUE-033 で扱う）。プラグイン横断的に命名規則を統一するかどうかを検討する際の起点として本イシューを参照のこと。
