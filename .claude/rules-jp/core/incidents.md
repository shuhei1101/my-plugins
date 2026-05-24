> ⚠️ **日本語ミラー** — Claude には自動ロードされません。このファイルを更新する際は、必ず英語本体 `.claude/rules/core/incidents.md` も同時に更新してください。

# Incidents（インシデントログ）

| Date | Summary | Detail |
|---|---|---|
| 2026-05-21 | master で直接ファイルを編集すると worktree マージ時に競合が発生する。必ず work-start → worktree 内で作業する | [detail](../../references/incidents/master-direct-edit-causes-merge-conflict.md) |
| 2026-05-23 | スキルが Step 0 で他のスキルを読み込む設計にすると起動ごとに 2500×N トークンを消費してコンテキストを圧迫する。判定知識はスキル本体の References に内包させること | [detail](../../references/incidents/skill-reading-token-cost.md) |
| 2026-05-23 | 複数のスキルが同じ判断基準を inline で二重管理していた。creator スキル群の共通知識は `references/` に集約し、各スキルから参照する設計にすること | [detail](../../references/incidents/creator-skill-inline-duplication.md) |
| 2026-05-24 | merge スキルがユーザーの明示的指示なしに `git merge` を自動実行した。セッション内で過去に許可を得ていても次のマージは別指示が必要。修正: SKILL.md に Critical Prohibition セクション追加・Step 6 に絶対禁止ルール追記 | [detail](../../references/incidents/merge-auto-execution-without-permission.md) |
| 2026-05-24 | `.work/specs/` フォルダ名が「仕様書」を連想させるため、AI に自動読み込みされないにもかかわらず重要ドキュメント扱いになり古くなりやすかった。AI 非読み込みのフォルダは `notes/` など非公式な名前にすること | [detail](../../references/incidents/work-folder-name-implies-official-docs.md) |
| 2026-05-24 | merge スキルが master cwd で conversation-to-claude を呼んでいたため、生成された glossary/incidents が master 直接コミットになり PR ブランチに同梱されなかった。修正: ワークツリーに cd してから呼び出す。教訓: git commit を含むスキルへの委譲は呼び出し側で cwd を明示的に制御すること | [detail](../../references/incidents/conversation-to-claude-master-direct-commit.md) |
| 2026-05-24 | `.jp.md` ファイルの JP 警告コメント有無を `head -5` で検証したため、frontmatter 持ちファイル（警告が 7 行目以降にある）を「警告なし」と誤検出し対象件数を 39 件と過大算定した。実際は 25 件。ファイル先頭メタデータの検証は frontmatter を skip した上で本体先頭を見るべき | [detail](../../references/incidents/header-check-misses-frontmatter-files.md) |
| 2026-05-24 | hook-creator で `hooks/prompts/*.md` を作成した際に `*.jp.md` の JP ミラーを作成しなかった。`skill-jp-mirror-sync.md` ルールは SKILL.md のみ対象のため hook prompts はカバーされていなかった。修正: `hook-prompts-jp-mirror-sync.md` ルールを追加 | [detail](../../references/incidents/hook-prompts-jp-mirror-missing.md) |
| 2026-05-24 | スキルのステップを独立スキルに切り出した際、master に同じステップを変更する PR が既に存在し、実装後に2回の master 取り込みが必要になった。対象ステップの切り出し前に `git log --oneline master -- {ファイル}` で直近の変更を確認すること | [detail](../../references/incidents/extract-step-check-master-first.md) |
| 2026-05-24 | `CLAUDE.md` を編集した際に `CLAUDE.jp.md` の JP ミラー更新を忘れた。`skill-jp-mirror-sync.md` も `hook-prompts-jp-mirror-sync.md` も CLAUDE.md はカバーしていなかった。修正: `claude-md-jp-mirror-sync.md` ルールを追加 | [detail](../../references/incidents/claude-md-jp-mirror-missing.md) |
| 2026-05-24 | `incidents.md` / `glossary.md` を編集しても `rules-jp/` の JP ミラーが更新されず、英語版との乖離が長期間放置された。修正: `incidents-glossary-jp-mirror-sync.md` ルールを追加して同コミット更新を強制する | [detail](../../references/incidents/incidents-glossary-jp-mirror-missing.md) |
| 2026-05-24 | 複数の Stop フックが同時発火すると、`"Read and follow: /path"` 方式の指示が `stop_hook_active` ガードで無効化される。Claude は直接指示（notify-aituber 等）を先に実行して再 Stop し、2回目の発火では stop_hook_active=true のため全フックがスキップ → 間接参照の指示が永遠に実行されない。修正: reason/stdout にファイル内容を直接埋め込む方式に戻す | [detail](../../references/incidents/stop-hook-multiple-block-race-condition.md) |
| 2026-05-24 | PR115 でフックパターンを一括変更した際、work-kit/dev-kit/ui-kit は修正したが claude-kit/hooks.json の UserPromptSubmit × 5・PostToolUse × 1 が漏れた。教訓: フックパターンの横断変更は `grep -r "対象パターン" --include="*.json" .` で全プラグインを確認してから修正すること | [detail](../../references/incidents/hook-pattern-change-missed-plugin.md) |
| 2026-05-25 | statusLine の `python -c "..."` 内で `r5["resets_at"]` のダブルクォートが外側を切り、rate_limits.resets_at が入った瞬間に NameError でステータスラインが落ちる。修正: `r5.get('resets_at')` でシングルクォート完結に変更 | [detail](../../references/incidents/statusline-python-quote-nesting.md) |
| 2026-05-25 | `apply-statusline.py` を WSL Python で実行したが、Claude Code は Windows ネイティブで動いていたため別の settings.json を書き換え、変更が反映されなかった（エラーも出ない）。教訓: `Path.home()` を使うスクリプトは Claude Code と同じ Python 環境で実行する | [detail](../../references/incidents/path-home-cross-env-mismatch.md) |
