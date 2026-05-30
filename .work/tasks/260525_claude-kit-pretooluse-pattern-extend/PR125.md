# PR125 — claude-kit-pretooluse-pattern-extend

## 概要

claude-kit の `skill-creator-dispatch` PreToolUse フックが現在 `/skills/[^/]+/SKILL\.md$` のみを対象にしており、`SKILL.jp.md`・`.claude/rules/*.md`・`CLAUDE.md` が対象外になっている。これを拡張して creator スキル管理下の全ファイルをガードする。

### 背景（PR124 より）
- PR121 で PreToolUse ブロック型フックを導入し、`SKILL.md` (EN) のみをガード対象にした。
- PR124 で dev-kit/ui-kit/work-kit の重複エントリを削除し、claude-kit に集約した。
- 集約後に残った課題: `SKILL.jp.md`・`rules/*.md`・`CLAUDE.md` が未ガード。
- Claude が `claude-refactor` スキル等を実行すると creator スキルを経由せず直接これらを編集する穴がある。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #PR121 | skill-creator-dispatch を PreToolUse ブロック型に移行 |
| #PR124 | dev-kit/ui-kit/work-kit から重複削除・claude-kit に集約 |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| x | QA.md に未決定事項を記録する | `.work/tasks/20260525_claude-kit-pretooluse-pattern-extend/PR125/QA.md` |
| x | `.work/notes/` のノートを更新する | `.work/notes/claude-kit-creator-skill-hook.md` |
| x | claude-kit PreToolUse パターンを拡張（SKILL.jp.md 対応） | `plugins/claude-kit/hooks/hooks.json` |
| x | claude-kit PreToolUse パターンを拡張（rules/*.md 対応） | `plugins/claude-kit/hooks/hooks.json` |
| x | claude-kit PreToolUse パターンを拡張（CLAUDE.md 対応） | `plugins/claude-kit/hooks/hooks.json` |
| x | rule-creator-dispatch / claude-creator-dispatch の PreToolUse エントリを追加または統合 | `plugins/claude-kit/hooks/hooks.json` |
| x | 対応するプロンプトファイルを確認・必要に応じて更新 | `plugins/claude-kit/hooks/prompts/` |
| x | claude-kit の plugin.json バージョンバンプ | `plugins/claude-kit/.claude-plugin/plugin.json` |
| x | marketplace.json バージョンバンプ | `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/notes/claude-kit-creator-skill-hook.md`: creator-dispatch フック設計メモ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| pretooluse-file-edit-intercept-research | PreToolUse でファイル編集を検知する仕組みの設計調査・実装 | 即時実施可 |

## QA

なし
