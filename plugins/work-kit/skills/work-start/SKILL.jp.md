# SKILL.jp.md — work-kit:work-start スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: work-start
**トリガー**: ユーザーが「新しい PR を作って」「新しい作業を始めたい」「work-start して」と言ったとき

---

## 概要

新規 PR 作業を開始するスキル。
ワークツリーとブランチを作成し、PR タスクドキュメントと index.yaml エントリを準備する。

---

## 作業内容

### ステップ1: 次の PR 番号を決定する

#### 条件

- 常に — 最初に実行する

#### 処理内容

1. `docs/tasks/index.yaml` を読む
2. `prs` リストの最大 `id` + 1 を次の PR 番号とする
3. リストが空なら PR 番号は 1 とする

→ ステップ2へ進む

#### 出力

- 次の PR 番号（例: 171）

---

### ステップ2: PR 情報を収集する

#### 条件

- ステップ1が完了していること

#### 処理内容

1. ユーザーに以下を確認する:
   - **タイプ**: `feat` / `fix` / `refactor` / `docs` / `chore` / `test`
   - **説明**: kebab-case の短い説明（例: `add-bgm-feature`）
   - **サマリー**: PR の概要（1行）
   - **作業内容**: 今回やることのリスト（チェックリスト用）

→ ステップ3へ進む

#### 出力

- PR タイプ・説明・サマリー・作業内容リスト

---

### ステップ3: ワークツリーとブランチを作成する

#### 条件

- ステップ2が完了していること

#### 処理内容

1. ワークツリーを作成する:

```bash
git worktree add -b PR{N}/{type}/{description} ../$(basename $(pwd))-wt-PR{N}
```

→ ステップ4へ進む

#### 出力

- ワークツリーが `../repo-wt-PR{N}` に作成済み
- ブランチ `PR{N}/{type}/{description}` が存在する

#### 補足

##### 禁止事項

- メインリポジトリのブランチ（master/main）に直接コミットしない

---

### ステップ4: PR タスクドキュメントを作成する

#### 条件

- ステップ3が完了していること

#### 処理内容

1. タスクフォルダを作成する: `docs/tasks/{YYYYMMDD}_{description}/`
2. PR ドキュメントを作成する: `docs/tasks/{YYYYMMDD}_{description}/PR{N}.md`

テンプレート:

```markdown
# PR{N} — {summary}

## 概要

{summary}

## 作業内容

{checklist items as - [ ] }

## 変更ファイル

<!-- コミット後に追記する -->
```

→ ステップ5へ進む

#### 出力

- `docs/tasks/{YYYYMMDD}_{description}/PR{N}.md` 作成済み

---

### ステップ5: index.yaml にエントリを追加する

#### 条件

- ステップ4が完了していること

#### 処理内容

1. `docs/tasks/index.yaml` の `prs` リストに以下を追記する:

```yaml
- id: {N}
  title: 'PR{N} — {summary}'
  type: {type}
  tags: []
  summary: '{summary}'
  completed: false
  task: '{YYYYMMDD}_{description}'
```

→ ステップ6へ進む

#### 出力

- `docs/tasks/index.yaml` に PR エントリが追加済み

---

### ステップ6: ユーザーに報告して承認を待つ

#### 処理内容

1. 作成した内容を報告する:
   - ブランチ名
   - ワークツリーパス
   - PR ドキュメントパス
2. ユーザーの承認を待ってから実装を開始する

#### 出力

- ユーザーが内容を確認・承認済み

#### 補足

##### 禁止事項

- ユーザーの明示的な承認なしに実装を開始しない
