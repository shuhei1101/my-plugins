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
このスキルはどの他プラグインにも依存しない。ブランチ管理（PR ブランチを切る、コミットする、
マージするなど）はユーザーの責務。

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

### ステップ1: 現在のブランチを確認する

#### 条件

- 常に — 最初に実行

#### 処理内容

1. `git rev-parse --abbrev-ref HEAD` で現在のブランチを取得する
2. **master / main の場合** → 「master / main では実行できません。先に作業用ブランチを切ってから再実行してください」とユーザーに伝えて終了する
3. それ以外のブランチ → そのまま進む

→ ステップ2 へ

#### 出力

- 以降のファイル編集を行うブランチが master / main 以外であることが確定している

#### 注意

##### 禁止事項

- master / main ブランチ上での実行

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

### ステップ4: 差分を報告する

#### 条件

- ステップ3 完了

#### 処理内容

1. `git status` と `git diff` をユーザーに見せる
2. 差分が無ければ「すべての dev-kit 生成物は既に最新です」と報告して終了する
3. 差分があれば、上書きしたファイル一覧と提案コミットメッセージを提示し、コミットはユーザーに委ねる
   - 提案メッセージ例: `chore: sync dev-kit templates to v{N}`
   - dev-kit の現在バージョンは `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` から取得する
4. このスキルは自分ではコミットしない（コミット・マージはユーザーの責務）

→ 完了
