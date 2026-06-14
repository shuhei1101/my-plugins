---
name: work:issue-resolve-auto
description: イシューを解決する
disable-model-invocation: true
---

# issue-resolve-auto — レビュー済みイシューを消化する

## タスク

### Step 1: 最上位の対応可能イシューを探す

- `.work/issues/targets/`配下にISSUEが無ければ → 報告して停止。
- `.work/issues/targets/` の候補を上から5つ決定する。
   - 決定した5つのイシューを`.work/issues/progress/`に移す
- 各イシューファイルを開き `対応する／対応しない` のチェックボックスを読む：
   - `- [x] 対応しない` → REJECT アクション（Step 2）。
   - `- [x] 対応する` → ACCEPT アクション（Step 3）。
   - 全て `- [ ]`（未チェック＝未レビュー）→ スキップ。
- 対応可能イシューが無ければ → 「対応可能なイシューはありません」と報告してループ終了

### Step 2: REJECT — 使い捨てブランチでクローズし即 master へマージ
- ブランチを作成する
- `worktree_create` MCP ツール（work-tools サーバー）を実行し、ワークツリーを作成する
- リジェクトされたイシューごとに `issue_close` MCP ツール（work-tools サーバー）を実行する:
  - issues_dir: `{リポジトリルート}/.work/issues` の絶対パス（`.work/issues/progress/` ではなく `.work/issues/` を指定すること）
  - issue_id: `ISSUE-{N}`
  - resolution: `wontfix`

### Step 3: `direct_merge` の値を決定する:
#### `direct_merge: true`
- イシューが`対応する`かつ`マージ前確認不要`にチェックが入っている場合
- リファクタリング（表面の動作は変わらない変更）
- 命名規則変更
- タイムゾーン挙動
- タイムアウト追加
- 例外ハンドル変更（握り潰し改善など）
- ロガー変更
- ラベル、テキスト変更など、簡易的な見た目変更
- dead codeの除去
- 分散ロジックの共通化

#### `direct_merge: false`
- その他

### Step 4: サブエージェント実行準備

1. 移譲前に、メインリポジトリの `_index.yaml` でイシューを in-progress にする
   - `issue_set_status` MCP ツール（work-tools サーバー）を実行:
     - issues_dir: `{リポジトリルート}/.work/issues` の絶対パス / issue_id: `ISSUE-{N}` / status: `in_progress`

### Step 5 `issue-resolver`をサブエージェントで実行する
以下を渡す
- イシューID
- イシュードキュメントパス
- 採用方針（採用案 + QA 回答 + 意思の補足）
- `direct_merge`（特に、該当イシューがrefactor typeならtrue）
- その他、実行に必要な情報
（なおサブエージェントは一回のイテレーションでは非同期で最大5件実行すること）

### Step 6 サブエージェントから返却
- 完了・直接マージ済み → リゾルバーが既にマージ・イシュークローズ済み。
- 完了・マージ待ち → 特になし（ユーザがあとでマージ依頼を別セッションに依頼する）

### Step 7 結果報告書の作成
- Step 6で受けた報告をもとに報告書を作成する
  - 配置場所: `.work/issues/logs/{YYMMDD-HHMM}-{title}.resolve.md`
  - 記載ルールは作成時に読み込まれる
  - `worktree_create` MCP ツール（work-tools サーバー）でブランチ作成、ワークツリー作成し、その中で記載
  - 完了後、`/merge`スキルを実行しmasterにマージする
