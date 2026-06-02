# claude-kit configスキル削除

> ブランチ: chore/remove-claude-kit-config-skill

## 概要

### 実施条件

即時実施可

### 背景

`claude-kit:config` スキル（`plugins/claude-kit/skills/config/SKILL.md` + `SKILL.jp.md`）を削除し、
ファイルを参照している箇所もあわせてクリーンアップする。

## 作業内容

| No | 状態 | タスク | 対象ファイル |
|----|------|--------|------------|
| 1 | 済 | SKILL.md / SKILL.jp.md の削除 | `plugins/claude-kit/skills/config/SKILL.md`<br>`plugins/claude-kit/skills/config/SKILL.jp.md` |
| 2 | - | CLAUDE.md changelog の config スキル記述を削除 | `plugins/claude-kit/CLAUDE.md` |
| 3 | - | _index.yaml の config skill 参照を削除 | `plugins/claude-kit/references/.ref-injects/_index.yaml` |
| 4 | - | _index.jp.yaml の同様の記述を削除 | `plugins/claude-kit/references/.ref-injects/_index.jp.yaml` |
| 5 | - | QA を記録する | — |
| 6 | - | ノートを更新する | — |

## 変更内容

| No | ファイル | 変更種別 | 概要 |
|----|----------|----------|------|
| 1 | `plugins/claude-kit/skills/config/SKILL.md` | 削除 | configスキル本体 |
| 2 | `plugins/claude-kit/skills/config/SKILL.jp.md` | 削除 | JP ミラー |
| 3 | `plugins/claude-kit/CLAUDE.md` | 編集 | changelog の config スキル行を削除 |
| 4 | `plugins/claude-kit/references/.ref-injects/_index.yaml` | 編集 | config skill 参照行を削除 |
| 5 | `plugins/claude-kit/references/.ref-injects/_index.jp.yaml` | 編集 | 同上の JP ミラー側 |

## テスト

| No | 確認項目 | 結果 |
|----|----------|------|
| 1 | `plugins/claude-kit/skills/config/` フォルダが存在しない | - |
| 2 | CLAUDE.md に config スキル記述がない | - |
| 3 | _index.yaml に config skill 参照がない | - |

## QA

なし

## 参考ドキュメント

## 関連ブランチ

## 次ブランチ候補
