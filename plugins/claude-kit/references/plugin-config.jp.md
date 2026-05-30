<!-- This file is a Japanese mirror of plugin-config.md. When updating the English original, update this file too. -->
# プラグイン Config スキルガイド

Claude Code プラグインに **config スキル** を追加する方法。config スキルとは、`settings.json` を
手動で編集しなくても、プラグインの env 変数制御の機能をユーザーがトグルできるスキルです。

英語正本: `references/plugin-config.md`

参照実装: `plugins/work/skills/plugin-config/SKILL.md`（`work:plugin-config` スキル）

---

## なぜすべてのプラグインに config スキルが必要か

プラグインはオプトイン / オプトアウトの挙動を環境変数で制御します（`environment.md` 参照）。
config スキルがない場合、ユーザーは JSON を手編集しなければなりません。

config スキルを実装することで：
- すべてのトグルの現在の状態を一目で確認できる
- `AskUserQuestion` で値を切り替えられる（JSON 編集不要）
- スコープ（プロジェクト vs ユーザー）を透過的に扱える
- 「キーなし = デフォルト有効」の契約を守り、`"true"` の書き残しを防ぐ

---

## config スキルを追加するタイミング

プラグインに **ユーザーが変更することを想定した env トグルが 1 つ以上ある** 場合に追加します。
開発者向けのみの内部設定（例: `*_INJECTION_TTL`）だけのプラグインには不要です。

最低基準：プラグインの `CLAUDE.md` の `## Environment Variables` セクションに、
ユーザー向けの ON/OFF トグルが 1 つ以上あること。

---

## 管理トグルの規約

すべてのユーザー向けトグルは同じ契約に従います：

| 状態 | 表現 |
|---|---|
| ON（デフォルト） | `env` ブロックにキーが **存在しない** |
| OFF | `env.{KEY}` を `"false"` に設定 |
| 明示的 ON | `env.{KEY}` を `"true"` に設定（不在と同等。明確さが必要な場合のみ使用）|

**デフォルトへの戻し方**: キーを削除する（`"デフォルトに戻す"` オプション）— `"true"` を設定するのは避けること。

例外: `{PREFIX}_INJECTION_DISABLE` は逆極性（truthy = オフ）のため、config スキルの管理対象外。
settings.json の手動編集で対応すること。

---

## スキル構造 — 5 ステップの AskUserQuestion ループ

```
Step 1: 現在の状態を読み取る        → 状態テーブルを表示
Step 2: env 変数を選択（ループ先頭） → AskUserQuestion（変数選択 + 完了オプション）
Step 3: 値とスコープを選択          → AskUserQuestion（2 問を 1 回で）
Step 4: 変更を適用                 → settings.json を編集・変更を記録・Step 2 に戻る
Step 5: 報告                       → 全変更のサマリーテーブル
```

### Step 1 — 現在の状態を読み取る

```bash
cat .claude/settings.json 2>/dev/null || echo '{}'
cat ~/.claude/settings.json 2>/dev/null || echo '{}'
```

各トグルについて: 不在 → **ON**、`"false"/"0"/"no"/"off"` → **OFF**、それ以外 → **ON**

`AskUserQuestion` を呼ぶ前に状態テーブルをテキスト出力：

```
## 現在の設定

| env 変数 | 状態 | 設定ファイル |
|---|---|---|
| FOO_BAR | ON | .claude/settings.json |
| FOO_BAZ | OFF | ~/.claude/settings.json |
```

### Step 2 — env 変数を選択（ループ先頭）

管理トグルの番号付き一覧をテキストで出力し、ターンを終了してユーザーの入力を待つ
（番号を入力、または `0` / `q` で終了）：

```
設定する変数の番号を入力してください（0 で終了）:

  1. [{状態}] {VAR_NAME_1} — {機能の説明}
  2. [{状態}] {VAR_NAME_2} — {機能の説明}
  3. [{状態}] {VAR_NAME_3} — {機能の説明}
  …
  0. 完了（終了）
```

**ここでは `AskUserQuestion` を使わない** — 番号付きリストにすることで、4 オプション上限なしに
すべてのトグルを表示できる。

`0` または `q` が入力された場合 → Step 5 へジャンプ。
それ以外は番号から変数名を特定し → Step 3 へ進む。

### Step 3 — 値とスコープを選択

**2 問を 1 回の呼び出しで** `AskUserQuestion` を呼ぶ：

```yaml
# 問 1 — 値
question: "{VAR_NAME} の値を設定"
header:   "値"
options:
  - label: "デフォルトに戻す（キー削除 = ON）"   description: "env キーを削除してデフォルト有効に戻す"
  - label: "OFF（\"false\" に設定）"            description: "この機能を無効化する"

# 問 2 — スコープ
question: "どの settings.json に書き込みますか？"
header:   "スコープ"
options:
  - label: "プロジェクト（.claude/settings.json）"    description: "このリポジトリのみに適用"
  - label: "ユーザー（~/.claude/settings.json）"     description: "全プロジェクトに適用"
```

### Step 4 — 変更を適用

1. スコープ回答から対象ファイルを決定
2. 既存 JSON を読む（不在の場合は `{}` を使用）
3. `env` オブジェクトが存在することを確認
4. 適用: "デフォルトに戻す" → キー削除; "OFF" → `env.{KEY} = "false"`
5. 2 スペースインデントで書き戻す
6. 変更を記録（変数名、変更前 → 変更後、ファイル）→ Step 2 に戻る

### Step 5 — 報告

```
## 変更完了

| env 変数 | 変更前 | 変更後 | 設定ファイル |
|---|---|---|---|
| FOO_BAR | ON | OFF | .claude/settings.json |
```

変更がない場合 → "変更なし"。

---

## 最小 SKILL.md テンプレート

```markdown
---
name: plugin-config
description: |
  When /{plugin-name}:plugin-config is invoked.
  Or when the user says "設定を変えたい", "env を設定したい", "トグルを切り替えたい".
---

# {plugin-name}:plugin-config — Plugin Toggle Configuration

Interactively configures env toggle variables via `AskUserQuestion`.

---

## Managed Toggles

| env 変数 | 説明 | デフォルト |
|---|---|---|
| `{PREFIX}_FOO` | {機能の説明} | 有効 |

**Rule**: キー不在 = ON（デフォルト有効）。`"false"` に設定 = OFF。ON に戻すにはキーを削除する。

---

## Tasks

### Step 1: Read current state
…
### Step 2: Select env var to configure （ループ先頭）
…
### Step 3: Select value and scope
…
### Step 4: Apply change
…
### Step 5: Report
…
```

---

## リリース前チェックリスト

- [ ] プラグインの `CLAUDE.md` の `## Environment Variables` に管理トグルが全て記載されている
- [ ] 各トグルが「不在 = ON / `"false"` = OFF」の契約に従っている
- [ ] `{PREFIX}_INJECTION_DISABLE`（逆極性）が config スキルの管理対象から**除外**されている
- [ ] SKILL.md の `description` フロントマターが「設定を変えたい」などの自然言語フレーズでトリガーされる
- [ ] プラグインのバージョンバンプと changelog エントリが追加されている
