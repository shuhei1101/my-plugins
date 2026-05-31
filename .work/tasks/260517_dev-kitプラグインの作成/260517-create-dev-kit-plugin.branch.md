# PR47 — create-dev-kit-plugin

## 概要

`py-kit` と `yaml-rule` を統合した新プラグイン `dev-kit` を新設する。
`dev-kit` は実装作業全般を支援するスキル群と、各種リファレンス資料（`references/`）を提供する。

リファレンス構成（フラット）:
- `common.md` — フロントエンド/バックエンド共通の規約（Markdown など）
- `frontend.md` — フロントエンド共通（HTML/CSS/JS の書き方）
- `backend.md` — バックエンド共通
- `python.md` — Python 共通の書き方（旧 `py-kit/references/python-standards.md` を移植）
- `yaml.md` — YAML の使い方（旧 `yaml-rule` から移植）
- `vscode-extension.md` — VS Code 拡張機能の作り方

スキルは現行の py-kit / yaml-rule のスキルをそのまま `dev-kit/skills/` に移植する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260517_create-dev-kit-plugin/PR47/QA.md` |
| 済 | 仕様書 `dev-kit-design.md` を新規作成する | - `.work/specs/dev-kit-design.md` |
| 済 | `dev-kit` プラグインスケルトン作成 | - `plugins/dev-kit/.claude-plugin/plugin.json` |
| 済 | `references/python.md` を移植（py-kit から） | - `plugins/dev-kit/references/python.md`, `python.jp.md` |
| 済 | `references/yaml.md` を新規作成（yaml-rule から内容を抽出） | - `plugins/dev-kit/references/yaml.md`, `yaml.jp.md` |
| 済 | `references/common.md` / `frontend.md` / `backend.md` / `vscode-extension.md` を雛形作成 | - `plugins/dev-kit/references/*.md` |
| 済 | `skills/py-script` を py-kit から移植 | - `plugins/dev-kit/skills/py-script/` |
| 済 | `skills/py-project` を統合作成（py-new-project + py-project を 1 つに、最初の分岐で新規/既存を判定） | - `plugins/dev-kit/skills/py-project/` |
| 済 | `skills/yaml` を yaml-rule から移植・改名 | - `plugins/dev-kit/skills/yaml/` |
| 済 | スキル内の references 参照パスを更新 | - `plugins/dev-kit/skills/**/SKILL.md` |
| 済 | `marketplace.json` に `dev-kit` を追加、`py-kit` と `yaml-rule` を削除 | - `.claude-plugin/marketplace.json` |
| 済 | 旧 `plugins/py-kit/` と `plugins/yaml-rule/` を削除 | - `plugins/py-kit/`, `plugins/yaml-rule/` |
| 済 | ルール・CLAUDE.md を整備する | - `CLAUDE.md`, `CLAUDE.jp.md` |

## 参考ドキュメント

- `.work/specs/dev-kit-design.md`: dev-kit プラグイン設計仕様（本 PR で作成）
- `.work/specs/py-kit-design.md`: 旧 py-kit 設計（参考、移植元）

## QA

なし
