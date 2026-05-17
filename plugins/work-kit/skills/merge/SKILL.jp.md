# SKILL.jp.md — work-kit:merge スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: merge
**トリガー**: ユーザーが「マージして」「PR をマージしたい」「merge して」と言ったとき
**注意**: ユーザーの明示的な指示があるときのみ実行する。自動的に起動してはいけない。

---

## 概要

PR のマージフローを実行するスキル。
TODO 確認 → index アーカイブ → `--no-ff` マージ → ワークツリークリーンアップ → ドキュメント更新を行う。

---

## 作業内容

### ステップ1: マージ対象の PR を特定する

#### 条件

- 常に — 最初に実行する

#### 処理内容

1. 以下を実行してアクティブな PR 一覧を取得する:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py list-active .work/tasks/index.yaml
```

   出力形式: `id|title|type|task`（1行1PR）
2. 複数ある場合はユーザーにどれをマージするか確認する
3. 対応するブランチ名を特定する: `PR{N}/{type}/{title}`

→ ステップ2へ進む

#### 出力

- マージ対象の PR 番号・TODO.md パス・ブランチ名が確定している

---

### ステップ2: 作業内容テーブルを確認する

#### 条件

- ステップ1が完了していること

#### 処理内容

1. `.work/tasks/{date}_{title}/PR{N}/TODO.md` の `## 作業内容` テーブルを読む
2. 全行の「完了」列が `済` であることを確認する

→ 全て `済` ならステップ3へ進む

#### 補足

##### 条件分岐

- 未完了行がある → マージせずユーザーに報告し停止する

---

### ステップ3: 完了済みエントリをアーカイブする

#### 処理内容

1. `${CLAUDE_PLUGIN_ROOT}/scripts/trim-index.py` が存在しない場合はこのステップをスキップする
2. 完了済みエントリを `index.yaml` から `index.archive.yaml` へ移動する:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/trim-index.py .work/tasks/index.yaml
```

3. 「Nothing to archive」と出力された場合は以下のコミットをスキップする
4. `index.archive.yaml` が作成・更新された場合は、**ワークツリー（PR ブランチ）にコピーしてコミットする**:

```bash
cp .work/tasks/index.archive.yaml ../$(basename $(pwd))-wt-PR{N}/.work/tasks/index.archive.yaml
git -C ../$(basename $(pwd))-wt-PR{N} add .work/tasks/index.archive.yaml
git -C ../$(basename $(pwd))-wt-PR{N} commit -m "chore: archive completed PR entries"
```

→ ステップ4へ進む

#### 補足

- `index.yaml` は gitignore 対象のためコミット不要
- `index.archive.yaml` は git 追跡対象 — master に直接コミットするのではなく、マージ対象の PR ブランチにコミットする（ステップ4のマージに含まれる）

---

### ステップ4: マージを実行する

#### 処理内容

1. メインブランチにいることを確認する
2. `--no-ff` でマージする:

```bash
git merge --no-ff -m "{type}: {title} #PR{N}" PR{N}/{type}/{title}
```

→ ステップ5へ進む

---

### ステップ5: ワークツリーとブランチを削除する

#### 処理内容

1. ワークツリーを削除する:

```bash
git worktree remove ../$(basename $(pwd))-wt-PR{N}
git branch -d PR{N}/{type}/{title}
```

→ ステップ6へ進む

#### 補足

##### 禁止事項

- ワークツリーのルートで `Remove-Item -Recurse` や `rm -rf` を実行しない
  （Junction を辿ってメインリポジトリのファイルを破壊する）

---

### ステップ6: ドキュメントを更新する

#### 処理内容

1. `.work/tasks/{date}_{title}/PR{N}/QA.md` を確認し、未解決エントリがあればユーザーに確認する
2. 変更があればコミットする:

```bash
git add .work/
git commit -m "docs: PR{N} マージ後ドキュメント更新"
```

→ ステップ7へ進む

---

### ステップ7: 完了報告

#### 処理内容

1. マージ完了をユーザーに報告する
2. `.work/tasks/` に残っている進行中 PR があれば提示する

#### 補足

##### チェックリスト

- [ ] マージコミットが存在する
- [ ] ワークツリーとブランチが削除済み
- [ ] QA.md が更新済み
- [ ] index.archive.yaml がコミット済み（trim-index.py があり対象エントリが存在した場合）
