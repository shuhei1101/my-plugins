---
name: gh:issue-scan
description: コードベースを観点ごとにスキャンし、見つかった問題を GitHub Issues に起票する
---

# issue-scan — コードベーススキャン

## タスク

### ステップ 1: スキャン履歴と既存 Issue を把握

GitHub MCP で以下を取得し、観点の重複を避ける情報源にする。

| No | 取得対象 | 方法 |
|---|---|---|
| 1 | 直近のオープン/クローズ済み Issue | `list_issues` / `search_issues`（ラベル `scan` 付きを優先） |
| 2 | ラベル `scan:{scope}` の使用履歴 | `list_labels` |

`scan:{scope}` ラベルがまだ作られていなければ、観点を起票する段で都度作成する。

### ステップ 2: スキャン観点を N 個選ぶ

直近スキャンで使われていない観点を **N=5** 件選ぶ（環境変数 `GH_ISSUE_SCAN_PERSPECTIVES` で上書き可）。観点は以下から選ぶ。

#### フォルダ / モジュール観点

- フィーチャーフォルダ: `features/{x}/`、ドメインパッケージ、インテグレーションパッケージ
- 横断フォルダ: `shared/` `lib/` `utils/` `config/` `tools/` `scripts/` `hooks/`
- サブシステム: `llm/` `infra/` `db/` `auth/` `api/` `server/` `runtime/` `components/`

#### レイヤー観点

- ルートファイル: `/route.ts`、FastAPI ルーター
- サービス層: `*Service.*`、`service.py`
- データアクセス: `query.ts`、`*Repository.*`、`db.*`
- スキーマ/DTO: `schema.*`、`types.*`、Zod/Pydantic モデル

#### ファイル種別観点

- パッケージ初期化: `/__init__.py`
- エントリポイント: `main.py` / `index.ts` / `app.*`
- 設定面: `settings.*` / `constants.*` / `*.config.*`

#### パターン観点（grep ベース）

- 抽象型: `Base*` クラス、`ABC` サブクラス、`Protocol` 定義
- 並行処理: `async def` / `await` 箇所
- リスク臭: 裸の `except:` / `except Exception: pass`、握りつぶし
- デバッグ残骸: 残った `print(` / `console.log(`、`TODO` / `FIXME`
- ハードコード: インラインのシークレット/URL/マジックナンバー
- デッドコード、履歴コメント

各観点に短く安定した `scope` ラベルを付ける（例 `folder:src/llm`、`pattern:Base-classes`）。

### ステップ 3: スキャナサブエージェントを並列起動

[サブエージェントで並列実行・完了を待つ] 観点ごとに `issue-scanner` サブエージェントを N 件並列起動する。
（戻り値: `[{title, body, labels[], scope, perspective}]` の配列）

各サブエージェントに渡す入力:
- 観点: 何をスキャンするか
- scope ラベル
- プロジェクトルート

### ステップ 4: GitHub に Issue 起票

サブエージェントから返ってきた findings について、1 件ずつ MCP `create_issue` で起票する。

| 引数 | 値 |
|---|---|
| `title` | finding の `title` |
| `body` | finding の `body`（Markdown） |
| `labels` | `[scan, scan:{scope}, type:{type}, priority:{priority}, ...tags]` |

ラベルが存在しない場合は `create_label` で先に作成する（色は scope→teal、type→blue、priority→red 系で統一）。

### ステップ 5: スキャン記録 Issue（オプション）

ステップ 2 で選んだ観点を 1 件の「スキャン履歴 Issue」としてまとめてクローズ状態で起票する（ラベル `scan-record`）。これは次回スキャン時の重複判定に使う。

### ステップ 6: 結果報告

| No | 報告項目 |
|---|---|
| 1 | スキャンした観点とその scope |
| 2 | 起票した Issue 番号と件数 |
| 3 | 0 件だった観点の一覧 |

## 注意

- スキャン結果のローカル保存はしない（GitHub Issue が単一の真実）
- 起票後に再度同じ観点でスキャンしないこと（重複防止）
