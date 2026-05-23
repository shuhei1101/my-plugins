# Incidents

| Date | Summary | Detail |
|---|---|---|
| 2026-05-21 | master で直接ファイルを編集すると worktree マージ時に競合が発生する。必ず work-start → worktree 内で作業する | [detail](../../references/incidents/master-direct-edit-causes-merge-conflict.md) |
| 2026-05-23 | スキルが Step 0 で他のスキルを読み込む設計にすると起動ごとに 2500×N トークンを消費してコンテキストを圧迫する。判定知識はスキル本体の References に内包させること | [detail](../../references/incidents/skill-reading-token-cost.md) |
| 2026-05-23 | 複数のスキルが同じ判断基準を inline で二重管理していた。creator スキル群の共通知識は `references/` に集約し、各スキルから参照する設計にすること | [detail](../../references/incidents/creator-skill-inline-duplication.md) |
| 2026-05-23 | async コピーハンドラが失敗時でも stop() を呼んでいたため選択状態が失われリトライ不可だった。失敗時は stop() を呼ばずピッカーを維持する | [detail](../../references/incidents/async-handler-stop-on-failure.md) |
| 2026-05-23 | removeEventListener に匿名関数（アロー関数）を渡しても解除できない。イベントリスナーは名前付き関数で登録・解除すること | [detail](../../references/incidents/removeeventlistener-anonymous-function.md) |
