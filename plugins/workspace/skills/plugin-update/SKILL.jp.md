---
name: plugin-update
description: |
  カレントプロジェクトのプラグイン生成物を、現在インストール済みのプラグインバージョンに合わせて更新する:
  workspace の静的 `.work/` テンプレ（CLAUDE.md・.gitignore）を上書きし、
  `index.yaml` を最新スキーマへ移行する。他プラグインの生成物は対象外（各プラグインが
  同等のスキルを持っている場合はそれを使う）。
  手動起動のみ — `/workspace:plugin-update` を使う。
---
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# workspace:plugin-update — プラグイン生成物を最新版に揃える

旧 `update` スキルからの置き換え（PR168）。スコープは **workspace 自身の静的テンプレ**のみ:
`.work/CLAUDE.md`・`.gitignore`・`index.yaml` のスキーマ移行。

他プラグインの diff ロジックは意図的に対象外 — 各プラグインが自分の更新パスを所有し、
必要なら同等のスキル（仮: `/{plugin}:plugin-update`）を提供する。
このスキルは決してプラグイン境界を跨がない。

---

## 作業内容

### ステップ1: `.work/` の存在確認と作業ブランチの準備

#### 条件

- 常に — 最初に実行

#### 処理内容

1. カレントプロジェクトに `.work/` があることを確認する
2. なければユーザーに `/workspace:setup` を先に実行するよう伝えて終了する
3. `/workspace:work-start` を実行してこの同期作業専用の作業ブランチを切る
   （生成された編集が master でなくレビュー可能なブランチに載るようにするため）
4. ワークツリーとブランチが作成されるのを待つ

→ ステップ2 へ

#### 出力

- `.work/` の存在を確認した。作業ブランチ / ワークツリーが準備できている
- 以降のファイル編集とコミットはこのワークツリーの作業ブランチで行う

---

### ステップ2: `.work/` 配下の workspace テンプレートを上書きする

#### 条件

- ステップ1 完了

#### 処理内容

1. workspace テンプレートルートを特定: `${CLAUDE_PLUGIN_ROOT}/templates/.work/`
2. 以下のファイルをテンプレートからプロジェクトへコピー（上書き）:
   - `CLAUDE.md` → `.work/CLAUDE.md`
   - `CLAUDE.jp.md` → `.work/CLAUDE.jp.md`
   - `tasks/.gitignore` → `.work/tasks/.gitignore`
   - `issues/.gitignore` → `.work/issues/.gitignore`（テンプレ側に存在する場合）
3. 上書きしたファイルを報告する

→ ステップ3 へ

#### 出力

- `.work/CLAUDE.md`・`.work/CLAUDE.jp.md`・`.work/tasks/.gitignore` が最新になっている

---

### ステップ3: `.work/tasks/index.yaml` を移行する（`last_id` がなければ追加）

#### 条件

- ステップ2 完了
- `.work/tasks/index.yaml` が存在する

#### 処理内容

1. `.work/tasks/index.yaml` を読む
2. `last_id` が既にあればこのステップをスキップ
3. `last_id` がなければ:
   - `last_id` = 全エントリの `max(id)`（空なら 0）を計算
   - `prs` セクションの先頭に `last_id: {N}` を追加
   - ファイルを書き戻す

→ ステップ4 へ

#### 出力

- `index.yaml` に `last_id` が存在する
- 既にあった場合は「index.yaml には既に last_id があります — スキップ」と報告

#### 補足

- `index.yaml` は gitignore 済み — コミット不要
- このスキルが行うスキーマ移行はこれだけ。より深い書き換えは破壊的バージョンバンプ時の専用スクリプトに任せる

---

### ステップ4: レビューしてコミットする

#### 条件

- ステップ3 完了

#### 処理内容

1. ワークツリーの `git status` と `git diff` をユーザーに見せる
2. 意味のある単位でコミットする:
   - `chore: sync workspace .work/ templates to v{version}`

→ ステップ5 へ

---

### ステップ5: 完了報告

#### 処理内容

1. 更新したファイルを列挙する
2. 変更がなければ「workspace 関連の生成物はすべて最新です」と報告する
3. 同期ブランチの準備ができたら `/workspace:merge` を実行することをユーザーに提案する

→ 完了
