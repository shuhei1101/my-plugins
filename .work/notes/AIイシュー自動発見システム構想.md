# AI イシュー自動発見システム 構想ノート

作成: 2026-05-26

---

## 背景・動機

### 現在のフロー
```
ユーザーが画面を見て気づく
  → Claude Code に話す
    → PR 作成・実装
```

### 目指すフロー
```
AI がコードベース・画面を調査（呼び出し時に実行）
  → イシュー候補リストを生成
    → ユーザーが選択・優先度判断
      → 選んだものを PR 化
```

またはユーザーが口頭で困りごとを話す
  → AI が内容を解釈し複数のイシューに分割して登録

ユーザーは「何を直すか」の判断に集中、「何が問題か」の発見は AI に委譲する。
※ 定期スケジュール実行はプラグイン外（外部プログラムが Claude Code に投げる形）で対応。

---

## プラグイン設計（決定事項）

### プラグイン構成

| プラグイン名 | 役割 | 状態 |
|---|---|---|
| `dev-kit` | YAML スキル + 汎用開発ツール | 現状維持 |
| `py-kit` | Python コーディング規約・スキャフォールド | 新規作成（dev-kit から Python を分離） |
| `html-kit` | HTML/CSS/JS 実装規約・スキャフォールド | ui-kit をリネーム |
| `next-kit` | Next.js 実装規約・スキャフォールド | ✅ PR132 作成 / PR135 references 全面再構築 |
| `work-kit` | PR ライフサイクル管理 + イシュー管理スキル | 既存に2スキル追加 |

### PR 区切り案

| PR | 内容 | 状態 |
|---|---|---|
| PR-A | py-kit プラグイン新規作成（dev-kit から Python を分離） | ✅ PR129 作成 / PR138 大方針 / PR140 references 全面再構築・自動注入フック実装 |
| PR-B | ui-kit → html-kit リネーム | ✅ PR130 完了 |
| PR-C | work-kit に issue-scan・issue-create・issue-save スキルを追加 + `*-kit` フックに Read マッチャー追加 | ✅ PR131 完了 |
| PR-D | work-kit merge スキルにイシュークローズ処理を統合 | ✅ PR146 完了 |
| PR-E | next-kit プラグイン新規作成 + references 全面再構築（90 ファイル + 自動注入フック） | ✅ PR132 作成 / PR135 全面再構築 |

---

## フォルダ構成

### dev-kit（変更なし）

```
plugins/dev-kit/
├── .claude-plugin/plugin.json
├── references/
│   └── yaml.md
└── skills/
    └── yaml/
```

### py-kit（v2.0.0 — PR129 新規作成 / PR138 大方針確定 / PR140 実装）

```
plugins/py-kit/
├── .claude-plugin/plugin.json     # v2.0.0
├── CLAUDE.md / CLAUDE.jp.md       # プラグイン全体ガイド（PR140 新設）
├── changelogs/
│   └── v2.0.0.md
├── hooks/
│   ├── hooks.json
│   └── prompts/
│       ├── python-skill-dispatch.md
│       └── python-skill-dispatch.jp.md
├── references/                    # 38 ファイル（jp ミラー込みで 76）構成
│   ├── CLAUDE.md / CLAUDE.jp.md   # 「index.yaml を読め」式の最小指示
│   ├── index.yaml                 # メタデータ + 注入星取り表（PR141 のフックが読む）
│   ├── core/                      # 命名・コメント・型・言語ルール・スタイル（5 ファイル）
│   ├── architecture/              # 機能フォルダ型レイアウト・TypeScript 風・関数配線・依存方向（4 ファイル）
│   ├── shared/                    # logger / settings / errors / types / constants（5 ファイル）
│   ├── scripts/                   # 単一スクリプト + ランチャー + tkinter（4 ファイル）
│   ├── testing/                   # 結合テスト方針・pytest・Mock（3 ファイル）
│   ├── concurrency/               # asyncio / parallelism（2 ファイル）
│   ├── packaging/                 # pyproject / uv / distribution / python-versions（4 ファイル）
│   ├── performance/               # プロファイラチート集（1 ファイル）
│   ├── llm/                       # providers / Instructor / prompts / cost-cache / exceptions-retry（5 ファイル）
│   └── fastapi/                   # app / routes / schemas / auth-and-errors / health（5 ファイル）
└── skills/
    ├── py-script/                 # SKILL.md / SKILL.jp.md（PR140 で書き直し）
    └── py-project/                # SKILL.md / SKILL.jp.md（PR140 で書き直し）
```

**設計方針（v2.0.0）**:
- レイアウトは **機能フォルダ型**（`src/{pkg}/{shared,features,integrations,runtime,server}/`、`shared/` と `main.py` のみ必須）
- 振る舞いは **モジュールレベルの関数**。クラスは DTO とライブラリ要求のみ
- 抽象化は **`type` エイリアス（関数の型）+ `Protocol`**（クラス継承による DIP は使わない）
- DI は `functools.partial` で `build_handlers(settings) -> Handlers` パターン
- DB は対象外（Web 関連は next-kit に委譲）
- テストは **結合テスト + スモークテストのみ**（単体テストなし、スモークはユーザー手動実行限定）

**自動注入の仕組み（✅ PR140 で実装済み）**:
- `references/index.yaml` の `injection_rules` に「編集対象ファイルパス → 必読 reference / 任意 reference」を集約
- `hooks/inject_references.py` (PreToolUse) が `Edit` / `Write` 時に該当 reference を `decision: block` で Claude へ自動注入する

**詳細度**: PR132 next-kit の書きぶり（必須/推奨表・✅/❌対比例・禁止事項リスト）を Python 用に展開。各ファイルが本格リファレンス（数百行規模）。

### next-kit（v3.1.0 — PR132 新規作成 / PR135 全面再構築）

```
plugins/next-kit/
├── .claude-plugin/plugin.json     # v3.1.0
├── CLAUDE.md / CLAUDE.jp.md       # プラグイン全体ガイド
├── changelogs/
│   └── v3.1.0.md
├── hooks/
│   ├── hooks.json
│   ├── inject_references.py       # next-references-injection フック (PR135)
│   └── templates/
│       ├── injection.md.j2
│       └── injection.jp.md.j2
└── references/                    # 90 ファイル（jp ミラー込みで 180）構成
    ├── CLAUDE.md / CLAUDE.jp.md   # 「index.yaml を読め」式の最小指示
    ├── index.yaml / index.jp.yaml # reference 一覧 + メタデータ
    ├── injection_rules.yaml       # pattern → required/optional マッピング
    ├── frontend/                  # page.tsx・screen.tsx・フォーム・コンポーネント等（~40 ファイル）
    ├── backend/                   # route.ts・query.ts・db.ts・auth・Service 等（~40 ファイル）
    ├── shared/                    # 型定義・定数・ユーティリティ
    ├── testing/                   # テスト規約
    ├── devops/                    # デプロイ・CI 等
    └── devtools/                  # 開発ツール設定
```

**設計方針（PR135 全面再構築後）**:
- **1 ファイル = 1 ユースケース**: `query.ts` 編集 → `query-ts.md` だけ inject（他のファイル種別の情報は入らない）
- ファイル名がフックのトリガーキーワードに直接対応（`route.ts` → `route-ts.md`、`EditScreen.tsx` → `edit-screen-tsx.md`）
- 比較・選定・トレードオフセクションは完全削除（決定済みの情報は不要、inject 時にノイズになる）
- Stack: shadcn/ui + Tailwind + react-hook-form + Zod + TanStack Query + Drizzle + Server Actions + Better Auth

**自動注入の仕組み（✅ PR135 で実装済み）**:
- `references/injection_rules.yaml` の `rules:` に「編集対象ファイルパス → required/optional reference」を集約
- `hooks/inject_references.py` (PreToolUse: Edit/Write/MultiEdit) が該当 reference を `decision: block` で Claude へ自動注入
- `NEXT_KIT_INJECTION_LANG=jp` で日本語版テンプレに切替（デフォルト en）

### html-kit（ui-kit からリネーム）

```
plugins/html-kit/
├── .claude-plugin/plugin.json
├── references/
│   ├── principles.md
│   └── ui-design.md
└── skills/
    ├── implement/
    ├── logging/
    ├── mock/
    └── debug-fab/
```

### work-kit（追加スキル）

```
plugins/work-kit/skills/
├── ...（既存スキル）
├── issue-scan/     # コードベース自動スキャン
└── issue-create/   # ユーザーの口頭説明からイシューを生成
```

### .work/issues/（対象プロジェクト側・work-kit setup で作成）

```
.work/issues/
├── .gitignore               # _index.yaml を除外
├── _index.yaml              # オープンイシュー一覧（git 管理外）
├── _index.archive.yaml      # クローズ済み + スキャン履歴（git 管理）
├── closed/
│   ├── ISSUE-001.md
│   └── ...
├── ISSUE-002.md
└── ISSUE-003.md
```

---

## References 設計原則（フック自動注入前提）

PR135 / PR140 の設計経験から確立した原則。issue-scan が references を参照する場合も同様に適用する。

### 1 ファイル = 1 ユースケース

- 「`query.ts` を編集したとき inject される reference」は `query-ts.md` 1 ファイルだけ
- 1 つの reference に複数のファイル種別を詰め込まない
- ファイル名 = トリガーキーワード（`injection_rules.yaml` の pattern と 1:1 対応）

### injection_rules.yaml から設計を始める

reference の目次（TOC）ではなく「どのファイル編集でこの reference を読ませたいか」を先に決め、そこからファイル名・内容を導く。

### 削除するもの

- 比較・選定・トレードオフセクション → `.work/notes/` か commit メッセージに記録
- 実装者が「編集中のファイルとは無関係」な情報 → 別 reference に分離 or 削除

### 参照

- インシデント: `bestprac-over-usecase-references-bloat.md`（ベストプラ網羅型の失敗例）
- ルール: `.claude/rules/feature/kit-hooks-index-sync.md`（kit 間の構造同期強制）

---

## kit-hooks-index-sync ルール

`py-kit` と `next-kit`（および将来の `*-kit`）は **同じ references 自動注入構造** を共有する:

| ファイル | 役割 |
|---|---|
| `hooks/inject_references.py` | PreToolUse フック本体（plugin ごとに env var 名・ログタグのみ異なる） |
| `hooks/hooks.json` | フック登録（PreToolUse: Edit/Write/MultiEdit） |
| `hooks/templates/injection.md.j2` + `.jp.md.j2` | 注入テンプレ（Jinja2） |
| `references/index.yaml` + `index.jp.yaml` | reference 一覧 + メタデータ |
| `references/injection_rules.yaml` | pattern → required/optional マッピング |
| `references/CLAUDE.md` + `CLAUDE.jp.md` | 「index.yaml を読め」式インデックス |

**片方の kit で構造を変えたら、他の kit も同じコミットで変える**（`.claude/rules/feature/kit-hooks-index-sync.md` で強制）。

共通化（共通スクリプト化）は PR140 で試みたが、各 plugin が独立 install される都合上断念。ルールで「同コミット更新」を強制する形に落ち着いた。

---

## 学びとアンチパターン

### ベストプラ網羅型 references の失敗（PR135）

**何が起きたか**: PR135 当初、「ベストプラクティスを網羅する」観点で 46 ファイル構成を設計。`api-routes.md` に 6 種類のファイル型の規約を詰め込み、`auth.md` に認証ライブラリの比較表を収録した。

**なぜ失敗か**: `query.ts` を 1 行編集したときに、関係ない 5 種類のファイル型の情報まで inject される。比較表は決定後には不要なのに毎回 inject されるノイズになる。

**解決**: QA-073 で全面再分割。46 → 90 ファイル、ファイル名をトリガーキーワードに対応させた（`query-ts.md`、`edit-screen-tsx.md` など）。比較・選定セクションは全削除。

**詳細**: `.claude/references/incidents/bestprac-over-usecase-references-bloat.md`

---

## イシューメタデータ

### `_index.yaml`（オープン、git 管理外）

```yaml
last_id: 5
issues:
  - id: ISSUE-005
    title: "personal-chat.html: HistoryDetailPanel 未適用"
    created: 2026-05-26
    type: refactor          # refactor | rule-violation | ui | backend
    scan_scope:
      - "frontend/dev/personal-chat.html"
      - "frontend/dev/history-viewer.html"
    priority: medium        # high | medium | low（AI 提案、ユーザーが変更可）
    tags: [frontend, history]
```

### `_index.archive.yaml`（クローズ + スキャン履歴、git 管理）

```yaml
closed_issues:
  - id: ISSUE-001
    title: "..."
    closed: 2026-05-26
    resolution: resolved    # resolved | wontfix
    linked_pr: 130          # 対応した PR 番号
    tags: [frontend, history]

scan_records:
  - date: 2026-05-26
    skill: issue-scan
    scope: "frontend/dev/personal-chat.html"  # スキャン対象の画面
    issues_found: [ISSUE-005]
  - date: 2026-05-26
    skill: issue-scan
    scope: "layer:endpoint"
    issues_found: []
```

#### wontfix について

`resolution: wontfix` は「この問題は把握しているが意図的に修正しない」という意思決定の記録。
スキャンのたびに同じ問題が再検出されないよう、`wontfix` でクローズされたイシューはスキャン結果から除外する。

#### linked_pr の連携（✅ PR146 で実装済み）

- `_index.archive.yaml` の `closed_issues[].linked_pr` に対応 PR 番号を記録
- TODO.md の `## 関連イシュー` テーブル（カラム: `ID | 概要 | resolution`）で、このイシューと対応 PR・解決区分を紐付け
- work-kit `merge` スキルが Step 5（`set-completed` / `archive` の前）で TODO.md の `## 関連イシュー` を読み、行ごとに `plugins/work-kit/scripts/issue-tool.py close` を呼んで自動クローズする
  - イシューファイル: `.work/issues/ISSUE-{N}.md` → `.work/issues/closed/ISSUE-{N}.md` に git rename
  - `_index.yaml`: 該当エントリを削除（gitignore のまま）
  - `_index.archive.yaml.closed_issues`: `linked_pr` 付きエントリを追記
- `.work/issues/` 自体が存在しないプロジェクト（イシュー管理未導入）では silent skip

---

## スキルフロー

### スキャン単位の設計原則

- **フロントエンド**: 1 画面（HTML ファイル）単位でスキャン
- **バックエンド**:
  - 横スキャン（レイヤー別）: endpoint → application → domain → infrastructure → llm-client
  - 縦スキャン（ルート別）: 将来追加（1 エンドポイントの全レイヤーをトレース）
- **スキャン履歴**: `_index.archive.yaml` の `scan_records` で「どこまでスキャン済みか」を管理

---

### `/work:issue-scan`

`issue-scan` はオーケストレーター専用。メインはソースもイシュー本文も読まず、分析は全て `work:issue-scanner` サブエージェント内で行う。

```
Step 0. master 確認 → 一時スキャンブランチ作成、ISSUE_SCAN_AGENTS=N を読む
Step 1. _index.archive.yaml の scan_records（スキャン済み観点）と _index.yaml の last_id=L を読む
Step 2. スキャン観点を N 個選ぶ（フォルダ/grep/レイヤー/ファイル群/パターン — 観点カタログから巡回選択）
Step 3. 各観点に ID ブロック割当（START_i = L+1+i*SLOT, SLOT=30）→ work:issue-scanner を N 個並列起動
        各サブエージェント: 観点をスキャン → ISSUE-{N}.md を作成（先採番ブロック使用）→ メタデータのみ返す
Step 4. 戻り値（メタデータのみ）を集約し _index.yaml / _index.archive.yaml を更新
Step 5. スキャンブランチへコミット → master に --no-ff マージ → ブランチ削除
Step 6. スキャン結果をレポート
```

責務分担: サブエージェントは「ISSUE ファイル作成まで」（共有 index には触れず・コミットしない）、メインは「ID 先採番・index 更新・コミット・マージ」を集約する。並列で同一 worktree にコミットすると git 競合するため、コミットはメインに一本化している。

---

### `/work-kit:issue-create`

```
1. ユーザーが困りごとを口頭で説明する
2. AI が内容を解釈し、独立した問題に分割
3. 各問題を ISSUE-{N}.md に整形して保存
4. _index.yaml に追記
5. 作成したイシュー一覧をレポート
```

例: 「チャット画面の履歴が見づらいし、設定を変えても次回起動時にリセットされる」
→ ISSUE-006: チャット履歴 UI の視認性改善
→ ISSUE-007: 設定の永続化不具合

---

## 懸念・課題

### イシューの重複・古さ問題
- 同じ問題が毎回スキャンで検出される
- `wontfix` でクローズ → 次回スキャンから除外

### 誤検出対応
- AI の誤検出は必ず起きる
- ユーザーが `wontfix` でクローズ可能

### スキャン頻度
- `issue-scan` は単発でも `/loop /work:issue-scan` による連続ループでも実行可能
- 毎回実行でスキャンブランチ（`chore/issue-scan-YYMMDD-HHMMSS`）を自動作成し、master に `--no-ff` でマージして終了
- `ISSUE_SCAN_AGENTS=N` で 1 回の実行当たりのスキャン観点数を制御（デフォルト 1）
  - N=1 でも必ず 1 つの `work:issue-scanner` サブエージェントを別コンテキストで起動する（メインは分析しない）
  - N≥2: N 個のサブエージェントを並列起動し、各エージェントが 1 観点をスキャン

---

## 次のステップ（AI イシュー自動発見の具体実装に向けて）

PR135 / PR140 の成果により、フック自動注入の基盤は py-kit / next-kit の両方で揃った。
「AI がコードベースを規約と照合し、イシューを自動発見する」という構想の実装前提が整った状態。

### 残タスク

| タスク | 状態 | 備考 |
|---|---|---|
| PR-D: merge スキルにイシュークローズ処理を統合 | ✅ PR146 完了 | work-kit issue-scan/create が前提（PR131 完了済み） |
| issue-scan の自動ループ＋オーケストレーター化 | ✅ feat/issue-scan-auto-loop 完了 | `work:issue-scanner` エージェント新設。観点ベースのスキャン、ISSUE_SCAN_AGENTS で並列数制御、ブランチ自動作成・マージ、/loop で継続スキャン |
| issue-scan の references 参照精度向上 | 未検討 | next-kit / py-kit references が 1 ファイル = 1 ユースケース化された今、scan 時の粒度を合わせる |
| スキャン対象の拡張（Next.js フロントエンド） | 未検討 | 現在は HTML / backend が対象。next-kit プロジェクトへの適用を検討 |

### 基盤として確立したもの（PR135 / PR140 の成果）

- **py-kit** (v2.0.0): 38 ファイル、`inject_references.py` で自動注入済み
- **next-kit** (v3.1.0): 90 ファイル、`inject_references.py` で自動注入済み
- **kit-hooks-index-sync ルール**: 両 kit の構造が同一フォーマットを維持することを保証
- **1 ファイル = 1 ユースケース設計原則**: 将来の新 kit にも適用すべき設計規約として確立
