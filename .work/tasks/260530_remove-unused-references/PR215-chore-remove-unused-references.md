# PR215 — remove-unused-references

## 概要

`plugins/claude-kit/references/` にある `glossary.md` / `incidents.md`（およびJPミラー）が不要になったため削除する。
これらは `.claude/rules/glossary.md` や `.claude/rules/incidents.md` のフォーマットガイドだったが、現在は使われていない。

削除に合わせて、これらのファイルを参照している箇所もクリーンアップする。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QAを `## QA` に記録する | - |
| - | `.work/notes/` のノートドキュメントを更新する | - |
| - | `glossary.md` / `incidents.md` とJPミラーを削除 | - `plugins/claude-kit/references/glossary.md`<br>- `plugins/claude-kit/references/glossary.jp.md`<br>- `plugins/claude-kit/references/incidents.md`<br>- `plugins/claude-kit/references/incidents.jp.md` |
| - | `_index.yaml` / `_index.jp.yaml` から該当エントリを削除 | - `plugins/claude-kit/references/_index.yaml`<br>- `plugins/claude-kit/references/_index.jp.yaml` |
| - | `references/CLAUDE.md` / `CLAUDE.jp.md` のインジェクションルールテーブルから該当行を削除 | - `plugins/claude-kit/references/CLAUDE.md`<br>- `plugins/claude-kit/references/CLAUDE.jp.md` |
| - | `skills/plugin-update/SKILL.md` / `SKILL.jp.md` から参照を削除 | - `plugins/claude-kit/skills/plugin-update/SKILL.md`<br>- `plugins/claude-kit/skills/plugin-update/SKILL.jp.md` |
| - | ルール / CLAUDE.md を更新する | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/claude-kit/references/glossary.md` | 削除 | 不要になったためファイルごと削除 | - |
| `plugins/claude-kit/references/glossary.jp.md` | 削除 | 同上（JPミラー） | - |
| `plugins/claude-kit/references/incidents.md` | 削除 | 不要になったためファイルごと削除 | - |
| `plugins/claude-kit/references/incidents.jp.md` | 削除 | 同上（JPミラー） | - |
| `plugins/claude-kit/references/_index.yaml` | 編集 | glossary/incidentsエントリを削除 | - |
| `plugins/claude-kit/references/_index.jp.yaml` | 編集 | 同上（JPミラー） | - |
| `plugins/claude-kit/references/CLAUDE.md` | 編集 | インジェクションルールテーブルから該当行を削除 | - |
| `plugins/claude-kit/references/CLAUDE.jp.md` | 編集 | 同上（JPミラー） | - |
| `plugins/claude-kit/skills/plugin-update/SKILL.md` | 編集 | glossary/incidents参照を削除 | - |
| `plugins/claude-kit/skills/plugin-update/SKILL.jp.md` | 編集 | 同上（JPミラー） | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト変更なし | - |

## QA

QAなし

## 参考ドキュメント

- `.work/notes/remove-unused-references.md`: 削除対象ファイルとクリーンアップ箇所の記録

## 関連PR

| PR番号 | 概要 |
|---|---|
| - | - |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
