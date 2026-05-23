---
name: ui-kit:debug-fab-modify
description: debug-fab ウィジェットの UI や動作を変更する（uidev.js / uidev.css）。FAB の動作変更、ボタンの追加・削除、ピッカーモードのロジック変更、コピーペイロードの更新などに使用。実装 → ドキュメント同期 → バージョンバンプ → example.html 確認の流れをガイドする。例: "FABの動作変えて", "コピーボタン追加して", "ピッカーモードの挙動直して"。
---

> このファイルは SKILL.md の日本語ミラーです。Claude Code が自動読み込みするのは `SKILL.md`（英語版）のみです。
> 編集時は先に日本語版を更新し、その後 SKILL.md に同じ変更を反映してください。

# ui-kit:debug-fab-modify — ウィジェット変更ワークフロー

`uidev.js` / `uidev.css` の変更を、実装・ドキュメント同期・バージョンバンプ・`example.html` 手動確認まで通してガイドするスキル。

---

## アーキテクチャ概要（コードに触れる前に必読）

```
templates/
  uidev.js        ← ウィジェットロジック（ピッカー、コピー、DOM）
  uidev.css       ← ウィジェットスタイル（FAB、トップバー、ピッカーハイライト）
  example.html    ← 手動スモークテスト用ページ
  CLAUDE.md       ← 使用ガイド（このフォルダで作業時に自動読み込み）
SKILL.md          ← スキル定義（オペレーションフロー、リファレンス）
```

主な設計上の制約:
- **FAB は右下固定** — 位置切り替えなし
- **トップコピーバー** はピッカーモード中のみ表示（`body.uidev-picker-active`）
- **`copyAndStop(feedbackBtn)`** が FAB・トップボタン共通のコピーハンドラー。`feedbackBtn` に渡したボタンに "✓ コピーしました" を表示する
- **コピー失敗時は `stop()` を呼ばない** — ピッカーモードを維持してリトライ可能にする
- ログバッファは常に記録されるが、画面上には表示しない

---

## 手順

### Step 1: 変更種別を特定する

| 変更種別 | 触るファイル |
|---|---|
| ピッカー動作（選択・トグル・コピー） | `uidev.js` → `startPicker()` |
| FAB の外観またはクリック動作 | `uidev.js` → `init()` + `startPicker()`、`uidev.css` |
| トップバーボタン（ラベル、表示、動作） | `uidev.js` → `refresh()` / `copyAndStop()`、`uidev.css` |
| コピーペイロードの形式 | `uidev.js` → `buildPayload()` |
| 新しい UI 要素 | `uidev.js` → `buildDOM()`、`uidev.css` |

→ Step 2 へ

---

### Step 2: 変更を実装する

#### `uidev.js` の主要関数

| 関数 | 役割 |
|---|---|
| `buildDOM()` | FAB + トップバーの HTML を生成 |
| `startPicker(root)` | ピッカーモードに入り、すべてのイベントリスナーを登録 |
| `refresh()` | `currentSelected.size` に基づいて FAB・トップボタンのラベルを更新 |
| `copyAndStop(feedbackBtn)` | 共通コピーハンドラー — 選択 > 0 なら `feedbackBtn` にフィードバックを表示してコピー。失敗時は `stop()` を呼ばない |
| `onTopCopyClick()` | トップボタン用のラッパー（`copyAndStop(topCopyBtn)` を呼ぶ名前付き関数） |
| `stop()` | ピッカーモードを終了、すべてのリスナーを削除、FAB・ボタンをリセット |
| `buildPayload(elements)` | ページ・ファイル・ログ・要素を含む JSON を組み立てる |

#### CSS の規則

- FAB スタイル: `.uidev-fab`、`.uidev-fab[data-picker-active="true"]`
- トップバー表示: `.uidev-top-bar { display: none }` / `body.uidev-picker-active .uidev-top-bar { display: block }`
- ピッカーハイライト: `.uidev-picker-highlight`（ホバー）、`.uidev-picker-selected`（選択済み）

→ Step 3 へ

---

### Step 3: ドキュメントを同期する

動作または UI に変更があった場合は**両方**を更新する:

1. **`SKILL.md`** — オペレーションフロー（番号付き手順、各ボタンの動作）
2. **`templates/CLAUDE.md`** — Operations テーブル（アクション → 結果 の行）

チェックリスト:
- [ ] `SKILL.md` のオペレーションフローが新しい動作と一致しているか
- [ ] `CLAUDE.md` の Operations テーブルが各ボタンを正確に説明しているか

→ Step 4 へ

---

### Step 4: バージョンをバンプする

以下の2ファイルを更新:

```
plugins/ui-kit/.claude-plugin/plugin.json  →  "version": "x.y.z"
.claude-plugin/marketplace.json            →  "version": "x.y.z"  (ui-kit エントリ)
```

| 変更種別 | バンプ |
|---|---|
| バグ修正 | PATCH |
| 新しい UI 要素または動作変更 | MINOR |
| 完全な再設計 | MAJOR |

→ Step 5 へ

---

### Step 5: example.html で確認する

ブラウザで `templates/example.html` を開き、以下を確認:

- [ ] FAB（🐛）クリック → ピッカーモード開始
- [ ] トップバーが表示され "要素を選択してください" と表示される
- [ ] 要素をクリック → 選択（緑枠）; トップボタン → "📋 コピー (N件)"
- [ ] FAB クリック（0件）→ ピッカー終了（キャンセル）
- [ ] FAB クリック（N件）→ JSON コピー + FAB に "✓ コピーしました" 表示 + ピッカー終了
- [ ] トップボタンクリック（N件）→ JSON コピー + ボタンに "✓ コピーしました" 表示 + ピッカー終了
- [ ] トップボタンクリック（0件）→ ピッカー終了（キャンセル）
- [ ] `Esc` → コピーなしでピッカー終了

`example.html` が変更内容を正確に示さない場合は更新する。

→ 完了

---

## リファレンス

- `{plugin_root}/skills/debug-fab/templates/CLAUDE.md` — ウィジェットの使用方法と JSON スキーマ
- `{plugin_root}/skills/debug-fab/SKILL.md` — 組み込みスキル（画面への埋め込み方法）
- `.claude/rules/debug-fab-template-sync.md` — ファイル同期チェックリスト（自動読み込み）
