# Incidents

| Date | Summary | Detail |
|---|---|---|
| 2026-05-21 | master で直接ファイルを編集すると worktree マージ時に競合が発生する。必ず work-start → worktree 内で作業する | [detail](../../references/incidents/master-direct-edit-causes-merge-conflict.md) |
| 2026-05-23 | スキルが Step 0 で他のスキルを読み込む設計にすると起動ごとに 2500×N トークンを消費してコンテキストを圧迫する。判定知識はスキル本体の References に内包させること | [detail](../../references/incidents/skill-reading-token-cost.md) |
| 2026-05-23 | 複数のスキルが同じ判断基準を inline で二重管理していた。creator スキル群の共通知識は `references/` に集約し、各スキルから参照する設計にすること | [detail](../../references/incidents/creator-skill-inline-duplication.md) |
| 2026-05-23 | async コピーハンドラが失敗時でも stop() を呼んでいたため選択状態が失われリトライ不可だった。失敗時は stop() を呼ばずピッカーを維持する | [detail](../../references/incidents/async-handler-stop-on-failure.md) |
| 2026-05-23 | removeEventListener に匿名関数（アロー関数）を渡しても解除できない。イベントリスナーは名前付き関数で登録・解除すること | [detail](../../references/incidents/removeeventlistener-anonymous-function.md) |
| 2026-05-23 | merge スキルの archive ステップが常に 0 件を返していた。原因: (1) `completed: true` 設定ステップの欠落 (2) `index.yaml` は gitignored でワークツリーに存在しない。修正: set-completed コマンド追加 + Step 4 追加 + archive 先をワークツリーに変更 | [detail](../../references/incidents/merge-archive-step-zero-bug.md) |
| 2026-05-24 | merge スキルがユーザーの明示的指示なしに `git merge` を自動実行した。セッション内で過去に許可を得ていても次のマージは別指示が必要。修正: SKILL.md に Critical Prohibition セクション追加・Step 6 に絶対禁止ルール追記 | [detail](../../references/incidents/merge-auto-execution-without-permission.md) |
| 2026-05-24 | `.work/specs/` フォルダ名が「仕様書」を連想させるため、AI に自動読み込みされないにもかかわらず重要ドキュメント扱いになり古くなりやすかった。AI 非読み込みのフォルダは `notes/` など非公式な名前にすること | [detail](../../references/incidents/work-folder-name-implies-official-docs.md) |
| 2026-05-24 | Stop フックの `reason` に全文を埋め込むと Claude のレスポンスごとに長文が会話セッションへ注入されユーザーに見えて鬱陶しい。`reason` は「このファイルを読んで従え」の1行参照のみにし、Claude 自身がファイルを読む方式にすること | [detail](../../references/incidents/stop-hook-reason-floods-session.md) |
