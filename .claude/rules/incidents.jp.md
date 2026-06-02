<!-- This file is a Japanese mirror. When updating the English original (incidents.md), update this file too. -->
# Incidents（インシデント）

実際に起きた**作業プロセスのミス**（操作・判断の誤り。コードのバグは対象外）を再発防止のために記録する。
各件の詳細は `.claude/references/incidents/{slug}.md`（+ `.jp.md`）に置く。

英語オリジナル: `.claude/rules/incidents.md`

> 採用基準とフォーマット: `plugins/work/references/conversation/インシデント.md`。

---

| No | カテゴリ | インシデント (slug) | 要約 |
|---|---|---|---|
| 1 | リファレンス / フック注入の記述 | bestprac-over-usecase-references-bloat | リファレンスは `injection_rules.yaml` のトリガーマップ起点で設計する（内容の目次起点ではない）。1 ファイル = 1 ユースケース、比較・選定・トレードオフ節は持たない。 |
| 2 | 〃 | orphan-references-not-checked | `injection_rules.yaml` 編集後は YAML とファイルシステムを突合する孤立チェックを実行し、どのパターンにも紐づかない reference を残さない。 |
| 3 | 〃 | glob-pattern-missing-recursive-prefix | 名前ベースのフォルダ glob には `**/` を前置する（例 `**/tools/**/*.py`）。ルート固定パターンは直下に必ず置かれるファイル専用。 |
| 4 | 〃 | yaml-unquoted-colon-space-breaks-parse | 引用符なし YAML スカラー内に `word: `（コロン+空白）を書かない — ネストしたマップと解釈され `safe_load` が壊れる。値を引用し検証する。 |
| 5 | 〃 | markdown-for-code-consumed-config | コードが読む設定は構造化形式（YAML/JSON）のまま保つ。人間用に Markdown ビューが要るなら生成する — ソース自体を表に変換しない。 |
| 6 | 〃 | injection-only-fires-on-write-edit-path | AI 呼び出しスキルを注入専用 reference に置き換える前に、全呼び出し元の対象が Write/Edit/Read 経路上にあるか確認する。スクリプト生成・非マッチのファイルはスキルが必要。 |
| 7 | 〃 | ref-inject-overbuilt-script-and-hook | 生成スクリプトより Claude 駆動のコピー+置換を優先し、既存の TTL/仕組みで足りる挙動に新フックを足さない — 最小の仕組みを既定にする。 |
| 8 | スキル / プラグイン設計 | skill-reading-token-cost | スキルが実行時に他スキルを読み込む設計にしない（1 回あたり約 2,500×N トークン）。必要な判定知識はそのスキル自身の references に埋め込む。 |
| 9 | 〃 | premature-cross-plugin-centralization | 利用者が 3 つ以上（または drift の再発）になるまでプラグイン横断の集約をしない。2 プラグイン間はコピペの方が安い。 |
| 10 | 〃 | skill-cli-args-format | Claude Code スキルは CLI フラグを取らない — 期待入力は `--flag` 表ではなく自然言語の箇条書きで書く。 |
| 11 | 〃 | skill-name-log-implies-error-log | データを永続化するスキル/関数は `save`/`write`/`record` と命名する。`log` は本来のロギング出力に取っておく。 |
| 12 | 命名 / ドキュメント | work-folder-name-implies-official-docs | AI が自動ロードしないフォルダには非公式な名前（例 `notes/`）を付ける — 公式に見える名前（`specs/`）は権威ある文書扱いされ陳腐化を招く。 |
| 13 | Git / ブランチ / マージのワークフロー | stale-session-git-snapshot-already-merged-followup | 後続・ブランチ跨ぎの作業を始める前に実際の現 master を確認する（`git log master`、`git worktree list`）— セッション開始時のスナップショットは古く、候補が既にマージ済みのことがある。 |
| 14 | 〃 | large-master-adapt-user-decisions | 進んだ master への適合が新しい識別子名・スコープ判断・中止/続行判断を迫る場合は、ユーザーに 2〜4 問尋ねてから進める — tiebreaker はコミット順の事実しかカバーしない。 |
| 15 | 〃 | master-deletion-overlooked-on-long-branch | 長命ブランチでは rule/index/overview ファイルを編集する前に `git show master:{file}` の存在を確認する — master 側で既に削除されている場合がある。 |
| 16 | 〃 | parallel-pr-version-bump-collision | `git diff HEAD..master` で同一プラグインの version bump が見えたら、マージ前にブランチ側を次バージョンへ再 bump する。 |
| 17 | 〃 | worktree-reserved-before-predecessor-merge | ブランチが先行をミラーする場合、in-tree ファイルを雛形扱いする前に先行がブランチ履歴に含まれるか確認する（`git merge-base --is-ancestor`）。なければ先に `git merge master`。 |
| 18 | 〃 | merge-theirs-loses-branch-only-additions | `git merge -X theirs` / `checkout --theirs` はブランチ固有の追加を黙って捨てる。片側一括採用ではなく追加分を手動で取り込む。 |
| 19 | プロセス / QA | design-qa-implementation-creep | 方針/設計のみのブランチでは QA は what/why/where まで — 実装詳細（how）は書かない。 |
| 20 | フック / スクリプト / 環境 | git-guard-false-positive-file-content | コマンドガードは、マッチ文字列がファイル内容や部分文字列として現れた時に誤検知しうる。部分文字列ではなくコマンド本体にマッチさせる。 |
| 21 | 〃 | python3-c-backtick-shell-expansion | `python3 -c "..."` 内のバッククォートは Python が見る前にシェルがコマンド置換する。バッククォートを避けるか、シングルクォートのヒアドキュメント/ファイル経由で渡す。 |
| 22 | 〃 | path-home-cross-env-mismatch | `Path.home()` を使うスクリプトは Claude Code と同じ Python 環境で実行する — Claude Code がネイティブ Windows なのに WSL Python（逆も同様）で動かすと別の home を黙って編集し、何も適用されない。 |
| 23 | 〃 | template-under-gitignore | `.gitignore` のあるディレクトリにファイルを置く前に `git check-ignore -v` で追跡可能か確認する。無理ならセットアップスクリプトで実行時に書き出す。 |
| 24 | 〃 | claude-plugin-root-unset-manual-steps | Bash ツールでスキル手順を手動実行するとき（`disable-model-invocation: true` のスキルなど）`${CLAUDE_PLUGIN_ROOT}` は未設定。work プラグインのスクリプトコマンドを実行する前に `find` でパスを特定する。 |
| 25 | 〃 | pretooluse-read-block-cancels-tool | `PreToolUse(Read)` フックで `{"decision": "block"}` を返すと Read がキャンセルされファイル内容を Claude が受け取れない。Read 時は `hookSpecificOutput.permissionDecision: "allow"` + `additionalContext` でコンテキストを注入しつつ Read を通過させる。 |
| 26 | Git / ブランチ / マージのワークフロー | migration-reruns-resets-processed-state | 一括変換スクリプトを変換済みファイルに再実行すると既存状態（`[x]` チェックボックスなど）が黙ってリセットされる。マージで新規ファイルが追加された後は、そのファイルのみにスクリプトを適用するか、冪等性を事前確認する。 |
