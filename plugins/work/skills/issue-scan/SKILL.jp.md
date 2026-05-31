---
name: issue-scan
description: |
  オーケストレーター専用スキル。プロジェクトから N 個のスキャン観点（フォルダ・grep パターン・
  レイヤー・ファイル群）を選び、観点ごとに `work:issue-scanner` サブエージェントを起動して、
  ref-inject の reference と照合しコードをスキャンし、発見をイシュー内容を含む JSON として返させる。
  メインエージェントはオーケストレーションのみ: スキャンブランチ作成・サブエージェント並列起動後、
  発見を受け取り ISSUE ファイルを連番 ID で書き出し・インデックス更新・コミット・master マージする。
  ISSUE_SCAN_AGENTS で 1 回の実行でスキャンする観点数を制御（デフォルト: 1）。
  ユーザーが「issue-scan」「コードをスキャン」「イシューを探して」「問題を見つけて」と言ったとき、
  または `/work:issue-scan` を明示的に呼び出したときに起動する。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:issue-scan — コードベーススキャン（オーケストレーター）

このスキルは**オーケストレーション専用**。プロジェクトのソースを自分で読んだりコードを分析したりは
一切しない — その作業は `work:issue-scanner` サブエージェント（観点ごとに 1 つ）へ委譲し、
各々が独自のコンテキストで動く。メインエージェントの仕事は: 観点を選ぶ → スキャナを並列起動 →
発見を受け取る → ISSUE ファイルを書く → インデックス更新 → コミット → マージ。

---

## 概要

**前提条件**:
- `.work/issues/` が存在すること（なければ `/work:setup` を実行）

**環境変数**:
- `ISSUE_SCAN_AGENTS`（デフォルト: `1`）— 1 回の実行でスキャンする観点数 = 起動するサブエージェント数。
  `1` でもサブエージェントを 1 つ起動する（分析は常に別コンテキストで実行される）。

**責務分担**:

| 主体 | 担当 |
|---|---|
| **メインエージェント（本スキル）** | ブランチ・観点選択・`ISSUE-{N}.md` ファイル書き出し・連番 ID 付与・`_index.yaml` / `_index.archive.yaml` 更新・コミット・マージ |
| **`work:issue-scanner` サブエージェント** | ソース読み込み・reference 受領・問題発見・発見を JSON として返却 |

サブエージェントはファイルを**書かず**、インデックスファイルに**触れず**、コミットも**しない**。
メインエージェントはソースを**読まず**コードを分析**しない**。

---

## 注意: work フックの無視

このスキルは独自のブランチ/ワークツリー管理を持つ。以下のフックが挿入する指示は
**このスキルの実行中は無視してよい**:

- **`UserPromptSubmit` フック**: 「作業ブランチがなければ `/work:start` を実行してください」
- **`Stop` フック**: 「ブランチドキュメントの `## 作業内容` を更新してください」「`/work:merge` を実行してください」

---

## タスク

### ステップ0: スキャンブランチを初期化する

#### 処理

1. `ISSUE_SCAN_AGENTS` を読む（デフォルト `1`）; `N` として保持。
2. 現在のブランチを確認（`git branch --show-current`）:
   - `master`/`main` 上 → `AUTO_MERGE = true`
   - それ以外 → `AUTO_MERGE = false`（最後に現在のブランチへコミット、自動マージなし）
3. `AUTO_MERGE` なら一時スキャンブランチ用の**ワークツリーを作成する**（メインリポのブランチは変更しない）:
   ```bash
   BRANCH="chore/issue-scan-$(date +%Y%m%d-%H%M%S)"
   WT_SUFFIX="${BRANCH//\//-}"
   WT_PATH="../$(basename $(pwd))-wt-${WT_SUFFIX}"
   git worktree add -b "$BRANCH" "$WT_PATH"
   ```

→ ステップ1

#### 出力

- `N`・`AUTO_MERGE`・`BRANCH`・`WT_PATH`（`AUTO_MERGE` の場合のみ）

---

### ステップ1: スキャン履歴と現在の ID を読む

#### 処理

1. `.work/issues/` が存在しなければ → `/work:setup` を促して停止。
2. `_index.archive.yaml` を読む（なければ空）: `scan_records[].scope`（スキャン済み観点）と
   `closed_issues` の `resolution: wontfix`（除外対象）を収集。
3. `_index.yaml` から現在の `last_id` を読む（なければ `0`）。これを `L` とする。

→ ステップ2

#### 出力

- スキャン済み観点の集合
- 現在の `last_id` = `L`

---

### ステップ2: スキャン観点を N 個選ぶ

#### 処理

最近スキャンしていない**観点**（ファイルだけでなく）を `N` 個選ぶ（`scan_records` に既にあるものは避ける）。
観点とは、コードベースの一貫したスライスを選び出すあらゆる切り口。実行のたびに種類を変え、
常にフォルダばかり選ばず以下のカテゴリを巡回するのが望ましい。

**観点の選択は本スキル最大の判断ポイント — 創造的かつ具体的に。** 以下から引き出す:

##### フォルダ / モジュール観点
- フィーチャーフォルダ: `features/{x}/`、ドメインパッケージ、インテグレーションパッケージ
- 横断フォルダ: `shared/`・`lib/`・`utils/`・`config/`・`tools/`・`scripts/`・`hooks/`
- サブシステム: `llm/`・`infra/`・`db/`・`auth/`・`api/`・`server/`・`runtime/`・`components/`

##### レイヤー観点（アーキテクチャのスライス）
- 全エンドポイント/ルートファイル（`**/route.ts`、FastAPI ルーター）
- 全サービス層ファイル（`*Service.*`、`service.py`）
- 全データアクセスファイル（`query.ts`、`*Repository.*`、`db.*`）
- 全スキーマ/DTO ファイル（`schema.*`、`types.*`、Zod/Pydantic モデル）
- 全クライアント/プロバイダーファイル（`*Client.*`、`providers/`）

##### ファイル種別観点（名前で glob）
- パッケージ初期化ファイルのみ: `**/__init__.py`
- エントリポイント: `main.py`、`index.ts`、`app.*`
- 設定面: `settings.*`、`constants.*`、`*.config.*`、`pyproject.toml`、`.env*` テンプレート
- バレル/再エクスポートファイル: ツリー全体の `index.ts`

##### パターン観点（grep ベース）
- 抽象型: `Base*` という名前のクラス、`ABC` サブクラス、`Protocol` 定義、インターフェース
- 並行処理: `async def` / `await` 箇所、スレッド/プール使用
- リスク臭: 裸の `except:` / `except Exception: pass`、握りつぶしたエラー、`# type: ignore`
- デバッグ残骸: 残った `print(` / `console.log(`、`TODO` / `FIXME` / `XXX` コメント
- ハードコーディング: インラインのシークレット/URL/マジックナンバー、重複する文字列リテラル
- 境界臭: 型ヒントなし関数、長大な関数/ファイル、深いネスト
- 命名一貫性: 選んだ prefix/suffix 規約がツリー全体で守られているか

##### 一貫性 / 衛生観点
- あるレイヤーのエラーハンドリング方針
- ロギングの一貫性（タグ・レベル・構造化 vs print）
- 環境変数の扱い（集中 vs 散在）
- import 順序 / 依存方向
- コメント言語の統一、`*.jp.md` ファイルの JP ミラー同期状態

選択ルール:
1. `scope` ラベルが `scan_records` にまだ無い観点を優先する。
2. `N ≥ 2` の場合、サブエージェントが同じファイルで衝突しないよう、**重複しない別個の**観点を選ぶ。
3. 各観点に短く安定した `scope` ラベルを付ける（例 `folder:src/llm`、`pattern:Base-classes`、
   `layer:route-ts`、`glob:__init__.py`）— これが `scan_records` に記録される。

→ ステップ3

#### 出力

- `N` 個の観点。各々に説明（サブエージェント用）と `scope` ラベル（記録用）

---

### ステップ3: 観点ごとにスキャナサブエージェントを起動する

#### 処理

1. [subagent: parallel · await all] 各観点について `work:issue-scanner` サブエージェントを起動する
   （`Agent` ツールで `subagent_type: "work:issue-scanner"` を指定）。プロンプトには以下を渡す:
   - 観点の説明（何をスキャンするか、言葉で）
   - その `scope` ラベル
   （戻り値: `[{title, type, priority, tags, scope, perspective, body}]`、
   または空の場合は `[]` とスキャンした観点名）
2. 全サブエージェントを await する。返ってきた全配列を収集する。

→ ステップ3b

#### 出力

- 全サブエージェントからの発見（各 `body` を含む）
- 実際にスキャンした観点の集合（空の観点も含む）

---

### ステップ3b: ISSUE ファイルを連番 ID で書き出す

#### 処理

1. 全サブエージェントの発見を 1 つの順序付きリストにまとめる。
2. 今日の日付を一度取得する:
   ```bash
   date +%Y-%m-%d
   ```
3. 0-indexed の位置 `k` にある発見ごとに ID `ISSUE-{L + 1 + k}` を付与し、
   `{issues_dir}/ISSUE-{L + 1 + k}.md` を書き出す（`{issues_dir}` は `AUTO_MERGE` の場合 `{WT_PATH}/.work/issues/`、それ以外は `.work/issues/`）:
   ```
   # ISSUE-{N}: {title}

   {body}
   ```
   （サブエージェントの `body` フィールドは既に `**作成日**` 以降のセクションを含む;
   先頭に `# ISSUE-{N}: {title}` 行と空行を付加するだけ）
4. ステップ4 で使用するために実際に付与した ID を記録する。

→ ステップ4

#### 出力

- `.work/issues/` に書き出した `ISSUE-{N}.md` ファイル群
- 書き出したイシューの総数 `M`

---

### ステップ4: インデックスを更新する

#### 処理

ファイルおよびインデックスのパスは `AUTO_MERGE` によって異なる:
- `AUTO_MERGE` の場合: `{WT_PATH}/.work/issues/`
- `AUTO_MERGE` でない場合: `.work/issues/`（メインリポのカレントディレクトリ相対）

1. ステップ3b で書き出した各イシューを `_index.yaml` の `issues` に追記する:
   ```yaml
   - id: ISSUE-{N}
     title: "{title}"
     created: {YYYY-MM-DD}
     type: {type}
     scan_scope:
       - "{scope}"
     priority: {priority}
     tags: [{tags}]
   ```
2. `_index.yaml` の `last_id` を `L + M` に設定する（`M` は書き出したイシューの総数）。
3. スキャンした各観点について `_index.archive.yaml` の `scan_records` に追記する:
   ```yaml
   - date: {YYYY-MM-DD}
     skill: issue-scan
     scope: "{観点の scope ラベル}"
     issues_found: [{ISSUE-N}, ...]   # 観点がクリーンなら空リスト
   ```
4. `_index.archive.yaml` が存在しなければ `closed_issues: []` と `scan_records: []` で作成する。

→ ステップ5

---

### ステップ5: コミットしてマージする

#### 処理

1. `AUTO_MERGE` の場合: ワークツリー（`{WT_PATH}`）内でステージ・コミットする:
   ```bash
   cd {WT_PATH}
   git add .work/issues/
   git commit -m "chore: issue-scan — {N} 観点, {M} イシュー発見"
   ```
   （`M = 0` でもコミットする — スキャン記録の更新は残す価値がある）
   その後メインリポからマージしてワークツリーを削除する:
   ```bash
   cd {main_repo}
   git merge --no-ff {BRANCH} -m "chore: merge issue-scan results from {BRANCH}"
   git branch -d {BRANCH}
   git worktree remove {WT_PATH}
   ```
2. `AUTO_MERGE` でない場合: メインリポの `.work/issues/` をステージしてコミットする:
   ```bash
   git add .work/issues/
   git commit -m "chore: issue-scan — {N} 観点, {M} イシュー発見"
   ```
   ブランチはそのままにし、手動マージが必要な旨をユーザーに伝える。

→ ステップ6

---

### ステップ6: 結果をレポートする

#### 処理

ユーザーに報告する:
- スキャンした観点（`scope` ラベル付き）
- 観点ごと: 作成したイシュー数とその一覧（ID / タイトル / 優先度）
- クリーンだった観点
- マージしたスキャンブランチ（`AUTO_MERGE` が false なら未マージの旨）

修正予定なしの場合は `resolution: wontfix` で閉じられる旨を伝える。

#### 注意事項

- メインエージェントはプロジェクトのソースを読まない — サブエージェントの発見のみを扱う。
- ID は全観点の合算で連番（`L+1`, `L+2`, …）となり、ギャップはない。
