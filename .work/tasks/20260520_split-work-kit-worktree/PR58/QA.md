# QA — PR58 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: 分割境界線 — work-start内のworktree操作をどこまで分離するか

**状況**: 未決定

**背景**:
- 狭い解釈: `vscode-workspace-sync` スキルのみを worktree-kit へ移動
- 広い解釈: `work-start` 内の `git worktree add` ロジックも worktree-kit へ切り出し、work-kit は worktree-kit に委譲する形にする

**ユーザー回答待ち**
