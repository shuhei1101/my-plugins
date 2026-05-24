# Incident: skill-creator-dispatch が UserPromptSubmit のみで直接編集をブロックできなかった

## 概要

claude-kit の `skill-creator-dispatch` フックが `UserPromptSubmit` にのみ存在し、ユーザーが曖昧なプロンプト（例: 「PR120 の続きをやって」）を送った場合、フックが発火しなかった。その結果、Claude が `skill-creator` を経由せず直接 `SKILL.md` を編集した。

## 原因

- `UserPromptSubmit` フックはユーザーの**入力テキスト**をスキャンする
- キーワード `skill.md` / `/skills/` が入力に含まれない場合はフックが発火しない
- Claude が自律判断で `SKILL.md` を編集しようとしても発火しない

## 修正内容

4つのプラグイン（claude-kit / dev-kit / ui-kit / work-kit）に `PreToolUse` (Edit|Write) ブロック型フックを追加した。

- ファイルパスが `/skills/[^/]+/SKILL\.md$` にマッチした場合にブロック
- セッションフラグ（`/tmp/skill-creator-dispatch-{session_id}`）で初回のみブロック
- ブロック後 `skill-creator` を経由した編集は素通り

## 教訓

**creator-dispatch フックは UserPromptSubmit だけでは不十分。** ユーザーが明示的にファイルパスを言及しない場合でも Claude が対象ファイルを編集しようとする場面がある。ファイル種別ベースの保護は `PreToolUse` ブロック型フックで行うこと。`UserPromptSubmit` は「早期警告」として補助的に残してよいが、実効的なガードは `PreToolUse` で実装する。
