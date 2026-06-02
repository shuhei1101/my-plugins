# ISSUE-158: claude-kit:plugin-config SKILL.md の description に英語トリガーフレーズが欠落

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/claude-kit/skills/plugin-config/SKILL.md` の `description` フロントマターは日本語トリガーフレーズのみで、英語の自然言語トリガーが存在しない。

```yaml
description: |
  When /claude-kit:plugin-config is invoked.
  Or when the user says "設定を変えたい", "env を設定したい", "トグルを切り替えたい", "JP ミラーを無効にしたい", "注入言語を変えたい".
```

他の claude-kit スキルはすべて英語と日本語の両方のトリガーフレーズを含んでいる（例: `claude-creator` は "create a CLAUDE.md" と "CLAUDE.md を作って" の両方を含む）。英語ユーザーが `plugin-config` を自然言語で呼び出す手段がない。

## 対応方針

description に英語トリガーフレーズを追加する。例：`"change plugin settings"`、`"configure env vars"`、`"disable JP mirror"`、`"change injection language"` など。JP ミラーの description は変更不要（日本語のみで正しい）。

## 対象ファイル

- `plugins/claude-kit/skills/plugin-config/SKILL.md`: frontmatter の `description` フィールドに英語トリガーフレーズを追加
