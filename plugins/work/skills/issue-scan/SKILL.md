---
name: work:issue-scan
description: イシューをスキャンするスキル
---

# issue-scan — コードベーススキャン

## タスク
### ステップ1: スキャン履歴と現在の ID を読む

- `.work/issues/` が存在しなければ → `/setup` を促して停止。
- `_index.archive.yaml` を読む（なければ空）— `scan_records[].scope` と `closed_issues` の `resolution: wontfix` を収集。
- `_index.yaml` から現在の `last_id` を読む（なければ `0`）。

### ステップ2: スキャン観点を N 個選ぶ

最近スキャンしていない観点をN個選ぶ（`scan_records` に既にあるものは避ける）。
観点は以下から選ぶ

##### フォルダ / モジュール観点
- フィーチャーフォルダ: `features/{x}/`、ドメインパッケージ、インテグレーションパッケージ
- 横断フォルダ: `shared/`・`lib/`・`utils/`・`config/`・`tools/`・`scripts/`・`hooks/`
- サブシステム: `llm/`・`infra/`・`db/`・`auth/`・`api/`・`server/`・`runtime/`・`components/`

##### レイヤー観点（アーキテクチャのスライス）
- 全エンドポイント/ルートファイル（`/route.ts`、FastAPI ルーター）
- 全サービス層ファイル（`*Service.*`、`service.py`）
- 全データアクセスファイル（`query.ts`、`*Repository.*`、`db.*`）
- 全スキーマ/DTO ファイル（`schema.*`、`types.*`、Zod/Pydantic モデル）
- 全クライアント/プロバイダーファイル（`*Client.*`、`providers/`）

##### ファイル種別観点（名前で glob）
- パッケージ初期化ファイルのみ: `/__init__.py`
- エントリポイント: `main.py`、`index.ts`、`app.*`
- 設定面: `settings.*`、`constants.*`、`*.config.*`、`pyproject.toml`、`.env*` テンプレート
- バレル/再エクスポートファイル: ツリー全体の `index.ts`

##### パターン観点（grep ベース）
- 抽象型: `Base*` という名前のクラス、`ABC` サブクラス、`Protocol` 定義、インターフェース
- 並行処理: `async def` / `await` 箇所、スレッド/プール使用
- リスク臭: 裸の `except:` / `except Exception: pass`、握りつぶしたエラー、`# type: ignore`
- デバッグ残骸: 残った `print(` / `console.log(`、`TODO` / `FIXME` / `XXX` コメント
- ハードコーディング: インラインのシークレット/URL/マジックナンバー、重複する文字列リテラル
- デッドコード、履歴コメント
- 例外握りつぶし、フォールバックは極力しない（エラー補足が出来なくなる）
- 境界臭: 型ヒントなし関数、長大な関数/ファイル、深いネスト
- 命名一貫性: 選んだ prefix/suffix 規約がツリー全体で守られているか

##### 一貫性 / 衛生観点
- あるレイヤーのエラーハンドリング方針
- ロギングの一貫性（タグ・レベル・構造化 vs print）
- 環境変数の扱い（集中 vs 散在）
- import 順序 / 依存方向

選択ルール:
1. `scope` ラベルが `scan_records` にまだ無い観点を優先する。
2. 重複しない別個の観点を選ぶ（サブエージェント間でファイル衝突を防ぐ）。
3. 各観点に短く安定した `scope` ラベルを付ける（例 `folder:src/llm`、`pattern:Base-classes`、`layer:route-ts`、`glob:__init__.py`）。

### ステップ3: 観点ごとにスキャナサブエージェントを起動する

各観点について `issue-scanner` サブエージェントを5つ並列起動する（`Agent` ツール・`subagent_type: "issue-scanner"`）
以下を入力する
- 観点: 何をスキャンするか
- scope ラベル: 観点の短い安定ラベル（例 `folder:src/llm`）
- プロジェクトルート: 作業ディレクトリ

### ステップ3a: サブエージェントの完了報告処理
- 作業完了報告を受けたら、内容を確認する
- もし、簡単なイシューでマージ手前まで実装を進めていた場合
  - `/merge`スキルを実行し当該ブランチを完了させる（特にrefactor typeのものとか）

### ステップ3b: サブエージェントの作業がすべて完了後
- `/worktree-create`スキルを使用し、ブランチとワークツリーを作成する

`.work/issues/ISSUE-{N}.md` を書き出す
先頭に `# ISSUE-{N}: {title}` を書く

### ステップ4: インデックスを更新する

1. 各イシューを `_index.yaml` の `issues` に追記する。
2. `_index.yaml` の `last_id` を 更新する
3. 各観点を `_index.archive.yaml` の `scan_records` に追記する:
4. `_index.archive.yaml` が存在しなければ `closed_issues: []` と `scan_records: []` で作成する。

### Step 4a 結果報告書の作成
- Step 3aで受けた報告をもとに報告書を作成する
  - 配置場所: `{YYMMDD-HHMM}-{title}.scan.md`
  - 記載ルールは作成時に読み込まれる
  - `/worktree-create`スキルでブランチ作成、ワークツリー作成し、その中で記載、完了後masterにマージする

### ステップ5: コミットする
`.work/issues/`と結果報告書 をステージしてコミットする

### ステップ6: マージする
`/merge`スキルを実行し、masterにマージする
