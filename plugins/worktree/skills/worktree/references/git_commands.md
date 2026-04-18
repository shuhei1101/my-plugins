# Git コマンドリファレンス

worktreeスキルで使用するgitコマンドの詳細。

## ブランチ作成

```bash
git branch {ブランチ名} {ベースブランチ}
```

- ブランチ名形式: `{PR番号}/{やること名}` (例: `30/ログイン実装`)
- ベースブランチはスキル起動時のカレントブランチ

## Worktree作成

```bash
git worktree add {worktreeパス} {ブランチ名}
```

- worktreeパスのデフォルト: `{親ディレクトリ}/{リポジトリ名}-wt-PR{N}`
- 例: リポジトリが `/c/Users/shuhe/repo/voice-paste` なら worktreeは `/c/Users/shuhe/repo/voice-paste-wt-PR30`

## 空コミット

```bash
cd {worktreeパス}
git commit --allow-empty -m "chore: start PR{N} {やること名}"
```

## PRドキュメントコミット

```bash
cd {worktreeパス}
git add docs/PR/PR{N}.md
git commit -m "docs: add PR{N} plan"
```

## 実装後のコミット（Conventional Commits）

```bash
cd {worktreeパス}
git add .
git commit -m "{prefix}: {変更内容の簡潔な説明}"
```

プレフィックス:
- `feat:` — 新機能追加
- `fix:` — バグ修正
- `refactor:` — リファクタリング
- `docs:` — ドキュメント変更
- `test:` — テスト追加/修正
- `chore:` — 雑務（依存更新など）
- `style:` — コードスタイル（機能に影響なし）
- `perf:` — パフォーマンス改善

## Squashマージ

**メインリポジトリ側で実行**（worktree側ではない）:

```bash
cd {メインリポジトリパス}
git checkout {ベースブランチ}
git merge --squash {ブランチ名}
git commit -m "{機能名}の実装 #PR{N}"
```

マージメッセージ例:
- `ログイン機能の実装 #PR30`
- `認証バグの修正 #PR31`
- `設定画面のリファクタリング #PR32`

**重要**:
- `--squash` フラグで全コミットを1つにまとめる
- メッセージ末尾に `#PR{N}` を必ずつける（docs/PR/PR{N}.md への参照）
- リモートへの push はユーザーが手動で行う（自動push しない）

## クリーンアップ

```bash
git worktree remove {worktreeパス}
git branch -D {ブランチ名}
```

- `git branch -D` は強制削除（`-d` だとマージ済みチェックで失敗するケースがあるため `-D` を使用）
- squashマージ後はブランチの履歴がベースブランチに残らないため、`-d` は通常失敗する

## 状態確認コマンド

```bash
# カレントブランチ
git branch --show-current

# 作業ツリーがクリーンか
git status

# worktree一覧
git worktree list

# 既存ブランチ一覧（重複チェック用）
git branch --list {ブランチ名}
```

## 注意事項

- worktreeはブランチを専有する（同じブランチを複数worktreeでチェックアウトできない）
- メインリポジトリと同じブランチをworktreeで開こうとするとエラーになる
- squashマージ後のブランチは履歴が残らないので、マージ前に内容を確認すること
