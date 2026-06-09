---
name: claude-kit:hook-creator
description: |
  Create a prompt-injection hook — a hook that injects a text prompt into Claude's context at a specific event.
  Trigger when the user says "I want to give Claude instructions at a specific moment", "inject a prompt on hook",
  "create a hook that tells Claude to do X when Y happens", "hook でプロンプトを差し込みたい",
  "特定のタイミングで AI に指示を出したい", or invoked explicitly as `/claude-kit:hook-creator`.
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# hook-creator — プロンプト注入フック作成（薄ラッパー）

フックのオーサリング手順は本プラグインの references に移り、`hooks.json` / `.claude/settings.json` /
`hooks/prompts/*.md` を編集すると `claude-kit-references-injection` フックが**自動注入**する。
このスキルは明示起動と呼び出し元のために残している薄いラッパー。

## やること

1. `references/hooks.md` + `references/common.md`（本プラグイン内）に従う。フック設定を書く際に
   自動注入される。注入されない場合は直接読む。両者は「フックイベントとイベント対応」「注入メカニズム」
   「使用時機」「ループ防止（`stop_hook_active` / ワンタイムトークン / セッションフラグ）」「すぐ使える
   `hooks.json` スニペット」「プロンプトファイル配置」「パス変数」をカバーする。
2. リファレンス自動注入フックは手作りせず `/ref-inject:apply <plugin>` を使う。
3. プロンプトファイル（プラグインフックは `.jp.md` ミラーも）を作り、`hooks.json` / `settings.json` に
   配線し、`Stop` / `PreToolUse` ブロック型にはループガードを付ける。
4. 各 `.jp.md` ミラーの冒頭に JP ミラー警告コメントを付ける（フォーマットは `references/common/共通ガイド.md`、
   ファイルを書く際に自動注入される）— 直接書く（スキル呼び出し不要）。
