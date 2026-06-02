# ISSUE-154: 薄ラッパースキル5本が旧フラットパスで references を参照している（3.48.0 再編未反映）

**作成日**: 2026-06-02

## 問題

バージョン 3.48.0 で `references/` がロールベースのサブフォルダ構成に再編成された（`common/`、`skill/`、`hook/`、`claude-md/`、`plugin/`）。しかし、薄ラッパー系スキル 5 本がいずれも旧フラットパスを記述したままになっており、実在しないパスを指し示している。

スキルは「自動注入されない場合は直接 Read してください」と案内しているため、このパスが誤っているとフォールバック時に読めない。

**実在しないパス一覧（旧 → 現行正）**:

| 旧パス（存在しない） | 現行パス |
|---|---|
| `references/common.md` | `references/common/共通ガイド.md` |
| `references/skills.md` | `references/skill/スキル.md` |
| `references/rules.md` | `references/claude-md/記述ルール.md` |
| `references/hooks.md` | `references/hook/フック.md` |
| `references/claude-md.md` | `references/claude-md/CLAUDE-md記述ガイド.md` |
| `references/plugin-structure.md` | `references/plugin/プラグイン構造.md` |
| `references/provenance.md` | 廃止（`references/common/共通ガイド.md` に統合） |

## 対応方針

各薄ラッパースキルの `SKILL.md` と `SKILL.jp.md` の参照パス記述を現行のサブフォルダ構成に更新する。`provenance.md` への参照は「`references/common/共通ガイド.md` のスタンプ手順に従う」に書き換える。

## 対象ファイル

- `plugins/claude-kit/skills/claude-creator/SKILL.md`: 旧パス参照を修正
- `plugins/claude-kit/skills/claude-creator/SKILL.jp.md`: JP ミラー同期
- `plugins/claude-kit/skills/rule-creator/SKILL.md`: 旧パス参照を修正
- `plugins/claude-kit/skills/rule-creator/SKILL.jp.md`: JP ミラー同期
- `plugins/claude-kit/skills/skill-creator/SKILL.md`: 旧パス参照を修正
- `plugins/claude-kit/skills/skill-creator/SKILL.jp.md`: JP ミラー同期
- `plugins/claude-kit/skills/hook-creator/SKILL.md`: 旧パス参照を修正
- `plugins/claude-kit/skills/hook-creator/SKILL.jp.md`: JP ミラー同期
- `plugins/claude-kit/skills/plugin-creator/SKILL.md`: 旧パス参照を修正
- `plugins/claude-kit/skills/plugin-creator/SKILL.jp.md`: JP ミラー同期

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
