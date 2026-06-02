---
name: work:issue-resolve
description: |
  `.work/issues/` のレビュー済みイシューを上から自動的に消化する — 1 起動あたり最大
  `${ISSUE_RESOLVE_AGENTS}`（デフォルト: `1`）件のイシューを順番に処理する。
  `## 意思` が「対応する」のイシューは `work:issue-resolver` サブエージェントへ委譲し、ブランチを切って
  マージ待ち最終コミットまで進める。「対応しない」のイシューは使い捨ての 1 イシュー専用ブランチで
  クローズし、同一起動内で即 master へマージする。`/loop` での実行を想定。トリガー: 「イシューを対応して」「イシューを消化して」
  「resolve issues」「issue-resolve」、または `/loop /work:issue-resolve` / `/work:issue-resolve` を
  明示的に呼び出したとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:issue-resolve — レビュー済みイシューを消化する（ループ駆動）

`work:issue-review` が捌いたイシューを処理する。`/loop` 実行を前提に、各起動で最大 **N 件のアクション
可能なイシュー**（`${ISSUE_RESOLVE_AGENTS}`、デフォルト `1`）を上から順番に処理する。ループの繰り返しで
キューを消化し、（accept 由来の）マージ待ちブランチがユーザーの確認・マージ用に積み上がる。

- **意思=対応する + status: not_started** → `work:issue-resolver` サブエージェント（1 イシュー 1
  サブエージェント）へ委譲。ブランチを切り、修正を実装し、`direct_merge` の値に応じて master へ直接
  マージするか、マージ待ち最終コミットで止まる。
- **意思=対応しない** → 使い捨ての 1 イシュー専用ブランチで `wontfix` クローズ（ファイルは `closed/`
  へ移動）し、同一起動内で**即 master へマージ**する。蓄積されないため、イシューインデックスと master が
  乖離しない。（reject は純粋なステータス変更なので即確定して安全。accept は実作業なので従来どおり
  ユーザーのマージを待つ。）
- **意思=未チェック**（未レビュー＝全チェックボックスが `- [ ]`）と **意思=対応する + status: in_progress**
  （対応中。別セッションの可能性）→ スキップ。

イシューのフォーマット（フロントマター無し・回答欄が先頭）／ライフサイクルは `work-dir/イシュー.md`
（自動注入）が規定する — それに従う。`## 意思` のチェックボックスは AI が解釈し、`- [x] 対応する` を
肯定、`- [x] 対応しない` を否定とみなす。全て未チェック（`- [ ]`）なら未レビュー扱い。

---

## 概要

- **前提**: イシューが `work:issue-review` で捌かれている（`## 意思` が記入済み）。
- **1 起動 = 最大 N 件**（`${ISSUE_RESOLVE_AGENTS}`、デフォルト `1`）— イシューを順番に処理し、
  各処理単位（ブランチ / クローズ）をアトミックかつ追跡可能に保つ。
- QA はレビュー時に（イシュー上で）解決済みなので、resolver サブエージェントは止まらず最終コミットまで
  到達できるはず。**真にブロックする事項が出たらサブエージェントは止まる**（Step 3 参照）。

**環境変数**:
- `${ISSUE_RESOLVE_AGENTS}`（デフォルト: `1`）— 1 起動で処理するアクション可能なイシューの最大件数。
  イシューはイシュー番号の昇順で 1 件ずつ処理する。

---

## タスク

### Step 1: 最上位の対応可能イシューを探す

#### プロセス

1. `${ISSUE_RESOLVE_AGENTS}`（デフォルト `1`）を読み `N` とする。`handled = 0` で初期化する。
2. `.work/issues/` が無ければ → 報告して停止。
3. `.work/issues/_index.yaml` を読む。`status: not_started` のエントリをイシュー番号の昇順で
   収集する。これが開く候補ファイルの全て。
4. 候補を上から走査する。各エントリのイシューファイルを開き `## 意思` のチェックボックスを読む：
   - `- [x] 対応しない` → REJECT アクション（Step 2）。
   - `- [x] 対応する` → ACCEPT アクション（Step 3）。
   - 全て `- [ ]`（未チェック＝未レビュー）→ スキップ。
5. 対応可能イシューが無ければ → 「対応可能なイシューはありません」と報告して停止（ループ終了可）。

→ Reject → Step 2 ／ Accept → Step 3

---

### Step 2: REJECT — 使い捨てブランチでクローズし即 master へマージ

これらはすべて**メインリポジトリ**（このオーケストレーターが動く場所。`master` 上）で実行する。
ワークツリーではない。close はメインリポの `_index.yaml`（gitignore・作業コピーごとに別物 —
Step 1 が読む正）を更新する必要があり、追跡変更（ファイル移動 + archive）は使い捨てブランチで
`master` へ運ぶ。開始前にメインリポの作業ツリーがクリーンであること。

#### プロセス

1. この reject 1 件専用の使い捨てブランチを作成して切り替える（タスク文書は作らない — この起動限り）：
   ```bash
   git switch -c chore/reject-ISSUE-{N}
   ```
2. **メインリポの `.work/issues`** でイシューをクローズ（相対パス — cwd はメインリポ）。
   `ISSUE-{N}.md` を `closed/` へ移動し、`_index.yaml` から該当エントリを削除し、
   `_index.archive.yaml` に `wontfix` 記録を追記する：
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" close \
     --issues-dir .work/issues \
     --issue-id ISSUE-{N} \
     --resolution wontfix \
     --linked-branch chore/reject-ISSUE-{N}
   ```
3. 追跡変更（ファイル移動 + `_index.archive.yaml`）を使い捨てブランチでコミットする。
   `_index.yaml` は gitignore なのでコミットされないが、そのエントリ削除状態は次のブランチ切替を
   跨いで残る（switch は gitignore ファイルに触れない）：
   ```bash
   git add .work/issues/
   git commit -m "chore: reject ISSUE-{N} ({title})"
   ```
4. `master` へ戻り、使い捨てブランチを `--no-ff` でマージしてから削除する：
   ```bash
   git switch master
   git merge --no-ff -m "chore: reject ISSUE-{N} ({title})" chore/reject-ISSUE-{N}
   git branch -d chore/reject-ISSUE-{N}
   ```
   `master` へのマージは `git-guard` に 1 回引っかかる — 確認してリトライを通す。（`master-commit-guard`
   はここでは発火しない: `git commit` のみにマッチし、マージコミットはそもそも対象外。）

→ Step 4 へ

#### 注記

- **なぜ即マージか**: reject は純粋なステータス変更（`closed/` へ移動 + archive 記録）なので、即確定
  すれば master とイシューインデックスが毎 tick で整合する。旧来の共有 `chore/rejected-issues` 蓄積
  ブランチは、メインリポの `_index.yaml`（エントリは `not_started` のまま）と未マージのファイル移動を
  乖離させていた — まさにこれが避けたい不整合。
- **なぜワークツリーでなくメインリポか**: 新規ワークツリーには `_index.yaml` が存在しない（gitignore で
  コミットされない）ため、close が正であるインデックスを更新できない。メインリポで close すれば
  `_index.yaml` を直接更新でき、その gitignore な編集は `master` 切替を生き残り、追跡変更はマージ
  コミットで `master` に届く。
- **`master` 上で `git commit` を直接行わない**（ガードされる）。close/archive は使い捨てブランチに載り、
  マージコミット経由でのみ `master` に届く。

---

### Step 3: ACCEPT — `work:issue-resolver` サブエージェントを委譲

#### プロセス

1. 委譲前に、**メインリポジトリ**の `_index.yaml` でイシューを in-progress にする（セッション横断ロック）：
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" set-status \
     --issues-dir .work/issues --issue-id ISSUE-{N} --status in_progress
   ```
2. **`direct_merge` の値を決定する**:
   1. `_index.yaml` の ISSUE-{N} エントリに `direct_merge` フィールドがあればその値を使う。
   2. なければイシュー本文を分析する:
      - UI・画面・ビジュアル・フロントエンド・ユーザー表示に関する記述がある → `direct_merge: false`
      - タイプが `refactor`・`test`・`docs`・`backend` かつ UI 要素の記述がない → `direct_merge: true`
      - 判断できない場合 → `direct_merge: true`（デフォルト）
3. **イシューの難易度でサブエージェントのモデルを選ぶ**（オーケストレーターであるあなたが判断し、
   Agent ツールの `model` パラメータで渡す。エージェント自体はモデルを固定しない）：
   - **簡単／局所的**（単一ファイル編集、ドキュメント/typo/リネーム、狭いスコープ）→ `model: sonnet`
   - **難しい／複雑**（横断的変更、込み入ったロジック、複数ファイル、リスキーなリファクタ）→ `model: opus`
   - **`haiku` は絶対に使わない。**
   判断材料はイシューの `## 概要` / `## 対応案` のスコープ。迷ったら `opus`。
4. このイシュー用に `work:issue-resolver` サブエージェント（エージェントタイプ `work:issue-resolver`、
   上で選んだ `model` 付き）を**1 つ**委譲する。渡す情報: `ISSUE-{N}` の id とパス、確定した方針
   （`## 対応案` の採用案〔`## QA` の回答で確定〕 + `## 意思` の回答にある inline 補足）、および
   上で決定した `direct_merge` の値。
5. サブエージェントの返却時：
   - **完了・直接マージ済み**（`direct_merge: true`）→ リゾルバーが既にマージ・イシュークローズ済み。
     ブランチを記録するのみ。
   - **完了・マージ待ち**（`direct_merge: false`）→ 作成したブランチを記録。ユーザーが後でマージする。
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

### イシュー間: N 件まで繰り返す

Step 2 または Step 3 で 1 件処理したら `handled` をインクリメントする。`handled < N` かつ候補リストが
残っていれば **Step 1 に戻る**（インデックスを再読み込みしてステータス変化を反映）し、次のイシューを処理
する。`handled == N` になるか対応可能イシューがなくなったら Step 4 へ進む。

---

### Step 4: 報告

#### プロセス

1. この起動で何をしたか報告: 処理したイシュー、アクション（accept+direct_merge→master へマージ済み /
   accept+no-direct_merge→マージ待ちブランチ / reject→closed かつ master へマージ済み）、ブランチ名。
   ユーザー向けに残ったもの（マージ待ちブランチ、提示したブロッカー）を列挙。
2. `/loop` 下では、ループが再起動して次のイシューを処理する。
