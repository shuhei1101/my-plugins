# QA — PR153 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: hook-creator / plugin-creator dispatch を PreToolUse として配線するか

**状況**:
- `prompts/hook-creator-dispatch.{md,jp.md}` と `prompts/plugin-creator-dispatch.{md,jp.md}` は存在するが、現在 hooks.json に未配線（オーファン）。
- git 履歴上、これらは元々 **UserPromptSubmit のキーワード検出フック**だった（「プロンプトが hooks ファイル/plugins 配下のパスに言及したら」）。PreToolUse のファイルパスブロックへ移行した際、skill/rule/claude/j2 だけ PreToolUse 版が作られ、この 2 つは作られなかった。
- そのため prompt 本文の文言も "the user's prompt mentions one" という UserPromptSubmit 前提の言い回しのまま。

**論点**:
- **plugin-creator-dispatch**: PreToolUse で `plugins/**` を対象にすると、このリポジトリの**全ファイル編集**にマッチしてしまい、より具体的な skill/rule/j2 dispatch と全面的に重複・ノイズ化する。→ 配線は不適切と判断。
- **hook-creator-dispatch**: `hooks.json` / `settings(.local).json` の編集を hook-creator に通す、は方針として筋は通る。ただし hooks.json を触るたびにブロックが入る摩擦が増える。文言も PreToolUse 用に書き直しが必要。

**決定（2026-05-28 ユーザー回答）**:
- **両方とも PreToolUse(Edit/Write) のファイルパス dispatch として配線する**（skill/rule/claude/j2 や dev-kit の Python dispatch と同じ方式）。元の UserPromptSubmit キーワード検出方式から作り変える。
- prompt 本文は「プロンプトが言及したら」→「直接編集しようとしたら creator スキルを実行せよ」という PreToolUse 用の文言に書き直す。
- パターン:
  - hook-creator-dispatch: `hooks.json` / `settings.json` / `settings.local.json`（hook 設定ファイルに限定。スクリプト .py や .j2 テンプレ・prompts/*.md は対象外＝より具体的な dispatch/チェックに任せる）
  - plugin-creator-dispatch: `plugins/` 配下（最も広いのでルール順序では**最後＝最低優先度のキャッチオール**にし、skill/rule/claude/hook/j2 が先にマッチしたものはそちらが処理する）
- 補足: これらは claude-kit を**導入したプロジェクト**で発火する想定。本リポジトリ（マーケットプレイス自身）では plugins/ 配下が全ファイルなので広くヒットするが、セッションフラグ型で 1 セッション 1 回のみブロックのため許容。

