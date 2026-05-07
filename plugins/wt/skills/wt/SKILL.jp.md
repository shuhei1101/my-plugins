# SKILL.jp.md — wt スキル（日本語訳）

> このファイルは `SKILL.md` の日本語翻訳です。Claude Code には自動読み込みされません。内容を確認するための参照用ファイルです。
> 変更を加える場合は、まずこのファイルを更新し、その後 `SKILL.md`（本体）にも同じ変更を反映してください。

---

**スキル名**: wt  
**トリガー**: 新しい実装を始めたい・PR を作りたい・新しいブランチで作業したい・worktree セッションを再開したい・並行開発を管理したいときに自動起動。「worktree」「新しい PR」「〇〇を実装したい」「〇〇のブランチを作って」「並行実装」といった発言でトリガーする

---

# wt — Git Worktree 実装ワークフロー

## 基本原則

**1 セッション = 1 PR。** コード実装でもドキュメント更新でも、すべての作業は専用の worktree・専用ブランチ上で行う。複数の AI セッションが互いに干渉するのを防ぐためです。

ライフサイクル：**計画 → セットアップ → 実装 → レビュー → マージ → クリーンアップ**

---

## フェーズ1: 計画

コードやファイルに触れる前に：

1. **タスクを理解する。** `README.md` を読み、`docs/` があればスキャンし、スコープをユーザーと確認する。要件が不明な場合は、作業を開始する前に質問する。
2. **PR 番号を決める。** `docs/PR/` にある既存ファイルを確認して最大の PR 番号を調べる。次の番号は max + 1。`docs/PR/` がなければ作成する。
3. **PR ドキュメントを作成** (`docs/PR/PR{N}.md`)：

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

必要に応じてオプションセクションを追加：`## 設計メモ`、`## 依存関係`、`## リスク`、`## ユーザー確認事項`

4. **ブランチや worktree を作成する前に、ユーザーに計画を確認する。**

---

## フェーズ2: セットアップ

ユーザーが計画を承認したら：

1. **ベースブランチを確認する。** `git branch --show-current` と `git status` を実行。未コミット変更があれば警告。現在のブランチが `master`/`main` の場合も注意喚起。

2. **ブランチ名を決める** — `PR{N}/{type}/{内容}` 形式：
   - `type` は Conventional Commits に従う：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`
   - スペース・特殊文字はハイフンに変換
   - 日本語はそのまま許容
   - 例：`PR30/feat/login-implement`、`PR31/docs/update-wiki`、`PR32/fix/tts-timeout`
   - `git branch --list {ブランチ名}` で衝突チェック

3. **ブランチと worktree を作成：**

   ```bash
   git branch {ブランチ名} {ベースブランチ}
   git worktree add {worktreeパス} {ブランチ名}
   ```

   worktree パスのデフォルト：`{親ディレクトリ}/{リポジトリ名}-wt-PR{N}`  
   例：リポジトリが `/c/Users/shuhe/repo/voice-paste` なら worktree は `/c/Users/shuhe/repo/voice-paste-wt-PR30`

4. **依存関係をシンボリックリンクで接続**（対象が存在しない場合はスキップ）：
   - Python プロジェクト（`pyproject.toml` または `setup.py` が存在）：`ln -s {メインリポジトリ}/venv {worktree}/venv`
   - Node.js プロジェクト（`package.json` が存在）：`node_modules` と `.next`（あれば）をシンボリックリンク

5. **worktree 内で初期コミットを作成：**

   ```bash
   git commit --allow-empty -m "chore: start PR{N} {内容}"
   git add docs/PR/PR{N}.md
   git commit -m "docs: add PR{N} plan"
   ```

6. **セッション状態を保存** (`~/.claude/skill-memory/worktree/{YYYYMMDDHHMMSS}_session.md`)：
   ```
   ベースブランチ、worktree パス、PR 番号、現在のフェーズ
   ```

---

## フェーズ3: 実装

すべての作業は worktree ディレクトリ内で行う — メインリポジトリには触れない。

- `docs/PR/PR{N}.md` のタスクリストを進捗に合わせてチェックしていく
- フェーズの区切りごとに `~/.claude/skill-memory/worktree/` のセッションファイルを更新
- Conventional Commits 形式でコミット：
  - `feat:` 新機能、`fix:` バグ修正、`refactor:` リファクタリング、`docs:` ドキュメント、`test:` テスト、`chore:` 雑務
  - 例：`git add . && git commit -m "feat: JWT 認証を実装"`
- コミット前に変更ファイルを確認する

---

## フェーズ4: レビュー & マージ

### ユーザーレビュー

コミット完了後、worktree パスをユーザーに伝えて実装内容の確認を依頼：

```
変更内容を以下の worktree で確認してください: {worktreeパス}
```

ユーザーが修正を求めた場合はフェーズ3に戻る。

### マージ

ユーザーがレビュー完了を確認したら、以下のみを出力する：

```
コミット完了 — PR{N}: {変更内容の1行説明}
```

以降は何もしない。**マージコマンドを表示しない。**「マージしますか？」と聞かない。マージはユーザーが自分のターミナルで実行する：

```bash
# ユーザーがメインリポジトリで実行
git checkout {ベースブランチ}
git merge {ブランチ名}
```

ユーザーがマージ完了を伝えるまで待つ。

### クリーンアップ

ユーザーがマージ完了を確認したら、worktree とブランチを削除：

```bash
git worktree remove {worktreeパス}
git branch -d {ブランチ名}
```

セッションファイルを更新：`## ステータス: 完了`

リモートへの push は常にユーザーの責任 — このスキルでは `git push` を実行しない。

---

## セッションの再開

作業を中断して再開したいとき：

1. `~/.claude/skill-memory/worktree/` から該当セッションファイルを読み込む
2. `## 現在のステータス` で最後に完了したフェーズを確認
3. `git worktree list` で worktree がまだ存在するか確認
4. 該当フェーズから作業を再開する

---

## Git コマンドリファレンス

```bash
# worktree 一覧
git worktree list

# カレントブランチ
git branch --show-current

# 未コミット変更の確認
git status

# 次の PR 番号 — 既存ドキュメントから最大値を確認
ls docs/PR/

# ブランチ + worktree の作成
git branch PR{N}/{type}/{内容} {ベースブランチ}
git worktree add {パス} PR{N}/{type}/{内容}

# 空の初期コミット
git commit --allow-empty -m "chore: start PR{N} {内容}"

# マージ（worktree ではなくメインリポジトリで実行）
git checkout {ベースブランチ}
git merge {ブランチ名}

# クリーンアップ
git worktree remove {パス}
git branch -d {ブランチ名}
```
