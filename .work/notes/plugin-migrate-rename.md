---
created_at: 2026-05-31
updates:
  - 2026-05-31 — 初版作成（plugin-update → plugin-migrate リネーム）
related_specs:
  - plugin-config-reference.md
related_branches:
  - refactor/rename-plugin-update-to-migrate
---

# plugin-migrate スキル命名規則 — plugin-update から plugin-migrate へのリネーム

## 概要

各プラグインに存在する `plugin-update` スキルを `plugin-migrate` にリネームする。
スキルの用途は「プラグイン構造変更を全プラグインに横断適用（マイグレーション）」であり、
`update`（継続的な追随）より `migrate`（一回性の構造変換）の方が意図を正確に表すため。

## 対象プラグイン

| # | プラグイン | 旧スキル名 | 新スキル名 |
|---|---|---|---|
| 1 | `claude-kit` | `plugin-update` | `plugin-migrate` |
| 2 | `dev-kit` | `plugin-update` | `plugin-migrate` |
| 3 | `ref-inject` | `plugin-update` | `plugin-migrate` |
| 4 | `work` | `plugin-update` | `plugin-migrate` |

## 命名の根拠

- **update**: バージョン追随・依存関係更新など繰り返し実行する操作のニュアンス
- **migrate**: 旧構造 → 新構造への一回性の変換。スキルの実際の用途に合致する
- `plugin-sync` も候補に挙がったが、「同期」より「移行」の方がスキル内容を正確に表す

## 変更ファイル一覧

- 各プラグインの `skills/plugin-update/` → `skills/plugin-migrate/` にディレクトリリネーム
- `SKILL.md` / `SKILL.jp.md` 内の自己参照 (`plugin-update`) を `plugin-migrate` に更新
- `CLAUDE.md` / `CLAUDE.jp.md` のスキル一覧を更新
- `claude-kit/references/plugin/` 以下の参照ドキュメントを更新
