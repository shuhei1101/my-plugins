# PR138 — review-py-kit-plugin

## 概要

py-kit プラグイン全体を **Claude Code の一般的なベストプラクティス知識** で評価し、改善提案を **質問形式で大量に QA.md に書き出す**。ユーザーが一個ずつ判断し、採用したものを当 PR で実装する（PR135 / review-next-kit-plugin と同パターン）。

**評価観点（例）**:

- フォルダ / ファイル分割粒度（次PR の自動注入フックを見据えた小単位化）
  - 現状 `references/` フラット構成（python-core / python-architecture / python-scripts / python-testing / python-fastapi / python-llm）が、ファイルパス起点の自動注入に対して粒度として妥当か
  - LLM / API / scripts / domain / infrastructure / interface 等のサブフォルダ化を検討すべきか
  - 1 ファイルが扱う範囲が広すぎて「無関係な内容も一緒に注入される」リスクがないか
- 命名規則
  - フックの `tool_input.file_path` パターンとマッチさせやすい reference 名・配置か
  - reference ファイル名が「編集対象 Python ファイルから自然に連想できる名前」になっているか
- コメントルールの過不足
  - `python-core.md § 2` の必須/推奨表は実用的か（過剰にコメントを書かせていないか / 必要なケースを抜かしていないか）
  - PR 番号付き変更履歴コメントの基準（PR132 由来）は Python でも適用すべきか
- 型ヒント網羅性
  - 「全公開シンボル必須」「裸 Any 禁止」「Protocol vs ABC」「NewType」「TypedDict」「Literal」等の規定は妥当か
  - 抜けている観点（`@override`・`Self` 型・`ParamSpec`・dataclass の `kw_only`・Generic 構文 PEP 695 等）はないか
- 抽象パターンの実用性
  - Strategy / Template Method / Factory / Decorator / Observer の使い分け表は実プロジェクトで再現可能か
  - 各パターンに「使うべきでないケース」が明示されているか
- 抜け観点
  - 非同期（asyncio・タスクキャンセル・タイムアウト・並行性制御・asyncio.Lock / Semaphore）
  - パッケージング / 配布（`pyproject.toml` の `[project.scripts]`・wheel / sdist・PyPI publish）
  - 依存管理（`uv` / `pip-tools` / Poetry の選定方針・lockfile・dev/prod 分離）
  - パフォーマンス（プロファイリング・GIL 回避・multiprocessing vs multithreading vs asyncio の使い分け）
  - セキュリティ（依存脆弱性スキャン・secret スキャン・SQL injection / path traversal 等の Python 特有の落とし穴）
  - エラー観測性（Sentry・OpenTelemetry・構造化ログの設計）
  - CI / CD（lint / type-check / test の自動実行）
  - データ整合性（DB トランザクション・冪等性キー・分散ロック）
- 純DDDの硬さ
  - 簡易プロジェクト（CLI ツール・小規模サービス）にも純DDD を適用するのは過剰でないか
  - 「機能型を許容するライン」を引くべきか（QA-001 で純DDD単独を選んだが、規模分岐を再検討する余地）
- AITuber 参考実装との照合
  - AITuber の実プロジェクト構成（modes + integrations + runtime ハイブリッド）と py-kit の純DDD で齟齬がないか
  - AITuber を py-kit 規約に従ってリファクタする場合、現実的に当てはまるか

**流れ**:

1. AI が py-kit の references を全て読み、評価
2. 改善提案を質問形式で QA.md に大量に書く（例：「python-llm.md をさらに分割して `llm-providers.md` と `llm-task-clients.md` にしませんか？」「`@override` の使用ルールを追加しませんか？」「PEP 695 のジェネリック構文を採用しませんか？」）
3. ユーザーが一個ずつ「採用 / 不採用 / 後回し」を判断
4. 採用されたものを当 PR で実装（references の書き直し・分割・追加など）

**背景（PR129 からの引き継ぎ）**:

- PR129 で py-kit を新規作成（dev-kit から Python 分離、純DDD採用、CLAUDE.md インデックス化、next-kit 並みの詳細度に書き直し）
- 設計はユーザーの経験ベースと next-kit のスタイル参考から構築されたもので、外部のベストプラクティスとの照合は未実施
- **長期方針（ユーザー意向）**: 将来的に、編集対象 Python ファイルのパス / 命名に応じて対応 reference を自動注入する PreToolUse フック（PR139 候補）を実装したい。そのために references は **小単位に分割** され、フォルダ / ファイル名で **パスマッチング可能** な構成が望ましい。当 PR の評価では、この長期方針を念頭に references の構造的妥当性を必ず点検する
- 「自分が考えたやり方で、特に何かに習ってるわけじゃないから、一度評価しておきたい」とのユーザー意向（PR135 と同じ動機）

### 実施条件

即時実施可（PR129 がマージ済みで py-kit references が一通り整備済みであること）

### 関連PR

| PR番号 | 概要 |
|---|---|
| #129 | py-kit プラグイン新規作成（評価対象） |
| #135 | review-next-kit-plugin（パターン参照元） |
| #136 | add-next-kit-references-injection-hook（次PR候補の設計参考） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/.../PR138/QA.md` |
| 済 | py-kit の全 references を読み、ベストプラクティスと照合する | `plugins/py-kit/references/**` |
| 済 | フォルダ / ファイル分割粒度を評価（自動注入フックを見据えて） | (調査) |
| 済 | 抜け観点を洗い出す（async・packaging・依存管理・パフォーマンス・セキュリティ・観測性・CI/CD） | (調査) |
| 済 | AITuber 参考実装と py-kit 規約の照合 | `/mnt/c/Users/shuhe/repo/aituber/src/aituber` |
| 済 | 改善提案を**質問形式で QA.md に大量に**書き出す（QA-001 から QA-110、計 110 件） | `.work/tasks/.../PR138/QA.md` |
| 済 | ユーザーに採否を確認し、QA に判断を記録する | (ユーザー対話) |
| 済 | 次PR候補の予約（実装フェーズを別 PR へ分離） | (本 TODO の「次PR候補」参照) |

**当 PR の実装は行わない**。採用された提案の実装・SKILL.md 書き直し・JP ミラー・version bump・notes 更新・CLAUDE.md / glossary 整備はすべて次 PR `rebuild-py-kit-references` で行う。フック実装は更にその後の PR `add-py-kit-references-injection-hook` で行う。

## 参考ドキュメント

- `plugins/py-kit/references/`: 評価対象の py-kit リファレンス（PR129 で整備）
- `plugins/next-kit/references/`: 詳細度・書きぶりのスタイル参考（PR132）
- `.work/tasks/20260527_review-next-kit-plugin/PR135/`: 同パターン PR の TODO/QA（72 件の QA 構成が参考）
- `.work/tasks/20260527_add-next-kit-references-injection-hook/PR136/`: 自動注入フックの設計参考
- `plugins/dev-kit/hooks/hooks.json`: 既存 python-skill-dispatch / yaml-skill-dispatch（PR129 マージ後は `plugins/py-kit/hooks/hooks.json` に移動）
- `/mnt/c/Users/shuhe/repo/aituber/src/aituber`: 実プロジェクト参考（modes + integrations + runtime ハイブリッド型）
- `.work/notes/AIイシュー自動発見システム構想.md`: 設計背景

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| rebuild-py-kit-references | PR138 で確定した新方針（DDD 廃止 → 機能フォルダ型 + TypeScript 風 + 関数型ファースト）に従って py-kit の references を全面再構成。**作業**: ① 既存 6 ファイル（python-{core,architecture,scripts,testing,fastapi,llm}.md）を解体、② 新フォルダ構成（38 ファイル、QA.md § D-1 参照）へ移行、③ 各 reference 本文を新方針で書き直し、④ `references/index.yaml` 新規作成（メタデータ + 注入フック星取り表、QA.md § D-6 参照）、⑤ `references/CLAUDE.md` を「index.yaml を読め」式に書き換え、⑥ SKILL.md（py-project / py-script）を新方針で全面書き直し、⑦ `plugins/py-kit/CLAUDE.md` 新設、⑧ plugin.json / marketplace.json を MAJOR バンプ（2.0.0）、⑨ changelogs/v2.0.0.md 作成、⑩ glossary 更新（新方針用語追加 / 旧 DDD 用語削除）、⑪ JP ミラー全件同時生成、⑫ `.work/notes/AIイシュー自動発見システム構想.md` の py-kit セクション更新。実装方針の判断材料は PR138 の `.work/tasks/20260527_review-py-kit-plugin/PR138/QA.md` を参照。 | 即時実施可（PR138 マージ後） |
| add-py-kit-references-injection-hook | py-kit に references 自動注入フック（PreToolUse）を追加。`references/index.yaml` の `injection_rules` を読んで、編集対象ファイルパスにマッチする `required` を必読・`optional` を任意参照として Claude へ注入する。**実装**: `/claude-kit:hook-creator` で hook 作成 → Python スクリプト本体で `index.yaml` 読み込み + Jinja2 でプロンプト render + `decision: block` で reason に流し込む。Jinja2 テンプレ（必読/任意 + description）も同 PR で整備。 | 「rebuild-py-kit-references」が完了したら |

## QA

なし
