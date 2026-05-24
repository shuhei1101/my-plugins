# feature — 機能固有のドメイン知識

## About this folder

各プラグイン・機能に固有のリンクルール群。特定のファイルを編集した際に関連ファイルの更新漏れを防ぐ同期チェックリストを提供する。1機能 = 1ファイル。

## File list

| File | Content |
|---|---|
| `claude-kit-skill-dependencies.md` | claude-kit の creator スキル群と共有 references の依存関係 |
| `debug-fab-template-sync.md` | `uidev.js` / `uidev.css` 変更時の SKILL.md・CLAUDE.md・バージョン同期ルール |
| `work-kit-todo-template-sync.md` | TODO.md テンプレートと work-start SKILL.md Step 7 の同期ルール |
| `creator-skill-dispatch.md` | プラグインコンポーネント編集時に対応するクリエイタースキルを先に呼び出す強制ルール |
| `skill-jp-mirror-sync.md` | `SKILL.md` 編集時に `SKILL.jp.md` も同コミットで更新する同期ルール |
| `worktree-kit-dependency.md` | work-kit と worktree-kit の責務分離・インターフェース整合ルール |
| `work-kit-merge-skill-spec-sync.md` | merge SKILL.md のステップ番号変更時に `work-kit-merge-flow.md` 仕様書の参照番号も更新する同期ルール |
