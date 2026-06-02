# ISSUE-155: claude-refactor SKILL.md がサブフォルダ再編後の旧ショートネームで references を列挙している

**作成日**: 2026-06-02

## 問題

`plugins/claude-kit/skills/claude-refactor/SKILL.md` の Step 1・Step 2・References セクションで、参照するガイドを `common.md`、`rules.md`、`skills.md`、`hooks.md`、`claude-md.md`、`provenance.md` というショートネーム（パスなし）で列挙している。3.48.0 の再編後、これらのファイルは実在せず、現行パスはいずれも日本語サブフォルダ配下にある。

**現行パス対照表**:

| 旧ショートネーム | 現行パス |
|---|---|
| `common.md` | `references/common/共通ガイド.md` |
| `rules.md` | `references/claude-md/記述ルール.md` |
| `skills.md` | `references/skill/スキル.md` |
| `hooks.md` | `references/hook/フック.md` |
| `claude-md.md` | `references/claude-md/CLAUDE-md記述ガイド.md` |
| `provenance.md` | 廃止（`references/common/共通ガイド.md` に統合） |

## 対応方針

Step 1 の読み込み指示・Step 2 のアノテーション・References セクションをすべて現行のフルパスに更新する。`provenance.md` への参照は「共通ガイドのスタンプ手順」に書き換える。JP ミラーも同期する。

## 対象ファイル

- `plugins/claude-kit/skills/claude-refactor/SKILL.md`: Step 1・Step 2・References の旧ショートネームを現行フルパスに修正
- `plugins/claude-kit/skills/claude-refactor/SKILL.jp.md`: JP ミラー同期

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
