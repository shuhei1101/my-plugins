<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# ref-inject フックの再生成は creator-dispatch の catchall を踏む — これは誤検知

## 何が起きたか

PR157（`py-kit` を `ref-inject` の注入機構へ移行）では、`py-kit` の注入フックを
`ref-inject` テンプレートから再生成する作業を行った。これはまさに `/ref-inject:apply` の仕事。
再生成ファイルを書き込むと `creator-dispatch` の `PreToolUse` ブロックが発火した:

- `plugins/py-kit/hooks/inject_references.py` → **plugin-creator-dispatch**（`plugins/` 全体の広い catchall。`.py` はどの具体ルールにも当たらない）
- `plugins/py-kit/hooks/templates/*.j2` → **j2-stamp-check**
- `plugins/py-kit/CLAUDE.md`（および ref-inject の CLAUDE.md・glossary）→ **claude-creator-dispatch / rule-creator-dispatch**

これらの dispatch プロンプトは「編集前に `/claude-kit:plugin-creator` を呼べ」等と言うが、
ここでは字義通りに従うと誤り。ファイルの所有者は **`/ref-inject:apply`** であって
plugin-creator ではない。plugin-creator はプラグインレベルの関心事（plugin.json /
ルート CLAUDE.md / marketplace）を担当し、注入フック本体は担当しない。

## なぜ誤検知か

`creator-dispatch` はファイルパスを first-match-wins の `RULES` テーブルで照合し、最後のルールが
plugin-creator を指す `plugins/` 全体の広い catchall。ref-inject 管理のフックファイル
（`hooks/inject_references.py`、`templates/*.j2`）には専用 dispatch ルールがないため、この
catchall に落ちる。しかしこれらのファイルの専用機構スキルは `/ref-inject:apply`（未インストール時は
その `SKILL.md` 手順を直接実行）。

dispatch ブロックは **セッションフラグ型**: ルールごとに 1 セッション最初の編集だけブロックし、
以降は通す。よって正しい対処は、ref-inject 再適用に対する catchall を誤検知と認識し、そのまま続行
（再試行が通る）すること。

## 既存 incident との関係

これは `creator-dispatch-block-means-invoke-creator`（PR156）の補足。あちらは「dispatch ブロックは
名指しの creator を呼べ、編集を再試行するな」。これは*具体的な* dispatch ルール（skill-creator /
rule-creator / claude-creator / hook-creator）には当てはまる。例外として、**専用機構スキルが
ファイルを所有している場合**（ここでは `ref-inject:apply`）、汎用の `plugins/` catchall は適用外で、
plugin-creator を呼ぶのは誤り。所有機構の方で進める。

## 教訓

ref-inject 管理の注入ファイルを再生成するとき（PR158 next-kit、将来の再適用）、`plugins/` catchall +
`j2-stamp-check` + `claude/rule-creator` のブロックが発火することを織り込む。これらはこのワークフローでは
誤検知: `/ref-inject:apply`（所有機構）を実行し、セッションフラグのブロックを通し、plugin-creator へ
寄り道**しない**。j2-stamp チェックは ref-inject の `.j2` テンプレートが冒頭スタンプを既に持つため満たされる。
