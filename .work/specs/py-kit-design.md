---
created_at: 2026-05-17
updates:
  - 2026-05-17 — 初版作成（PR28）
related_specs: []
related_prs:
  - PR28
---

# py-kit — Python プラグイン設計仕様

## 概要

`py-kit` は Python 開発全般をサポートする Claude Code プラグイン。
簡易スクリプト作成・新規プロジェクト作成・既存プロジェクト対応の3スキルと、
共通 Python ルール資料（`references/`）、クラス構造/設定/テスト連携ルールで構成される。

## プラグイン構造

```
plugins/py-kit/
├── .claude-plugin/
│   └── plugin.json
├── references/
│   └── python-standards.md   # 全スキル共通のPythonルール集
├── skills/
│   ├── py-script/            # 簡易スクリプト作成
│   │   ├── SKILL.md
│   │   └── SKILL.jp.md
│   ├── py-new-project/       # 新規プロジェクト作成
│   │   ├── SKILL.md
│   │   └── SKILL.jp.md
│   └── py-project/           # 既存プロジェクト対応（確認・修正）
│       ├── SKILL.md
│       └── SKILL.jp.md
└── rules/                    # スキルから生成されるルールのテンプレート
    ├── class-structure.md
    ├── config-source-link.md
    └── source-test-link.md
```

## スキル仕様

### py-script（簡易スクリプト作成）

**トリガー**: 「スクリプト作って」「ちょっとしたPythonコード書いて」など単発スクリプト依頼時  
**対象**: 単一ファイル or 数ファイル程度の小規模スクリプト  
**特徴**: プロジェクト構造は作らない。`references/python-standards.md` の命名・コメント規則に従う

### py-new-project（新規プロジェクト作成）

**トリガー**: 「新しい Python プロジェクト作って」「土台から作りたい」など  
**対象**: pyproject.toml・src レイアウト・テスト構造などを含む本格プロジェクト  
**ステップ**:
1. 要件ヒアリング（ドメイン・ユースケース・外部依存）
2. DDD に基づくレイヤー設計（domain / application / infrastructure / interface）
3. プロジェクト構造生成（src レイアウト）
4. 依存関係注入・インターフェース設計
5. ルール生成（class-structure / config-source-link / source-test-link）
6. テスト雛形生成（結合テスト・ユースケーステスト）

### py-project（既存プロジェクト対応）

**トリガー**: 「このコード見て」「機能追加して」「リファクタして」など既存コードへの変更全般  
**対象**: すでに存在する Python プロジェクトへの確認・修正・機能追加  
**ステップ**:
1. プロジェクト構造把握（レイヤー・依存関係確認）
2. `references/python-standards.md` に照らした品質チェック
3. 変更実装
4. ルール照合（関連クラス・設定・テストへの波及確認）
5. テスト更新（変更対象に紐づくテストケースを更新）

## references/python-standards.md に含める内容

- 命名規則（モジュール・クラス・関数・変数・定数）
- コメント規則（なぜを書く、何は書かない）
- SOLID 原則（5原則すべて、Python での具体例付き）
- DRY 原則（コード重複排除、abstraction タイミング）
- ドメイン駆動設計（エンティティ・値オブジェクト・集約・リポジトリ・サービス）
- 拡張性重視の設計（Strategy/Factory/Decorator パターン、DI）
- テスト方針（単体テストは原則不要、結合テスト・ユースケーステスト推奨）
- 型ヒント（全箇所に付ける、`Protocol` でインターフェース定義）

## ルール管理

ルールは `py-new-project` / `py-project` スキルの実行ステップとして
プロジェクトの `.claude/rules/` に自動生成する（案B採用予定 — QA-001 参照）。

### class-structure ルール

対象: 抽象クラス・インターフェース（Protocol）・具象クラスが存在するファイル群  
トリガー: 上記いずれかのファイルが変更されたとき  
チェック: 継承ツリー内の他クラスへの波及確認を促す

### config-source-link ルール

対象: 設定ファイル（`.yaml`, `.toml`, `.env`, `.json`）とそれを読み込むソースファイル  
トリガー: 設定ファイルまたはソースファイルが変更されたとき  
チェック: 対応するソース or 設定の同期確認

### source-test-link ルール

対象: `src/` 配下のモジュールと `tests/` 配下のテストファイル  
トリガー: ソースファイルが変更されたとき  
チェック: 対応するテストファイルの更新確認を促す

## テスト方針

| テスト種別 | 方針 |
|---|---|
| 単体テスト | 原則不要（AI時代は実装コストに見合わない） |
| モジュール間結合テスト | 必要に応じて作成 |
| ユースケーステスト | ユースケース単位で作成（外部 I/O 境界のみモック） |
| E2E テスト | CLI / API エンドポイントがある場合に作成 |
