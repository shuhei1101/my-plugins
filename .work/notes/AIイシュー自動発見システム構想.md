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
| `next-kit` | Next.js 実装規約・スキャフォールド | 将来 PR（予約済み） |
| `work-kit` | PR ライフサイクル管理 + イシュー管理スキル | 既存に2スキル追加 |

### PR 区切り案

| PR | 内容 | 実施条件 |
|---|---|---|
| PR-A | py-kit プラグイン新規作成（dev-kit から Python を分離） | 即時実施可 |
| PR-B | ui-kit → html-kit リネーム | ✅ PR130 完了 |
| PR-C | work-kit に issue-scan・issue-create スキルを追加 | 即時実施可 |
| PR-D | work-kit merge スキルにイシュークローズ処理を統合 | PR-C 完了後 |
| PR-E | next-kit プラグイン新規作成 | ✅ PR132 で完了 |

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

### py-kit（新規）※ PR129 で実装済み

```
plugins/py-kit/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── hooks.json
│   └── prompts/
│       ├── python-skill-dispatch.md
│       └── python-skill-dispatch.jp.md
├── references/                    # フラット配置（python/ サブフォルダ廃止）
│   ├── CLAUDE.md                  # インデックス（references/ 配下読み込み時に自動ロード）
│   ├── CLAUDE.jp.md
│   ├── python-core.md             # 命名15項目・コメント必須/推奨表・型ヒント網羅・エラー処理・言語ルール
│   ├── python-architecture.md     # SOLID/DRY 詳細・純DDDレイヤー・No Hardcoding・Composition Root・Strategy/Template Method/Factory/Decorator/Observer・Pydantic 境界・プロジェクトフォルダ構成（純DDD）
│   ├── python-fastapi.md          # 純DDD配置（interface/api/）・build_app・lifespan・ルーター規約・Depends()・Pydantic schemas/・middleware・error_handlers
│   ├── python-llm.md              # 三層抽象（task-specific / provider / SDK）・Instructor 構造化出力・プロンプト管理・トークン/コスト/キャッシュ・複数ベンダー併用・LLM 例外階層
│   ├── python-testing.md          # ロガー仕様・テストポリシー表・モック方針・各種テストテンプレ・ソース↔テストリンク
│   ├── python-scripts.md          # 簡易スクリプト構造・bat ルール表・FastAPI run.bat・tkinter GUI・Linux/macOS 等価
│   └── *.jp.md                    # 各ファイルの JP ミラー
└── skills/
    ├── py-script/                 # SKILL.md / SKILL.jp.md
    └── py-project/                # SKILL.md / SKILL.jp.md
```

**設計決定事項（QA-001 / 2026-05-27 決定）**:
- フォルダ構成は**純DDD**（domain / application / infrastructure / interface）
- Protocol の置き場所は `domain/repositories/`（ドメイン層集約）
- 具体実装は `infrastructure/`（依存方向：interface・infrastructure → application → domain）

`references/CLAUDE.md`: スキルが Step 1 で読むインデックス。`references/` 配下の任意ファイルが読み込まれるとClaude Code がコンテキストに自動ロードする設計。タスク → 参照ファイルのマッピング表とクイック「○○を作る」マップを掲載。

**詳細度**: PR132 next-kit の書きぶり（コメント必須/推奨表・✅/❌対比例・禁止事項リスト・Definition of Done チェックリスト）を Python 用に展開。各ファイルが本格リファレンス（数百〜千行規模）。

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

#### linked_pr の連携

- `_index.archive.yaml` の `linked_pr` に対応 PR 番号を記録
- TODO.md に `## 関連イシュー` セクションを設け、このイシューと対応 PR を紐付け
- work-kit merge 実行時に自動でイシューをクローズ（PR-D で実装）

---

## スキルフロー

### スキャン単位の設計原則

- **フロントエンド**: 1 画面（HTML ファイル）単位でスキャン
- **バックエンド**:
  - 横スキャン（レイヤー別）: endpoint → application → domain → infrastructure → llm-client
  - 縦スキャン（ルート別）: 将来追加（1 エンドポイントの全レイヤーをトレース）
- **スキャン履歴**: `_index.archive.yaml` の `scan_records` で「どこまでスキャン済みか」を管理

---

### `/work-kit:issue-scan`

```
1. _index.archive.yaml の scan_records を確認し、未スキャン箇所を特定
2. 今回スキャンする対象をユーザーに提示（frontend画面 / backend-layer / ルール系）
3. 対象領域の py-kit または html-kit references を参照
4. プロジェクトコードを読んで規約と照合
5. 問題あり → ISSUE-{N}.md を作成、_index.yaml に追記
6. scan_records に記録（日時・スコープ・検出イシュー）
7. 新規イシュー一覧をレポート
```

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
- `issue-scan` は手動呼び出しが基本
- 定期実行は外部プログラムから Claude Code に投げる形で対応（プラグイン外）
