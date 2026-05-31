# PR129 — create-py-kit-plugin

## 概要

dev-kit から Python 専用コンテンツを分離し、py-kit プラグインを新規作成する。
dev-kit は YAML + 汎用開発ツールとして維持する。
py-kit は references/python/ サブフォルダに Python コーディング規約を格納し、
CLAUDE.md インデックスで AI が状況に応じて参照先を選べるようにする。

**PR128 での設計決定事項**:
- py-kit/references/python/CLAUDE.md（インデックス）を配置
- Python 規約ファイル: python-core / python-architecture / python-fastapi / python-llm / python-testing / python-scripts
- py-script / py-project スキルを py-kit に移動（dev-kit から削除）
- YAML スキルは dev-kit に残す
- dev-kit の python.md / python.jp.md は削除（py-kit に分割して格納）

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #128 | AIイシュー自動発見システム構想ノートの整備（プラグイン設計を確定） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260526_create-py-kit-plugin/PR129/QA.md` |
| 済 | plugins/py-kit/ を新規作成（plugin.json） | `plugins/py-kit/.claude-plugin/plugin.json` |
| 済 | references/python/ を作成し規約ファイルを配置 | `plugins/py-kit/references/python/python-core.md` 他 |
| 済 | references/python/_index.md（インデックス）を作成 | `plugins/py-kit/references/python/_index.md` |
| 済 | py-script / py-project スキルを py-kit に移動 | `plugins/py-kit/skills/py-script/` `plugins/py-kit/skills/py-project/` |
| 済 | dev-kit から python.md / py-script / py-project を削除 | `plugins/dev-kit/references/python.md` 他 |
| 済 | marketplace.json を更新（py-kit エントリを追加） | `.claude-plugin/marketplace.json` |
| 済 | notes を更新する | `.work/notes/AIイシュー自動発見システム構想.md` |

## 参考ドキュメント

- `.work/notes/AIイシュー自動発見システム構想.md`: py-kit 設計の背景

| 済 | references/python/ をフラット化（python/ サブフォルダを廃止） | `plugins/py-kit/references/` |
| 済 | 各リファレンスファイルの JP ミラーを作成 | `plugins/py-kit/references/*.jp.md` |
| 済 | `_index.md` → `CLAUDE.md` にリネーム（references 配下に確実にインデックスが読まれるように） | `plugins/py-kit/references/CLAUDE.md` |
| 済 | フォルダ構成案を QA に複数案として記録（AITuber 構成を参考） — QA-001 で純DDD（案A）に決定 | QA.md |
| 済 | python-architecture に Template Method パターンを追記 | `python-architecture.md` |
| 済 | 各リファレンスを next-kit 並みの詳細度に書き直し（コメント必須/推奨表・禁止事項・✅/❌対比例） | `python-core.md` / `python-architecture.md` / `python-scripts.md` / `python-testing.md` / `python-fastapi.md` / `python-llm.md` |
| 済 | プロジェクトフォルダ構成セクションは QA 決定（純DDD）を反映 | `python-architecture.md` § 8 |
| 済 | 全 JP ミラーも英語の改訂に同期 | `*.jp.md` |
| 済 | glossary を `CLAUDE.md` 表記に修正 | `.claude/rules/core/glossary.md` |
| 済 | SKILL.md / SKILL.jp.md の `references/_index.md` 参照を `references/CLAUDE.md` に更新 | `skills/py-script/SKILL.md` 他 |

## 参考ドキュメント追加

- PR132 (`/mnt/c/Users/shuhe/repo/my-plugins-wt-PR132/plugins/next-kit/`): 詳細度・書きぶりの参考（コメント必須/推奨表、禁止事項明記、✅/❌対比例、CLAUDE.md インデックス）
- AITuber プロジェクト (`/mnt/c/Users/shuhe/repo/aituber/src/aituber`): フォルダ構成案の元（modes + integrations + runtime のハイブリッド設計）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| review-py-kit-plugin | PR135（review-next-kit-plugin）と同パターン。py-kit references を Claude Code の一般ベストプラクティスと照合し、改善提案を**質問形式で大量に QA.md** に書き出す。ユーザーが採否判断 → 採用分を実装。**評価観点**: フォルダ/ファイル分割粒度（次PRのフック注入を見据えた小単位化）・命名規則（編集ファイルパスとマッチさせやすい）・コメントルールの過不足・型ヒント網羅性・抽象パターンの実用性（Template Method/Strategy 使い分け基準は妥当か）・抜け観点（async・並行制御・パッケージング・パフォーマンス・セキュリティ・依存管理・packaging/distribution）・純DDDの硬さの妥当性（簡易プロジェクトでも適用してよいか）・既存PythonコードベースのSAITuber参考実装との照合 | 即時実施可 |
| add-py-kit-references-injection-hook | PR136（add-next-kit-references-injection-hook）と同パターン。`plugins/dev-kit/hooks/hooks.json` を参考に PreToolUse フックを構築し、編集対象 `.py` ファイルのパス/命名から対応する `references/*.md` を Claude へ自動注入する。**設計方針**: フォルダ構造（`references/llm/`・`references/api/`・`references/scripts/` 等）とファイル名規約でマッチング；リファレンスは「広すぎて無関係内容を含む」のを避け小さく分割；現状のフラット構成 + python-skill-dispatch（全 `.py` に一律発火）から、より細かい注入へ移行。**対応マッピング案**: `**/infrastructure/llm/**/*.py` → `python-llm.md`／`**/interface/api/**/*.py` → `python-fastapi.md`／`**/tests/**/test_*.py` → `python-testing.md`／単発 `.py` → `python-scripts.md`／その他 `**/{domain,application,infrastructure,interface}/**/*.py` → `python-architecture.md`+`python-core.md` | 「review-py-kit-plugin」が完了したら（references 構成が確定してからフック設計に着手） |

## QA

なし
