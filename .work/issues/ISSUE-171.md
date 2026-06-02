# ISSUE-171: next-plan の References が旧名ファイル injection_rules.yaml（アンダースコアなし）を参照

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`dev-kit:next-plan` の `References` セクションが `references/injection_rules.yaml`（アンダースコアなし）を参照しているが、v4.2.0 でこのファイルは `_injection_rules.yaml` に改名されている。旧名のファイルは存在しない。

v4.2.0 changelog:
> Rename meta-YAML files in `references/` with `_` prefix: `injection_rules.yaml` → `_injection_rules.yaml`

`SKILL.jp.md` も同様。

## 対応方針

`references/injection_rules.yaml` を `references/_injection_rules.yaml` に修正する。

## 対象ファイル

- `plugins/dev-kit/skills/next-plan/SKILL.md`: References セクションのファイル名を修正
- `plugins/dev-kit/skills/next-plan/SKILL.jp.md`: 同上
