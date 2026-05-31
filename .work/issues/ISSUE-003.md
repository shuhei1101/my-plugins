# ISSUE-003: 全プラグインで必須の setup-wizard スキルが未実装

**作成日**: 2026-05-31

## 問題

`references/plugin/プラグイン構造.md` では、すべてのプラグインに `setup-wizard` スキルを必須として定めている（「Every plugin **must** ship a `setup-wizard` skill」）。しかし、現在リポジトリに存在する4つのプラグインすべてで `setup-wizard` スキルが実装されていない。

| プラグイン | setup-wizard の有無 |
|---|---|
| `dev-kit` | なし |
| `claude-kit` | なし |
| `ref-inject` | なし |
| `work` | なし |

`setup-wizard` は以下の役割を担う必須スキルである:
- ユーザーの初回セットアップをインタラクティブにガイドする
- `SessionStart` フック経由で `setup_done` フラグを確認し、未完了時に自動プロンプトを表示する
- `.claude/{plugin}.local.md` に `setup_done: true` を記録して完了をマークする

この欠如により、プラグインをインストールしたユーザーが初回設定をどこから始めればよいか分からず、env トグルや設定項目を見落とすリスクがある。

## 修正案

各プラグインに対して以下を実装する:

1. `plugins/{name}/skills/setup-wizard/SKILL.md` および `SKILL.jp.md` を作成する（`プラグイン構造.md` 内のスケルトンに従う）
2. `plugins/{name}/hooks/hooks.json` に `SessionStart` エントリを追加し、`setup_check.py` スクリプトを実装する
3. env vars を持つプラグイン（dev-kit / claude-kit / work）では `plugin-config` スキルがすでに存在するため、`setup-wizard` からそれに委任するフローを組む
4. 各プラグインの `plugin.json` と `marketplace.json` のバージョンを MINOR バンプする（新スキル追加のため）
5. 各プラグインの `CLAUDE.md` changelog に追記する

優先度は利用頻度の高い `work` → `dev-kit` → `claude-kit` → `ref-inject` の順を推奨する。

## 水平展開

今後新規プラグインを作成する際も `setup-wizard` を必ず含めるよう、`plugin-creator` スキルの手順書に「setup-wizard を生成する」ステップを明示的に追加することを検討する。また `ref-inject:plugin-migrate` のチェックリストにも `setup-wizard` 実装確認を加えることで、既存プラグインのアップグレード時に見落としを防げる。
