---
created_at: 2026-05-23
updates:
  - 2026-05-23 — PR91: pr-handoff スキルの追加
  - 2026-05-24 — PR109: pr-show スキルを merge Step 12 から切り出し
  - 2026-05-29 — PR163: worktree-kit を統合（work-add / vscode-workspace-sync を取り込み）
  - 2026-05-30 — PR172: プラグインを work-kit → workspace にリネーム、env var も WORK_KIT_* → WORKSPACE_* に変更
related_prs:
  - PR91
  - PR109
  - PR163
  - PR172
---

# work-kit スキル群 — 設計メモ

## 概要

work-kit プラグインに含まれるスキルの設計・目的・相互関係を記録するノート。

## スキル一覧

| スキル名 | 目的 |
|---|---|
| `work-start` | 新しいPRを開始：ワークツリー・タスクフォルダ・TODO.md・QA.mdを作成 |
| `merge` | PRをマージ：TODO確認・git merge・index.yaml更新・ワークツリー削除 |
| `update` | work-kit スキルを手動更新する |
| `setup` | `.work/` ディレクトリを初期化する（プロジェクトに初回導入） |
| `branch-index-cleanup` | 古いブランチとindex.yamlエントリをクリーンアップ |
| `pr-handoff` | 次のセッション向け引き継ぎ指示書を会話内に出力（PR91で追加） |
| `pr-show` | 予約済みPRの状況を3カテゴリ（着手可能・進行中・条件あり）で一覧表示（PR109で追加） |
| `work-add` | git worktree とブランチを作成（PR163 で worktree-kit から統合） |
| `vscode-workspace-sync` | VS Code `.code-workspace` の `folders` を worktree と同期する PostToolUse フックを設定（PR163 で worktree-kit から統合） |

## worktree-kit 統合（PR163）

worktree-kit プラグインを廃止し、`work-add` / `vscode-workspace-sync` を work-kit に取り込んだ。
work-kit ← worktree-kit の片方向依存しかなく、別プラグインに分ける利点がなかったため。

ワークツリーの利用可否は環境変数 `WORK_KIT_USE_WORKTREE` で切り替える:

- 未設定 / `true` 等 → ワークツリーを使用（デフォルト）
- `false` / `0` / `no` → ワークツリー作成をスキップし `.work/` 管理のみで継続

work-start Step 4 がこの env var を読んで分岐する（従来の「worktree-kit インストール有無」判定を置き換え）。

## pr-handoff スキルの設計

### 目的

1つのPRが終わった後、次のセッション（真っさらなコンテキストのClaude）に  
「これまでの経緯」と「次のPRでやってほしいこと」を伝えるための指示書を生成する。

### 出力形式

コードブロックで会話内に出力（ファイル保存なし）。  
ユーザーがClaudeCodeのコピー機能で内容をコピーし、次のセッションに貼り付ける。

### 指示書の構成

1. **これまでの経緯** — 現在のセッションで行った作業の要約
2. **次のPRの依頼** — 次に対応してほしいPR番号・タイトル・具体的な内容
3. **参考情報** — 関連ファイルパス・注意点など

### トリガー条件

- ユーザーが「引き継ぎ書を作って」「次のPRの指示書を作って」「ハンドオフして」などと言ったとき
- ユーザーが「pr-handoff して」と言ったとき
