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
| 2 | 済 | CLAUDE.md changelog の config スキル記述を削除 | `plugins/claude-kit/CLAUDE.md`<br>`plugins/claude-kit/CLAUDE.jp.md` |
| 3 | 済 | plugin.json / marketplace.json を v3.52.0 に更新 | `plugins/claude-kit/.claude-plugin/plugin.json`<br>`.claude-plugin/marketplace.json` |
| 4 | 済 | _index.yaml の config skill 参照は削除対象外と確認 | — |
| 5 | 済 | QA を記録する | — |
| 6 | 済 | ノートを更新する | `.work/notes/スキル設計/plugin-config-reference.md` |

## 変更内容

| No | ファイル | 変更種別 | 概要 |
|----|----------|----------|------|
| 1 | `plugins/claude-kit/skills/config/SKILL.md` | 削除 | configスキル本体 |
| 2 | `plugins/claude-kit/skills/config/SKILL.jp.md` | 削除 | JP ミラー |
| 3 | `plugins/claude-kit/CLAUDE.md` | 編集 | changelog の config スキル行を削除し v3.52.0 エントリ追加 |
| 4 | `plugins/claude-kit/CLAUDE.jp.md` | 編集 | 同上の JP ミラー側 |
| 5 | `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | v3.51.0 → v3.52.0 |
| 6 | `.claude-plugin/marketplace.json` | 編集 | 同上 |

## テスト

| No | 確認項目 | 結果 |
|----|----------|------|
| 1 | `plugins/claude-kit/skills/config/` フォルダが存在しない | ✅ |
| 2 | CLAUDE.md / CLAUDE.jp.md に config スキル追加行がない | ✅ |
| 3 | plugin.json / marketplace.json が v3.52.0 | ✅ |

## QA

なし

## 参考ドキュメント

- `.work/notes/スキル設計/plugin-config-reference.md`

## 関連ブランチ

## 次ブランチ候補
