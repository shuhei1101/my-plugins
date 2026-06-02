<!-- This file is a Japanese mirror of CLAUDE.md. When updating the English original, update this file too. -->
# utils プラグイン開発ガイド

汎用ユーティリティスキルを提供するプラグイン。特定のプラグインに属さない共通作業を担う。

---

## 構成

```
utils/
├── .claude-plugin/plugin.json
├── CLAUDE.md / CLAUDE.jp.md
├── agents/
│   ├── jp-mirror-translator.md       # サブエージェント定義（Sonnet、JP→EN 方向のみ）
│   └── jp-mirror-translator.jp.md
└── skills/
    ├── jp-mirror-sync/
    │   ├── SKILL.md                  # ユーザー向けインターフェース（並列サブエージェント起動）
    │   └── SKILL.jp.md
    └── plugin-migrate/
        ├── SKILL.md
        └── SKILL.jp.md
```

---

## スキル一覧

| スキル | 説明 |
|---|---|
| `utils:jp-mirror-sync` | 1 つ以上の `.jp.md` ファイルを受け取り、各ファイルに対してサブエージェントを並列で起動して英語版を作成・更新する |
| `utils:plugin-migrate` | utils で作成したファイルを最新の規約に合わせる |

## エージェント一覧

| エージェント | 説明 |
|---|---|
| `utils:jp-mirror-translator` | `.jp.md` ファイル 1 件を受け取り、対応する `.md` 英語版を作成または更新する。JP ミラーを正とする。モデル: Sonnet |

---

## 環境変数

なし

---

## Changelog

| バージョン | 日付 | 概要 |
|---|---|---|
| 1.0.0 | 2026-06-02 | 初回リリース — `jp-mirror-sync` スキルと `jp-mirror-translator` サブエージェントを追加 |
