# PR28 — restructure-py-kit-plugin

## 概要

`py` プラグインを `py-kit` にリネームし、単一スキルを3スキルに分割する。
共通の Python ルール・設計原則を `references/` に集約し、各スキルから参照させる。
クラス構造・設定ファイル・テストの連携ルールを `/rule-creator` で作成する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | プラグイン名を `py` → `py-kit` にリネーム（フォルダ名・plugin.json・marketplace.json） | - `plugins/py-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | `references/` フォルダ作成・共通 Python ルール資料を1ファイルにまとめる（命名規則・SOLID・DRY・DDD・拡張設計・テスト方針） | - `plugins/py-kit/references/python-standards.md` |
| 済 | スキル分割: `py-script`（簡易スクリプト作成） | - `plugins/py-kit/skills/py-script/SKILL.md`<br>- `plugins/py-kit/skills/py-script/SKILL.jp.md` |
| 済 | スキル分割: `py-new-project`（新規プロジェクト作成） | - `plugins/py-kit/skills/py-new-project/SKILL.md`<br>- `plugins/py-kit/skills/py-new-project/SKILL.jp.md` |
| 済 | スキル分割: `py-project`（既存プロジェクト確認・修正） | - `plugins/py-kit/skills/py-project/SKILL.md`<br>- `plugins/py-kit/skills/py-project/SKILL.jp.md` |
| 済 | ルールテンプレート作成: クラス構造連携 | - `plugins/py-kit/rules/class-structure.md` |
| 済 | ルールテンプレート作成: 設定ファイル ↔ ソースコード連携 | - `plugins/py-kit/rules/config-source-link.md` |
| 済 | ルールテンプレート作成: ソースコード ↔ テスト連携 | - `plugins/py-kit/rules/source-test-link.md` |
| 済 | 旧 `py` プラグインフォルダを削除 | - `plugins/py/` （削除済み） |
| 済 | plugin.json のバージョン更新、marketplace.json 更新 | - `plugins/py-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| - | `plugins/py-kit/rules/` フォルダを削除（プラグイン内にルールテンプレートは持たない） | - `plugins/py-kit/rules/class-structure.md`<br>- `plugins/py-kit/rules/config-source-link.md`<br>- `plugins/py-kit/rules/source-test-link.md` |
| - | `py-new-project` Step6 を修正: テンプレートコピーではなく `/claude-kit:rule-creator` を使う指示に変更 | - `plugins/py-kit/skills/py-new-project/SKILL.md`<br>- `plugins/py-kit/skills/py-new-project/SKILL.jp.md` |
| - | `py-project` Step5 を修正: ルールが未存在の場合 `/claude-kit:rule-creator` を使う指示に変更 | - `plugins/py-kit/skills/py-project/SKILL.md`<br>- `plugins/py-kit/skills/py-project/SKILL.jp.md` |
| - | `references/python-standards.jp.md` を作成（日本語ミラー） | - `plugins/py-kit/references/python-standards.jp.md` |

## 参考ドキュメント

- `.work/specs/py-kit-design.md`: py-kit プラグイン設計仕様

## スキル設計方針

- YAGNI・シンプルイズベスト的な記述は禁止。拡張性ある設計を前提とする
- 各スキルは `references/python-standards.md` を参照し重複記述をしない
- テスト方針：単体テストはほぼ不要。結合テスト・ユースケーステスト（外部境界のみ）を推奨
