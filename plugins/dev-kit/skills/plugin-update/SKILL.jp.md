---
name: plugin-update
description: |
  カレントプロジェクトに展開済みの dev-kit 生成物を、現在インストールされている dev-kit の
  バージョンに合わせて更新する: html-implement が配布する `.claude/rules/` 内ルールテンプレと、
  html-debug-fab が配布する `uidev.css` / `uidev.js` / `CLAUDE.md` を再コピーする。
  他プラグインの生成物は対象外。
  手動起動のみ — `/dev-kit:plugin-update` を使う。
---
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# dev-kit:plugin-update — dev-kit 生成物を最新版に揃える

スコープは **dev-kit がプロジェクトに静的にコピーする成果物**のみ:

- `html-implement` がプロジェクトの `.claude/rules/` に配布する HTML 系ルールテンプレ
- `html-debug-fab` がプロジェクトの静的アセットディレクトリに配布するデバッグウィジェット (`uidev.css` / `uidev.js` / `CLAUDE.md`)

`py-script` / `py-project` / `next-implement` / `next-plan` / `yaml` 系は ref-injection 方式で
プロジェクトに静的成果物を配布しないため対象外。`references/` や `injection_rules.yaml` など
プラグイン本体の内側で完結するファイルも対象外。

他プラグインの生成物には絶対に手を出さない（各プラグインが自分の `plugin-update` を持つ）。

---

## 同期対象一覧

| ソース (`{dev_kit_root}/`) | 配布先 |
|---|---|
| `templates/html/rules/css-js-link.md` | `.claude/rules/css-js-link.md` |
| `templates/html/rules/css-js-link.jp.md` | `.claude/rules-jp/css-js-link.md`（`.jp.` を落とす） |
| `templates/html/rules/common-component-first.md` | `.claude/rules/common-component-first.md` |
| `templates/html/rules/common-component-first.jp.md` | `.claude/rules-jp/common-component-first.md`（同上） |
| `skills/html-debug-fab/templates/uidev.css` | プロジェクトの静的アセットディレクトリ |
| | `uidev.js` も同ディレクトリ |
| | `CLAUDE.md` も同ディレクトリ |
| | `CLAUDE.jp.md` も同ディレクトリ |

`{dev_kit_root}` = `${CLAUDE_PLUGIN_ROOT}`（このスキル実行時に dev-kit プラグインへ解決される）。

---

## 作業内容

### ステップ1: PR ブランチを準備する

#### 条件

- 常に — 最初に実行

#### 処理内容

1. カレントプロジェクトに workspace プラグインの `.work/` ディレクトリが存在するか確認する
2. **存在する場合**:
   - `/workspace:work-start` を実行してこの同期作業専用の PR ブランチを切る
   - ワークツリーとブランチが作成されるのを待つ
3. **存在しない場合**:
   - ユーザーに「workspace プラグインが未導入です。現在のブランチに直接コミットしますがよろしいですか?」と確認し、了承を得てから進む

→ ステップ2 へ

#### 出力

- 以降のファイル編集とコミットを行うブランチ（PR ブランチまたは現在のブランチ）が確定している

---

### ステップ2: html-implement のルールテンプレを上書きする

#### 条件

- ステップ1 完了

#### 処理内容

1. 配布先が存在するかで html-implement の利用有無を判定する
   - `.claude/rules/css-js-link.md` が **存在しない** 場合 → html-implement 未使用と判断し、本ステップをスキップしてステップ3 へ
2. 利用済みの場合、上記表の html-implement 行 4 ファイルを `${CLAUDE_PLUGIN_ROOT}/templates/html/rules/*` からコピー上書きする
3. 上書きしたファイル名を報告する

→ ステップ3 へ

#### 出力

- `.claude/rules/{css-js-link,common-component-first}.md` と `.claude/rules-jp/{css-js-link,common-component-first}.md` が最新のテンプレ内容に揃っている

---

### ステップ3: html-debug-fab のウィジェットを上書きする

#### 条件

- ステップ2 完了

#### 処理内容

1. プロジェクト内の既存 `uidev.css` の場所を検索する
   - 例: `find . -name 'uidev.css' -not -path '*/node_modules/*' -not -path '*/.git/*'`
2. **見つからない場合** → html-debug-fab 未配布と判断し、本ステップをスキップしてステップ4 へ
3. **1 箇所のみ見つかった場合** → そのディレクトリを配布先として確定する
4. **複数見つかった場合** → ユーザーに対象ディレクトリを確認してから進む
5. 配布先ディレクトリに対して、`${CLAUDE_PLUGIN_ROOT}/skills/html-debug-fab/templates/` の以下 4 ファイルをコピー上書きする
   - `uidev.css`
   - `uidev.js`
   - `CLAUDE.md`
   - `CLAUDE.jp.md`
6. `example.html` はサンプル用途のためコピーしない
7. 上書きしたファイル名を報告する

→ ステップ4 へ

#### 出力

- 配布先ディレクトリの `uidev.css` / `uidev.js` / `CLAUDE.md` / `CLAUDE.jp.md` が最新のテンプレ内容に揃っている

---

### ステップ4: レビューしてコミットする

#### 条件

- ステップ3 完了

#### 処理内容

1. `git status` と `git diff` をユーザーに見せる
2. 差分が無ければ「すべての dev-kit 生成物は既に最新です」と報告して終了する
3. 差分があれば、まとめてコミットする
   - workspace を経由した場合: `chore: sync dev-kit templates to v{N} #PR{N}`
   - 経由しなかった場合: `chore: sync dev-kit templates to v{N}`
4. dev-kit の現在バージョンは `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` から取得する

→ ステップ5 へ

#### 注意

##### 禁止事項

- master ブランチに直接コミットしない（workspace 経由なら PR ブランチに、未導入なら現在のブランチに）

---

### ステップ5: 完了報告

#### 条件

- ステップ4 完了

#### 処理内容

1. 上書きしたファイルを全件列挙する
2. 差分が無かった場合は「全成果物は既に最新です」と明示する
3. workspace 経由の場合は `/workspace:merge` の実行を案内する

→ 完了
