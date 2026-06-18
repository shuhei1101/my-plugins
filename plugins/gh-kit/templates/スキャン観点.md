# コードスキャン観点メニュー

各観点は「1 スキャナーサブエージェントに渡す 1 単位」。重複を避けつつ N 件選ぶ。

## フォルダ / モジュール

- フィーチャーフォルダ: `features/{x}/`、ドメインパッケージ、インテグレーションパッケージ
- 横断フォルダ: `shared/` `lib/` `utils/` `config/` `tools/` `scripts/` `hooks/`
- サブシステム: `llm/` `infra/` `db/` `auth/` `api/` `server/` `runtime/` `components/`

## レイヤー

- ルートファイル: `/route.ts`、FastAPI ルーター
- サービス層: `*Service.*`、`service.py`
- データアクセス: `query.ts`、`*Repository.*`、`db.*`
- スキーマ/DTO: `schema.*`、`types.*`、Zod/Pydantic モデル
- クライアント/プロバイダー: `*Client.*`、`providers/`

## ファイル種別

- パッケージ初期化: `/__init__.py`
- エントリポイント: `main.py` / `index.ts` / `app.*`
- 設定面: `settings.*` / `constants.*` / `*.config.*` / `.env*` テンプレート
- バレル/再エクスポート: ツリー全体の `index.ts`

## コードパターン（grep ベース）

- 抽象型: `Base*` クラス / `ABC` サブクラス / `Protocol` 定義 / インターフェース
- 並行処理: `async def` / `await` 箇所、スレッド/プール使用、`asyncio.gather` / `Promise.all`
- リスク臭: 裸 `except:` / `except Exception: pass`、握りつぶしたエラー、`# type: ignore` / `// @ts-ignore`
- デバッグ残骸: 残った `print(` / `console.log(`、`TODO` / `FIXME` / `XXX` / `HACK`
- ハードコード: インラインのシークレット/URL/マジックナンバー、重複文字列リテラル
- デッドコード: 未使用 import、未呼び出し関数、コメントアウトされた古いコード
- 命名一貫性: prefix/suffix 規約が守られているか

## テスト網羅・品質 ★

- 実装ファイルに対応するユニットテストファイルが存在するか（`foo.py` ↔ `test_foo.py` / `foo.ts` ↔ `foo.test.ts` 等）
- 結合テスト（integration test）の有無 — API エンドポイント、外部 API クライアント、DB アクセス層
- E2E テストの有無 — クリティカルパス、認証フロー、決済フロー
- テスト品質: アサーション欠落、空テスト（`pass` だけ）、過剰モック（実装をほぼ全モックしてる）
- フィクスチャ重複: 同じセットアップが複数ファイルにコピペされてる
- スキップ/xfail 残骸: 長期間放置されている `@skip` / `@xfail`

## 型安全

- 型ヒント欠落: 公開関数の引数 / 戻り値に型が無い
- `Any` / `any` / `unknown` の散在（型推論が事実上効いていない）
- `# type: ignore` / `// @ts-expect-error` を理由コメントなしで使用
- 型キャストでごまかしている箇所（`cast(X, ...)` / `as X`）

## エラーハンドリング

- 例外握りつぶし（`except Exception: pass` / `try { } catch {}`）
- ユーザー向けエラーメッセージの一貫性（HTTP ステータス・エラーコード・メッセージ形式）
- ドメイン例外 vs 標準例外の混在
- `raise X from e` での原因連鎖が抜けている箇所

## ロギング・観測性

- `print` / `console.log` の残存（`logger` を使うべき箇所）
- ログレベルの使い分け（info / warning / error / critical の境界）
- 構造化ログ / 非構造化ログの混在
- メトリクス・トレーシングの抜け（重要パスでログだけ）

## セキュリティ

- ハードコードシークレット（API key / token / password）
- SQL インジェクション（文字列連結による SQL 構築）
- XSS / CSRF 対策の抜け
- 安全でない URL 生成（ユーザー入力を sanitize なしで URL に）
- ファイルパス traversal（ユーザー入力をパスに直接連結）
- 暗号アルゴリズムの古い使用（MD5 / SHA1 / DES 等）
- 認可チェック抜け（公開すべきでないエンドポイント）

## パフォーマンス

- N+1 クエリ（ループ内 DB アクセス）
- 同期 IO の多用（async コンテキスト内の sync 呼び出し）
- 無駄なループネスト（O(n²) 以上）
- キャッシュ可能なものをキャッシュしていない
- 大量データを 1 回でメモリに乗せている

## 並行性

- 競合状態（共有状態への mutex 無しアクセス）
- デッドロック懸念（複数ロックの取得順序）
- `async def` の中で sync ブロッキング呼び出し
- `asyncio.gather` / `Promise.all` の例外伝播の取りこぼし

## 設定・運用

- 環境変数の集中管理 vs 散在
- import 順序 / 依存方向（DAG 違反）
- 古い deprecated API の使用（フレームワーク・標準ライブラリ）
- lint / format / type-check の設定漏れ・除外項目の理由不明

## ドキュメンテーション

- 公開関数 / 公開クラスの docstring 欠落
- README / セットアップ手順の陳腐化
- API ドキュメントとコードのズレ

## i18n / UX

- ハードコード文字列（i18n catalog に乗っていない）
- アクセシビリティ: `aria-*` 属性、`alt` 属性、キーボードナビゲーション
- レスポンシブ崩れ（CSS のハードコード width 等）

## 依存性

- 使用していない依存（`package.json` / `pyproject.toml` に残ったまま）
- deprecated パッケージの使用
- メジャー更新待ち（古いバージョンで止まっている）

## リソース管理

- ファイル / ソケット / DB 接続のクローズ漏れ（`with` / `using` / `defer` 未使用）
- メモリリーク（イベントリスナーの解除漏れ、循環参照）

## API 設計

- RESTful 違反（GET で副作用、POST で取得等）
- レスポンス形式の一貫性（エラー形式、ページング形式）
- バージョニング戦略の抜け

## 一貫性 / 衛生

- あるレイヤーのエラーハンドリング方針
- ロギングの一貫性（タグ・レベル・構造化）
- env の扱い（集中 vs 散在）
- ファイル末尾改行・空白・改行コードの一貫性
