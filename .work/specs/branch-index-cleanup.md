# branch-index-cleanup スキル仕様

## 概要

`/work-kit:branch-index-cleanup` は、git ブランチと `.work/tasks/index.yaml` / `index.archive.yaml` の乖離を整理するワークフロースキル。
未登録ブランチを A/B/C に分類し、削除・archive登録・index反映を実行する。

## 背景

- `pr-pick` は未登録ブランチを一覧表示するだけで、整理は行わない
- aituber PR360 で手動実施したワークフローをスキルとして切り出す

## ワークフロー

### Step 1: 未登録ブランチの収集

1. `git branch` でローカルブランチ一覧を取得
2. `index.yaml` + `index.archive.yaml` に登録済みの PR番号を収集
3. いずれにも登録されていないブランチを「未登録ブランチ」として列挙

### Step 2: 分類

各未登録ブランチを以下の A/B/C に分類する（ユーザーに確認）:

| 分類 | 意味 | 処置 |
|---|---|---|
| A | 完了済み・不要 | ブランチ削除のみ |
| B | 完了済み・記録したい | index.archive.yaml に追記 → ブランチ削除 |
| C | 作業中・継続 | index.yaml に追記（completed: false） |

### Step 2b: B分類のメタデータ入力

ブランチ名（例: `PR42/feat/some-feature`）から以下を自動推定してユーザーに確認する:
- `id` — ブランチ名の PR番号部分
- `title` — ブランチ名のタイプ/タイトル部分をそのまま使用
- `type` — ブランチ名のタイプ部分（feat/fix/refactor 等）
- `summary` — 空欄のまま（ユーザーが任意で追記）

確認後、ユーザーが修正できるインタラクティブフローを採用する。

### Step 3: 処置の実行

- **A**: `git branch -d {branch}` で削除（マージ済みでなければ `-D`）
- **B**: `index.archive.yaml` に YAML エントリを追記 → `git branch -d`
- **C**: `index.yaml` に YAML エントリを追記（`completed: false`）

### Step 4: 結果報告

整理前後のブランチ数・各処置の件数を表形式で報告する。

## ファイル配置

```
plugins/work-kit/skills/branch-index-cleanup/
├── SKILL.md
└── SKILL.jp.md
```

## 関連スキル

- `pr-pick` — 未登録ブランチの一覧表示（本スキルの前処理として使える）
- `work-start` — index.yaml へのエントリ追加（C 分類で内部的に参考にする）
