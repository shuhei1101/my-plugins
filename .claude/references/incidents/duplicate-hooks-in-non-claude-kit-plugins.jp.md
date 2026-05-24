<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# インシデント: claude-kit 以外のプラグインに重複ガードフックを追加した

## 日付
2026-05-25

## 概要
PR121 で `skill-creator-dispatch` PreToolUse フックを4プラグイン（claude-kit / dev-kit / ui-kit / work-kit）に追加したが、claude-kit がすでに SKILL.md をグローバルにガードしているため、dev-kit/ui-kit/work-kit への追加は重複だった。PR124 で削除した。

## 何が起きたか
- PR121 は `skill-creator-dispatch` を `PreToolUse` ブロック型フックとして4プラグインに追加し、Claude が `skill-creator` を経由せず直接 `SKILL.md` を編集するのを防ごうとした。
- フックコード・フラグ名（`skill-creator-dispatch-{sid}`）・プロンプトファイルの内容は4プラグインで完全に同一だった。
- claude-kit のフックはグローバルに適用される（どのプラグインのファイルを編集中であっても発火する）ため、dev-kit/ui-kit/work-kit への3コピーは不要な重複だった。

## なぜ起きたか
PR121 の教訓「SKILL.md ガードには UserPromptSubmit より PreToolUse ブロックが有効」は正しかったが、「全プラグインに追加すれば確実」という過剰一般化があった。正しくは claude-kit にのみ追加すればよかった。

## 対処
PR124 で以下を削除した:
- `dev-kit/hooks/hooks.json`、`ui-kit/hooks/hooks.json`、`work-kit/hooks/hooks.json` の `PreToolUse` から `skill-creator-dispatch` エントリ
- `plugins/{dev-kit,ui-kit,work-kit}/hooks/prompts/skill-creator-dispatch.md`（と `.jp.md`）

## 再発防止
**グローバルなガードフック**（どのプラグインのファイルを編集しても発火させたい）は **claude-kit にのみ** 追加する。claude-kit は中央ツールキットプラグインであり、そのフックはグローバルに動作する。

非 claude-kit プラグインへのフック追加が適切なのは:
- そのプラグイン固有のファイルにのみ発火すべき場合（例: dev-kit が `.py` / `.yaml` にフックする）
- プラグインごとに動作が異なる場合

非 claude-kit プラグインに新しいフックを追加する前に「claude-kit に既にあるか？」と確認すること。
