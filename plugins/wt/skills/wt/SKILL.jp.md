# SKILL.jp.md — wt スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: wt
**トリガー**: 新しい実装を始めたい・PR を作りたい・新しいブランチで作業したい・worktree セッションを再開したい・並行開発を管理したいときに自動起動

---

# wt — Git Worktree 実装ワークフロー

1 セッション = 1 PR。コード実装でもドキュメント更新でも、すべての作業は専用の worktree・専用ブランチ上で行う。複数の AI セッションが互いに干渉するのを防ぐためです。

---

## 概要

ライフサイクル：**計画 → セットアップ → 実装 → レビュー → マージ → クリーンアップ**

実装中のファイル書き込みはすべて worktree 内で行う。メインリポジトリには実装中は触れない。

---

## 作業内容

### ステップ1: 計画

#### 条件

- ユーザーが新しいタスクや PR を始めたいとき

#### 入力

- ユーザーのタスク説明

#### 処理内容

1. `README.md` を読み、`docs/` があればスキャンしてプロジェクトを把握する。要件が不明な場合は作業前に確認する。
2. PR 番号を決める：
   - `docs/PR/` にある既存ファイルを確認して最大の PR 番号を調べる
   - 次の番号 = max + 1。`docs/PR/` がなければ作成する
3. `docs/PR/PR{N}.md` を作成する：

```markdown
## 概要
{このPRが何をするかを1行で}

## 作業内容
- [ ] {タスク1}
- [ ] {タスク2}

## 実装
| 追加/編集 | ファイルパス | クラス.メソッド | 変更内容 |
|-----------|-------------|----------------|---------|
| 追加 | src/foo.py | Foo.bar | 新規メソッド |
| 編集 | src/main.py | main | Foo.bar の呼び出し追加 |

## テスト
| 追加/編集 | ファイルパス | テスト対象ファイル | クラス.メソッド | 変更内容 |
|-----------|-------------|-----------------|----------------|---------|
| 追加 | tests/test_foo.py | src/foo.py | TestFoo.test_bar | bar のテスト |
```

オプションセクション：`## 設計メモ`、`## 依存関係`、`## リスク`、`## ユーザー確認事項`

4. ブランチや worktree を作成する前に、ユーザーに計画を確認する。

→ ステップ2へ進む

#### 出力

- `docs/PR/PR{N}.md` 作成済み
- ユーザーが計画を承認済み

---

### ステップ2: worktree のセットアップ

#### 条件

- ステップ1でユーザーが計画を承認済みであること

#### 入力

- PR 番号とベースブランチ

#### 処理内容

1. ベースブランチとクリーンな状態を確認する：
   ```bash
   git branch --show-current
   git status
   ```
   未コミット変更がある場合や `master`/`main` ブランチの場合は警告する。

2. ブランチ名を決める — `PR{N}/{type}/{内容}` 形式：
   - `type` は Conventional Commits に従う：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`
   - スペース・特殊文字はハイフンに変換
   - `git branch --list {ブランチ名}` で衝突チェック

3. ブランチと worktree を作成する：
   ```bash
   git branch {ブランチ名} {ベースブランチ}
   git worktree add {worktreeパス} {ブランチ名}
   ```
   デフォルトパス：`{親ディレクトリ}/{リポジトリ名}-wt-PR{N}`

4. 依存関係をシンボリックリンクで接続（対象が存在しない場合はスキップ）：
   - Python プロジェクト：`ln -s {メインリポジトリ}/venv {worktree}/venv`
   - Node.js プロジェクト：`node_modules` と `.next`（あれば）をシンボリックリンク
   - シンボリックリンクが作れない場合：`PYTHONPATH` でメインリポジトリの venv を流用する（参考資料参照）

5. worktree 内で初期コミットを作成する：
   ```bash
   git commit --allow-empty -m "chore: start PR{N} {内容}"
   git add docs/PR/PR{N}.md
   git commit -m "docs: add PR{N} plan"
   ```

6. セッション状態を保存する（`~/.claude/skill-memory/worktree/{YYYYMMDDHHMMSS}_session.md`）：
   ```
   ベースブランチ、worktree パス、PR 番号、現在のフェーズ
   ```

→ ステップ3へ進む

#### 出力

- `{worktreeパス}` に worktree 作成済み
- ブランチ `PR{N}/{type}/{内容}` 準備完了
- セッション状態保存済み

---

### ステップ3: 実装

#### 条件

- ステップ2で worktree のセットアップが完了していること

#### 入力

- `docs/PR/PR{N}.md` のタスクリスト

#### 処理内容

1. すべての作業は worktree ディレクトリ内で行う — 実装中はメインリポジトリに触れない。
2. `docs/PR/PR{N}.md` のタスクリストを進捗に合わせてチェックしていく。
3. Conventional Commits 形式でコミットする：
   ```bash
   git add {ファイル}
   git commit -m "feat: JWT 認証を実装"
   ```
   タイプ：`feat` / `fix` / `refactor` / `docs` / `test` / `chore`
4. フェーズの区切りごとに `~/.claude/skill-memory/worktree/` のセッションファイルを更新する。

→ すべてのタスクにチェックが入ったらステップ4へ進む

#### 出力

- すべてのタスクが worktree 内でコミット済み

#### 補足

##### 禁止事項

- worktree 内で `pip install -e .` を実行しない — メインリポジトリのパッケージが worktree の `src/` を参照するようになり、worktree 削除後にメインサーバーが壊れる

##### gitignore 対象ファイルのルール

`.gitignore` に含まれるファイル（`config/settings.yaml`、`.env` など）はメインリポジトリで直接編集する。worktree 内のこれらのファイルへの変更は `git worktree remove` の実行時に消えてしまう。

具体的な手順：PR で `settings.yaml` に新しいキーを追加する場合は、メインリポジトリの `settings.yaml` を直接編集し、worktree 内では `settings.yaml.sample`（git 管理下）のみ編集する。

---

### ステップ4: レビューとマージ

#### 条件

- ステップ3のすべてのタスクが完了してコミット済みであること

#### 処理内容

1. worktree パスをユーザーに伝えて実装内容の確認を依頼する：
   ```
   変更内容を以下の worktree で確認してください: {worktreeパス}
   ```
2. ユーザーが修正を求めた場合 → ステップ3に戻る。
3. ユーザーがレビュー完了を確認したら、以下のみを出力する：
   ```
   コミット完了 — PR{N}: {変更内容の1行説明}
   ```
   以降は何もしない。**マージコマンドを表示しない。**「マージしますか？」と聞かない。マージはユーザーが自分のターミナルで実行する：
   ```bash
   git checkout {ベースブランチ}
   git merge --no-ff {ブランチ名}   # --no-ff でブランチ線がログに残る
   ```
4. ユーザーがマージ完了を伝えるまで待つ。

→ ステップ5へ進む

#### 出力

- ユーザーがブランチをベースブランチにマージ済み

#### 補足

##### 禁止事項

- `--squash` は絶対に使わない — ブランチをログに残すため、必ず `--no-ff` を使ってマージコミットを作る

---

### ステップ5: クリーンアップ

#### 条件

- ユーザーがマージ完了を確認済みであること

#### 処理内容

1. worktree とブランチを削除する：
   ```bash
   git worktree remove {worktreeパス}
   git branch -d {ブランチ名}
   ```
2. セッションファイルを更新する：`## ステータス: 完了`

→ 完了

#### 出力

- worktree とブランチが削除済み
- セッションが完了とマーク済み

#### 補足

##### 禁止事項

- リモートへの push は常にユーザーの責任 — このスキルでは `git push` を実行しない

---

## 参考資料

### worktree からのサーバー起動と venv の扱い

**worktree 内で `pip install -e .` を実行しない。** 代わりに `PYTHONPATH` を使う：

```powershell
$env:PORT = "809{N}"
$env:PYTHONPATH = "{worktreeパス}\src"
{メインリポジトリ}\.venv\Scripts\python.exe -m {package_name}
```

worktree サーバーをクリーンアップ前に停止するとき：

```powershell
$port = 8091
$p = (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue).OwningProcess
if ($p) { Stop-Process -Id $p -Force }
```

### セッションの再開

1. `~/.claude/skill-memory/worktree/` から該当セッションファイルを読み込む
2. `## 現在のステータス` で最後に完了したステップを確認する
3. `git worktree list` で worktree がまだ存在するか確認する
4. 該当ステップから作業を再開する

### Git コマンドリファレンス

```bash
# worktree 一覧
git worktree list

# カレントブランチ
git branch --show-current

# 未コミット変更の確認
git status

# ブランチ + worktree の作成
git branch PR{N}/{type}/{内容} {ベースブランチ}
git worktree add {パス} PR{N}/{type}/{内容}

# 空の初期コミット
git commit --allow-empty -m "chore: start PR{N} {内容}"

# マージ（worktree ではなくメインリポジトリで実行）
git checkout {ベースブランチ}
git merge --no-ff {ブランチ名}

# クリーンアップ
git worktree remove {パス}
git branch -d {ブランチ名}
```

---

## プロジェクトへのルール展開

**プロジェクトで初めて使用するとき**、`.claude/rules/pr-docs.md` が存在しない場合に作成します：

1. プロジェクトルートで `Glob(".claude/rules/pr-docs.md")` を実行して確認。
2. 存在しなければ、`.claude/rules/pr-docs.md` を以下の内容で作成：

```markdown
---
paths:
  - "docs/PR/**/*.md"
  - "docs/PR/index.yaml"
---

# PR ドキュメントルール

## PRドキュメントを作成するタイミング

`docs/PR/PR{N}.md` は PR ごとにマージ前に作成する。計画のみのPR（実装なし）は index.yaml に `planning: true` を設定する。

## 必須セクション

\`\`\`markdown
# PR{N} — {短いタイトル}

## 概要

{1〜3行：このPRが何をするか、なぜするか}

## スコープ

### 含む
- {項目}

### 含まない
- {項目}

## 変更ファイル

- `path/to/file` — 1行の変更理由
\`\`\`

オプションセクション：`背景`、`前提条件`、`実装ログ`、`決定事項`、`未決定事項`。

## index.yaml — 必須更新

`docs/PR/PR{N}.md` を作成・大幅更新するたびに `docs/PR/index.yaml` のエントリも追加・更新する。

| フィールド | ルール |
|---|---|
| `id` | PR番号（int） |
| `title` | PR{N}.mdのh1テキストと完全一致 |
| `type` | `feat` / `fix` / `docs` / `refactor` / `chore` / `test` |
| `tags` | 自由形式のリスト |
| `planning` | 実装なし（計画・設計のみ）のPRは `true` |
| `summary` | ファイルを開かずに内容が分かる1行説明（120文字以内） |
| `children` | このPRが定義した子PRの番号リスト |
| `parent` | このPRを定義した親PRの番号 |
```

3. `.claude/rules-jp/pr-docs.md` をスタブとして作成：

```markdown
> **このファイルは日本語ミラーです。本体は `.claude/rules/pr-docs.md`。**
```

4. コミット：`git add .claude/rules/ && git commit -m "chore: add pr-docs rule"`
