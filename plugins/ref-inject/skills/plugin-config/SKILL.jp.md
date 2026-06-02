---
name: ref-inject:plugin-config
description: |
  /ref-inject:plugin-config が呼び出されたとき。
  またはユーザーが「ref-inject の設定を変えたい」「注入を無効にしたい」と言ったとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# ref-inject:plugin-config — プラグイントグル設定

ref-inject プラグインの env トグル変数をインタラクティブに設定するスキル。

> **注意**: ref-inject には現在ユーザー向けの env トグルがありません。
> 消費プラグイン（`dev-kit`、`claude-kit`）は各自の `plugin-config` スキルでトグルを公開しています。
> このスキルは将来のトグル追加に備えたプレースホルダーです。

---

## 管理対象トグル

現在、管理対象のトグルはありません。

---

## タスク

### ステップ 1: 現在の状態を報告

#### 条件

- 常に実行 — 最初に行う

#### 処理

ユーザーに以下を伝える:

```
ref-inject には現在ユーザー向けのトグルがありません。

注入動作を制御する場合は、各消費プラグインの plugin-config を使用してください:
  - /claude-kit:plugin-config — claude-kit の注入設定（JP ミラー / 言語 / TTL）
  - /dev-kit:plugin-config   — dev-kit の言語 opt-in および TypeScript チェック
```

→ 完了。

---

## 注意事項

- ref-inject のキルスイッチ（`${CLAUDE_KIT_INJECTION_DISABLE}` / `${DEV_KIT_INJECTION_DISABLE}`）は逆極性のため、各プラグインの plugin-config では管理しない — `settings.json` を直接編集すること
