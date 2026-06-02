---
name: issue-resolve
description: |
  `.work/issues/` のレビュー済みイシューを上から自動的に消化する — 1 起動あたり対応可能なイシュー 1 件。
  `## 意思` が「対応する」のイシューは `work:issue-resolver` サブエージェントへ委譲し、ブランチを切って
  マージ待ち最終コミットまで進める。「対応しない」のイシューは共有 `chore/rejected-issues` ブランチで
  クローズする。`/loop` での実行を想定。トリガー: 「イシューを対応して」「イシューを消化して」
  「resolve issues」「issue-resolve」、または `/loop /work:issue-resolve` / `/work:issue-resolve` を
  明示的に呼び出したとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:issue-resolve — レビュー済みイシューを消化する（ループ駆動）

`work:issue-review` が捌いたイシューを処理する。`/loop` 実行を前提に、各起動で**最上位の対応可能な
イシュー 1 件**だけを処理する。ループの繰り返しでキューを消化し、ユーザーが確認・マージするための
マージ待ちブランチが積み上がる。

- **意思=対応する + status: not_started** → `work:issue-resolver` サブエージェント（1 イシュー 1
  サブエージェント）へ委譲。`work:start` でブランチを切り、修正を実装し、**マージ待ち最終コミット**で
  止まる（マージはユーザーが別途判断）。
- **意思=対応しない** → 共有 `chore/rejected-issues` ブランチで `wontfix` クローズ（ファイルは `closed/`
  へ移動）。ユーザーがそのブランチをマージするまで蓄積される。
- **意思=未記入**（未レビュー）と **意思=対応する + status: in_progress**（対応中。別セッションの
  可能性）→ スキップ。

イシューのフォーマット（フロントマター無し・2 分割）／ライフサイクルは `work-dir/イシュー.md`
（自動注入）が規定する — それに従う。`## 意思` の `**回答**:` は人間の自由記述で、「対応する／様子見」を
肯定、「対応しない」を否定と解釈する。

---

## 概要

- **前提**: イシューが `work:issue-review` で捌かれている（`## 意思` が記入済み）。
- **1 起動 = 対応可能イシュー 1 件**で、各ループ tick を 1 ブランチ／1 マージ単位に保つ。
- QA はレビュー時に（イシュー上で）解決済みなので、resolver サブエージェントは止まらず最終コミットまで
  到達できるはず。**真にブロックする事項が出たらサブエージェントは止まる**（Step 3 参照）。

---

## タスク

### Step 1: 最上位の対応可能イシューを探す

#### プロセス

1. `.work/issues/` が無ければ → 報告して停止。
2. `.work/issues/_index.yaml` を読む。`status: not_started` のエントリをイシュー番号の昇順で
   収集する。これが開く候補ファイルの全て。
3. 候補を上から走査する。各エントリのイシューファイルを開き `## 意思` の `**回答**:` を読む：
   - `## 意思` = 否定（対応しない）→ REJECT アクション（Step 2）。
   - `## 意思` = 肯定（対応する／様子見）→ ACCEPT アクション（Step 3）。
   - `## 意思` 未記入（未レビュー）→ スキップ。
4. 対応可能イシューが無ければ → 「対応可能なイシューはありません」と報告して停止（ループ終了可）。

→ Reject → Step 2 ／ Accept → Step 3

---

### Step 2: REJECT — 共有 `chore/rejected-issues` ブランチでクローズ

#### プロセス

1. 共有 reject ブランチ + ワークツリーの存在を確認：
   - `git worktree list` に `chore/rejected-issues` があるか。
   - **無ければ**: `/work:start`（type `chore`、title `rejected-issues`）で作成する。そのブランチ文書には
     唯一の目的を記す — *「reject されたイシューを `closed/` へ退避するための集約ブランチ。マージすると
     リジェクトが確定する」* — そして各クローズ済み reject を追記するテーブルを持たせる。これにより
     意図がセッションをまたいでも残る（さもないとコンテキストが失われる）。
2. reject ワークツリー内でイシューをクローズ（イシューファイルは git 管理対象でそこに存在する）：
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" close \
     --issues-dir {REJECT_WT}/.work/issues \
     --issue-id ISSUE-{N} \
     --resolution wontfix \
     --linked-branch chore/rejected-issues
   ```
   `ISSUE-{N}.md` を `closed/` へ移動し、`_index.archive.yaml` に `wontfix` 記録を追記する。
3. reject ブランチ文書にイシュー ID・タイトル・reject 理由（イシューの `## 自由記述` / `## 意思` の回答から）
   の行を追記。
4. `chore/rejected-issues` でコミット（イシュー移動 + ブランチ文書）。**マージはしない** — ユーザーが
   準備できたら行う。

→ Step 4 へ

#### 注記

- reject を `master` でクローズしない — 移動／archive はブランチ上でコミットする必要がある
  （master 直コミットはガードされる）。共有 chore ブランチが全 reject を 1 マージ単位にまとめる。

---

### Step 3: ACCEPT — `work:issue-resolver` サブエージェントを委譲

#### プロセス

1. 委譲前に、**メインリポジトリ**の `_index.yaml` でイシューを in-progress にする（セッション横断ロック）：
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" set-status \
     --issues-dir .work/issues --issue-id ISSUE-{N} --status in_progress
   ```
2. **イシューの難易度でサブエージェントのモデルを選ぶ**（オーケストレーターであるあなたが判断し、
   Agent ツールの `model` パラメータで渡す。エージェント自体はモデルを固定しない）：
   - **簡単／局所的**（単一ファイル編集、ドキュメント/typo/リネーム、狭いスコープ）→ `model: sonnet`
   - **難しい／複雑**（横断的変更、込み入ったロジック、複数ファイル、リスキーなリファクタ）→ `model: opus`
   - **`haiku` は絶対に使わない。**
   判断材料はイシューの `## 概要` / `## 対応案` のスコープ。迷ったら `opus`。
3. このイシュー用に `work:issue-resolver` サブエージェント（エージェントタイプ `work:issue-resolver`、
   上で選んだ `model` 付き）を**1 つ**委譲する。渡す情報: `ISSUE-{N}` の id とパス、確定した方針
   （`## 対応案` の採用案〔`## QA` の回答で確定〕 + `## 自由記述` の回答）、そして**マージ待ち最終コミット**まで
   ブランチを進める指示（マージはしない）。
4. サブエージェントの返却時：
   - **完了（マージ待ち）** → 作成したブランチを記録。ユーザーが後でマージする。
   - **ブロック**（イシューで事前解決されなかった真の未決事項）→ サブエージェントがブロッカーを
     イシューの `# ユーザー回答欄` の `## QA` に記録して差し戻している。インデックスのロックを戻す：
     ```bash
     python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" set-status \
       --issues-dir .work/issues --issue-id ISSUE-{N} --status not_started
     ```
     ブロッカーをユーザーに提示する（再度 `work:issue-review` が必要）。

→ Step 4 へ

#### 注記

- 1 イシュー 1 サブエージェント（= 1 ブランチ）。`/loop` 下では次の tick が次のイシューを拾う。
- ワークツリー／ブランチ／コミットはサブエージェントが `work:start` 経由で所有する。本オーケストレーターは
  選択・ロック・委譲・報告のみ。

---

### Step 4: 報告

#### プロセス

1. この起動で何をしたか報告: 処理したイシュー、アクション（accept→ブランチ / reject→closed）、ブランチ名。
   ユーザー向けに残ったもの（マージ待ちブランチ、提示したブロッカー）を列挙。
2. `/loop` 下では、ループが再起動して次のイシューを処理する。
