# SKILL.jp.md — work-kit:archive スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: archive
**トリガー**: ユーザーが「アーカイブして」「index をアーカイブしたい」「/work-kit:archive」と言ったとき
**注意**: ユーザーの明示的な指示があるときのみ実行する。

---

## 概要

`index.yaml` の完了済みエントリを `index.archive.yaml` に移し、git で管理するスキル。

- `index.yaml` はローカル管理（gitignore）のままにする
- `index.archive.yaml` は git 追跡対象として新規ブランチ経由でコミットする
- `.work/` ディレクトリ自体が gitignore されている場合はスキップする

---

## 作業内容

### ステップ1: 前提条件を確認する

#### 条件

- 常に — 最初に実行する

#### 処理内容

1. `.work/tasks/.gitignore` を確認し、`index.yaml` のみが除外対象か確認する
2. `.work/` 全体が gitignore されているか確認する:

```bash
git check-ignore -q .work/
```

   - exit 0（gitignore 対象）→ 「.work/ がリポジトリから除外されているためアーカイブをスキップします」と報告してスキルを終了する
   - exit 1（追跡対象）→ ステップ2へ進む

→ ステップ2へ進む

---

### ステップ2: trim スクリプトを実行する

#### 処理内容

1. 以下を実行して完了済みエントリを `index.archive.yaml` へ移動する:

```bash
python plugins/work-kit/scripts/trim-index.py .work/tasks/index.yaml
```

2. 「Nothing to archive」と出力された場合は「完了済みエントリがありません」と報告してスキルを終了する

→ ステップ3へ進む

---

### ステップ3: アーカイブブランチを作成してコミットする

#### 処理内容

1. 日付付きのブランチ名を決定する: `archive/trim-{YYYYMMDD}`
2. ワークツリーを作成する:

```bash
git worktree add -b archive/trim-{YYYYMMDD} ../$(basename $(pwd))-wt-archive
```

3. `index.archive.yaml` をワークツリーにコピーする:

```bash
cp .work/tasks/index.archive.yaml ../$(basename $(pwd))-wt-archive/.work/tasks/index.archive.yaml
```

4. ワークツリー内でコミットする:

```bash
cd ../$(basename $(pwd))-wt-archive
git add .work/tasks/index.archive.yaml
git commit -m "chore: archive completed PR entries to index.archive.yaml"
```

5. ワークツリーを削除する（ブランチは残す）:

```bash
git worktree remove ../$(basename $(pwd))-wt-archive
```

→ ステップ4へ進む

#### 補足

##### 禁止事項

- ワークツリーのルートで `Remove-Item -Recurse` や `rm -rf` を実行しない

---

### ステップ4: 完了報告

#### 処理内容

1. 以下を報告する:
   - アーカイブしたエントリ数
   - 作成したブランチ名: `archive/trim-{YYYYMMDD}`
2. 「`/work-kit:merge` でこのブランチをマージしてください」と案内する
