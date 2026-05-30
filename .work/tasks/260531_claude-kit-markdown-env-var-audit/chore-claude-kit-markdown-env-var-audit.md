# chore/claude-kit-markdown-env-var-audit

> 内部 ID: 221（index.yaml 採番用 — クロスリファレンス目的）

## 概要

claude-kit / dev-kit / work / ref-inject など全プラグインのマークダウンファイル
（SKILL.md・ルール・references・CLAUDE.md）を調査し、「`echo $VAR` で env var を確認せよ」
等の **マークダウンが直接 env var を読もうとする誤った指示** がないか全量検査し、
あれば適切なパターン（フック経由でテンプレート注入 / セッション開始時 env 注入）に修正する。

### 引き継ぎ背景（PR201 から）

PR201 (`CLAUDE_KIT_JP_MIRROR` 環境変数追加) の作業中に、当初 `common.md` に
「ファイル作成前に `echo ${CLAUDE_KIT_JP_MIRROR:-true}` を実行して値を確認せよ」
と書いてしまった。これは **マークダウンファイルは env var を読めない**（フック/スクリプトのみ可）
という Claude Code プラグインの基本原則を理解していなかったことが原因。

PR201 では正しいパターン（フックが `os.environ` で読み Jinja2 テンプレートに渡す）に
修正し、`plugin-structure.md` に以下の知見を追記した：

| パターン | 使いどころ |
|---|---|
| **フックテンプレート注入** | 少数の env var が特定のスキル/ルールに影響する場合 |
| **セッション開始時 env 注入** | 多数の env var を全マークダウンに見せたい場合 |

このブランチでは過去に書かれた他のマークダウンに同様の誤りがないか全量調査する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 | 対象ファイル |
|---|---|---|---|
| 1 | ✅ | `plugins/**/*.md` 全体を `echo $`、`os.environ` 等のキーワードで grep し誤り候補を抽出 | - |
| 2 | ✅ | 抽出した各候補を内容確認し、誤りを修正（`WORK_KIT_*` → `WORK_*`、`NEXT_KIT_TS_CHECK` → `DEV_KIT_NEXT_TS_CHECK`） | `work/skills/config/SKILL.md` |
| 3 | ✅ | JP ミラー側 (`SKILL.jp.md`) も同様に修正 | `work/skills/config/SKILL.jp.md` |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/config/SKILL.md` | 編集 | `WORK_KIT_*` → `WORK_*`、`NEXT_KIT_TS_CHECK` → `DEV_KIT_NEXT_TS_CHECK`、`/work-kit:merge` → `/work:merge` | env var 名がフックコードと不一致だった |
| 2 | `plugins/work/skills/config/SKILL.jp.md` | 編集 | 同上（JP ミラー） | 〃 |

## テスト

上記実装に伴って追加・変更したテストファイル。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| (テストなし) | - | - | - |

## QA

QA 事項なし（調査結果に応じて随時追記）。

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-structure.md`: env var × マークダウンの2パターン
- `plugins/claude-kit/references/environment.md`: 環境変数の設計規約
- `.work/notes/jp-mirror-policy.md`: PR201 で更新済みのノート

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| PR201 (merged) | `CLAUDE_KIT_JP_MIRROR` 追加 + plugin-structure.md に env var パターンを記載 |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
