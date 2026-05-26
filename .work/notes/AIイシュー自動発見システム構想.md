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
AI が定期/随時 コードベース・画面を調査
  → イシュー候補リストを生成
    → ユーザーが選択・優先度判断
      → 選んだものを PR 化
```

ユーザーは「何を直すか」の判断に集中、「何が問題か」の発見は AI に委譲する。

---

## イシュー分類と AI 検出可能性

### ◎ 高: AI が自律的に発見しやすい

#### 1. 共通化漏れ (Refactoring)
- 複数の `.html` で同じ構造が重複している箇所
- 片方を修正したのに他方に反映されていないパターン
- **検出方法**: AST 差分解析 / 構造的類似度 / 修正コミット後に他ファイルをスキャン

#### 2. 設定・規約違反 (Static Check)
- CLAUDE.md / rules に記載のルール違反
- **検出方法**: rules に書いてある grep コマンドをそのまま実行

#### 3. 実行時エラーパターン (Static Bug)
- `import` エラー・型エラー (pyright / mypy)
- **検出方法**: linter を走らせるだけ

#### 4. 依存・バージョン問題
- pinned したパッケージに既知の CVE
- **検出方法**: `pip-audit` / `npm audit`

---

### △ 中: 文脈・設計意図の理解が必要

#### 5. 要件定義漏れ起因のバグ
- 機能として動いているが想定外の省略がある

#### 6. 画面間の機能非対称性
- A 画面にある便利な機能が B 画面にない

#### 7. UX / デザイン問題
- ボタン配置が使いづらい / 情報が見つからない

---

### × 低: 人間の創造性が必要

#### 8. 新機能アイデア
- まったく新しい発想は AI には出せない

---

## プラグイン設計（決定事項）

### プラグイン構成

| プラグイン名 | 役割 | 備考 |
|---|---|---|
| `py-kit` | Python コーディング規約・スキャフォールド | 旧 `dev-kit` をリネーム |
| `ui-kit` | HTML/CSS/JS 実装規約・スキャフォールド | 現状維持 |
| `audit-kit` | イシュー自動発見スキル群 | 新規作成 |
| `work-kit` | PR ライフサイクル管理 + イシュークローズ統合 | 既存に merge 連携を追加 |

### PR 区切り案

| PR | 内容 | 実施条件 |
|---|---|---|
| PR-A | dev-kit → py-kit リネーム (MAJOR) | 即時実施可 |
| PR-B | py-kit references 細分化 | PR-A 完了後 |
| PR-C | audit-kit プラグイン作成（issue-rule-scan 先行） | 即時実施可 |
| PR-D | work-kit merge へのイシュークローズ統合 | PR-C 完了後 |

---

## フォルダ構成

### py-kit (旧 dev-kit)

```
plugins/py-kit/
├── .claude-plugin/plugin.json
├── references/
│   ├── python-core.md          # 命名・型・SOLID・DRY
│   ├── python-architecture.md  # レイヤードアーキテクチャ・フォルダ構成
│   ├── python-fastapi.md       # エンドポイント設計・共通化パターン
│   ├── python-llm.md           # LLM クライアントアーキテクチャ
│   ├── python-testing.md       # テストポリシー
│   └── python-scripts.md       # スクリプト構成・bat テンプレート
└── skills/
    ├── py-script/
    ├── py-project/
    └── yaml/                   # ← yaml スキルの所属は QA-001 で確認中
```

### audit-kit (新規)

```
plugins/audit-kit/
├── .claude-plugin/plugin.json
├── references/
│   └── issue-format.md         # issue ファイルのフォーマット規約
└── skills/
    ├── issue-scan/             # オーケストレーター
    ├── issue-rule-scan/        # grep ベースのルール違反検知（最優先）
    ├── issue-refactor-scan/    # コード重複・乖離検知
    ├── issue-ui-scan/          # 画面 UX 問題検知
    └── issue-backend-scan/     # バックエンドレイヤー別検知
```

### .work/issues/ (対象プロジェクト側)

```
.work/issues/
├── .gitignore               # _index.yaml を除外
├── _index.yaml              # オープンイシュー一覧（git 管理外・ローカルのみ）
├── _index.archive.yaml      # クローズ済み + スキャン履歴（git 管理）
├── closed/
│   ├── ISSUE-001.md
│   └── ...
├── ISSUE-002.md
└── ISSUE-003.md
```

---

## イシューメタデータ

### `_index.yaml` (オープン、git 管理外)

```yaml
last_id: 5
issues:
  - id: ISSUE-005
    title: "personal-chat.html: HistoryDetailPanel 未適用"
    created: 2026-05-26
    type: refactor          # refactor | rule-violation | ui | backend
    source_skill: issue-refactor-scan
    scan_scope: "frontend/dev/personal-chat.html"
    priority: medium        # high | medium | low（AI 提案、ユーザーが変更可）
    applied_to_kit: false   # py-kit/ui-kit の規約へ反映済みか
```

### `_index.archive.yaml` (クローズ + スキャン履歴、git 管理)

```yaml
closed_issues:
  - id: ISSUE-001
    title: "..."
    closed: 2026-05-26
    resolution: resolved    # resolved | wontfix
    linked_pr: 130
    applied_to_kit: true

scan_records:
  - date: 2026-05-26
    skill: issue-refactor-scan
    scope: "frontend/dev/personal-chat.html"
    issues_found: [ISSUE-005]
  - date: 2026-05-26
    skill: issue-backend-scan
    scope: "layer:endpoint"
    issues_found: []
```

`scan_records` を見れば「どこまでスキャン済みか」が分かるため、
次回スキャン時に未実施箇所を特定できる。

---

## スキルフロー

### スキャン単位の設計原則

- **1 回のスキャンは小さく**: 全部一気にやらず、1 ファイル or 1 レイヤーずつ
- **フロントエンド**: 1 HTML ファイル単位（画面単位）
- **バックエンド**:
  - 横スキャン（レイヤー別）: endpoint → application → domain → infrastructure → llm-client
  - 縦スキャン（ルート別）: 将来追加（1 エンドポイントの全レイヤーをトレース）

### `/audit-kit:issue-rule-scan`

```
1. .claude/rules/**/*.md を読む
2. 「検証:」セクション内の grep コマンドを抽出
3. 全コマンドを実行
4. 非0件 → ISSUE-{N}.md を作成、_index.yaml に追記
5. scan_records に記録
6. 新規イシュー一覧をレポート
```

毎コミット後の自動実行候補（最も軽量・確実）

---

### `/audit-kit:issue-refactor-scan`

```
フロントエンドモード:
1. scan_records を読み、未スキャンの HTML ファイルを特定
2. 次の 1 ファイルを選択
3. 同種ファイル（命名パターンで推定）と構造比較
4. git log で「片方だけ最近変更」パターンを検出
5. 問題あり → ISSUE-{N}.md 作成
6. scan_records に記録（スコープ: ファイルパス）
```

---

### `/audit-kit:issue-ui-scan`

```
1. scan_records を読み、未スキャンの HTML ファイルを特定
2. 次の 1 ファイルを選択
3. ui-kit/references を参照しながら以下をチェック:
   - 主要機能への到達クリック数
   - エラー時フィードバックの有無
   - loading 状態の表示
   - 他画面と機能が非対称の箇所
4. 問題あり → ISSUE-{N}.md 作成
5. scan_records に記録
```

---

### `/audit-kit:issue-backend-scan`

```
横（レイヤー）スキャン:
1. scan_records で未スキャンのレイヤーを特定
   順序: endpoint → application → domain → infrastructure → llm-client
2. 対象レイヤーのファイル群を読む
3. py-kit/references/python-{layer}.md の規約と照合
4. 問題あり → ISSUE-{N}.md 作成
5. scan_records に記録（スコープ: layer:{name}）
```

---

### `/audit-kit:issue-scan`（オーケストレーター）

```
1. issue-rule-scan を常に実行（軽量）
2. _index.yaml の残件数を表示
3. 「次に何をスキャンしますか？」とユーザーに確認
   → frontend | backend-layer | ui から選択
4. 選択されたスキルを実行
5. 新規イシュー一覧を出力
```

---

### work-kit merge 統合（PR-D で追加予定）

```
マージ時の追加ステップ:
1. TODO.md に「## 関連イシュー」セクションがあるか確認
2. あれば、記載イシューを closed/ に移動
3. _index.yaml から削除
4. _index.archive.yaml に追記（linked_pr: {N}）
```

---

## イシューファイルフォーマット

```markdown
## [2026-05-26] issue-refactor-scan

### ISSUE-005: personal-chat.html — HistoryDetailPanel 未適用
- **種別**: Refactoring
- **重要度**: 中
- **対象**: `frontend/dev/personal-chat.html:245`
- **内容**: `history-viewer.html` で導入した `HistoryDetailPanel` 共通部品が
  `personal-chat.html` の履歴詳細表示に未適用。
  同種の変更が必要になった際に二重メンテが発生する。
- **推奨対応**: PR として `HistoryDetailPanel` を適用
- **apply_to_kit**: false
```

---

## 実現難易度・優先順位

| スキル | 検出精度 | 実装コスト | 優先度 |
|---|---|---|---|
| `issue-rule-scan` | ◎ 高（grep で確定） | 低 | ★★★ 最優先 |
| `issue-refactor-scan` | △ 中（ファイル比較） | 中 | ★★ 次点 |
| `issue-ui-scan` | △ 中（提案止まり） | 中 | ★★ 次点 |
| `issue-backend-scan` | ○ 中〜高 | 中 | ★★ 次点 |

---

## 未決定事項（QA）

詳細は `.work/tasks/20260526_update-ai-issue-notes/PR128/QA.md` 参照。

| QA番号 | 内容 | 状態 |
|---|---|---|
| QA-001 | YAML スキルの所属プラグイン（py-kit に残す vs 別プラグイン） | 未決定 |
| QA-002 | `.work/issues/` の設置先プロジェクト（AITuber専用 vs 汎用） | 未決定 |
| QA-003 | audit-kit から py-kit/ui-kit references を参照する方法 | 未決定 |
| QA-004 | dev-kit → py-kit リネームの既存プロジェクト移行手順 | 未決定 |

---

## 懸念・課題

### イシューの重複・古さ問題
- 同じ問題が毎回スキャンで検出される → `wontfix` フラグで対応
- `_index.yaml` で管理するため重複 ID は発行されない

### 誤検出対応
- AI の誤検出は必ず起きる
- ユーザーが「これは問題ではない」とマークできる仕組みが必要（`wontfix`）

### スキャン頻度
- `issue-rule-scan`: コミット後フックで自動実行
- その他: 手動 or 週次スケジュール
