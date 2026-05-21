# QA — PR58 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: 分割境界線 — work-start内のworktree操作をどこまで分離するか

**状況**: 決定済み ✅

**決定内容**: 広い解釈（B）を採用
- `work-start` 内の `git worktree add` ロジックも worktree-kit へ切り出す
- work-kit は worktree-kit に委譲する形にする
- `vscode-workspace-sync` スキルも worktree-kit へ移動

**理由**: worktree を使わないプロジェクトでは work-kit だけインストールして使えるようにしたい。worktree-kit は必要なプロジェクトにのみインストールする。

**影響**:
- `work-start` は worktree 操作部分を worktree-kit に依存する形にリファクタリング
- worktree-kit も work-kit と同様のフック・作業時確認フローを持つ
