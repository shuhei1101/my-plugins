<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# py-kit プラグイン開発者ガイド

> このファイルは `CLAUDE.md` の日本語ミラーです。
> 変更する場合は JP ミラーを先に更新し、その後 `CLAUDE.md` にも反映してください。

py-kit は Python 実装の規約と雛形生成を提供するプラグイン。
**v2.0.0（PR138 / PR140）で大方針を全面刷新** した。旧 v1（純 DDD ベース）から v2（機能フォルダ型 + 関数ファースト + TypeScript 風）へ。

---

## 大方針（v2.0.0）

| | 採用 | 廃止 |
|---|---|---|
| レイアウト | 機能フォルダ型（`src/{pkg}/{shared,features,integrations,runtime,server}/`） | 純 DDD（`domain` / `application` / `infrastructure` / `interface`） |
| 設計 | 関数ファースト（DTO + モジュール関数）+ 関数の型エイリアスで DI | クラスベース DI、Repository クラス、Provider クラス |
| 型 | Python 3.12+ / PEP 695 `type` 文 / `Protocol` / `Callable` | `TypeAlias` 互換 / Java 風インターフェース継承 |
| DB | 対象外（Web は next-kit に委譲） | リポジトリパターン |
| テスト | 結合テスト + スモークテストのみ。単体テストは書かない | 全層単体テスト |
| コメント | exported に 1 行 docstring 必須、設計上重要フィールドの description 必須（next-kit と整合） | docstring optional |

詳細は `references/index.yaml`（reference 一覧）と `references/injection_rules.yaml`（注入ルール）、および各 reference 本文を参照。

---

## references の構造

```
references/
├── CLAUDE.md / CLAUDE.jp.md  # 2 ファイル管理の役割説明（最小指示）
├── index.yaml                  # reference 一覧 + 1 行 description（英語、フックが parse）
├── index.jp.yaml               # 上の日本語ミラー（人間用）
├── injection_rules.yaml      # 編集対象パターン → 必読/任意 reference の星取り表（言語非依存）
├── core/             # 言語ルール（命名・コメント・型・スタイル）
├── architecture/     # 機能フォルダ型 + 関数配線 + 依存方向
├── shared/           # logger / settings / errors / types / constants
├── scripts/          # 単一ファイルスクリプト + ランチャー + tkinter
├── testing/          # 結合テスト + スモーク方針 + Mock パターン
├── concurrency/      # asyncio + parallelism
├── packaging/        # pyproject.toml + uv + distribution
├── performance/      # プロファイラチート集
├── llm/              # LLM プロバイダ / Instructor / プロンプト / キャッシュ
└── fastapi/          # app / routes / schemas / auth-errors / health
```

合計 39 reference ファイル（jp ミラー含めて 78）。

---

## index.yaml と injection_rules.yaml の役割分担

| ファイル | 内容 | 言語 |
|---|---|---|
| `index.yaml` | 全 reference の `path` + 1 行 `description` を YAML リストで | 英語（フックがここから parse） |
| `index.jp.yaml` | 上の日本語ミラー（人間が一覧確認するため） | 日本語 |
| `injection_rules.yaml` | 編集対象ファイルパスの pattern に対して `required` / `optional` reference を割り当てる星取り表 | 言語非依存 |

このマッピングは `py-kit-references-injection` フック（PreToolUse）が
`Edit` / `Write` / `MultiEdit` / `Read` 時に自動で読み、マッチした reference を `decision: block` で
Claude のコンテキストへ注入する。

---

## スキル

| スキル | 用途 |
|---|---|
| `py-kit:py-project` | Python プロジェクト全般（新規 / 既存）。機能フォルダ型レイアウトで雛形生成、または既存コードのレビュー・拡張 |
| `py-kit:py-script` | 単一ファイル / 数ファイルの簡易スクリプト |

スキル選択フックはなし。スキルはユーザーが **明示的に呼び出す**（`/py-kit:py-project`、`/py-kit:py-script`）。
自動 dispatch は PR140 で廃止 — references 自動注入フック（`inject_references.py`）が `Edit` / `Write` のたびに該当 reference を届けるので、別の dispatch フックは冗長。

---

## フック設計の方針

py-kit のフックは `claude-kit` の方針に従う:
- ファイル種別ガードは `PreToolUse`（`UserPromptSubmit` でなく）
- セッションフラグ型ブロック（`/tmp/{hook-name}-{session_id}`）で 1 セッション 1 回だけブロック
- ディスパッチ用 `UserPromptSubmit` は追加しない

**references 自動注入フック** (`py-kit-references-injection`) は v2.4.0（PR157）で `ref-inject` の
仕組みへ移行した。再生成は `/ref-inject:apply` で行い、`hooks/inject_references.py` をプラグインごとに
手書きしない。方針:
- `PreToolUse(Edit|Write|MultiEdit|Read)` で `references/injection_rules.yaml` を読み、`references/index.yaml` から description を引く
- 対象ファイルパスを `rules[].pattern` と glob 照合
- マッチした `required` は **本文全量**、`optional` は **path + description のみ** を Jinja2 テンプレ経由で `decision: block` の reason へ注入
- `optional` の本文は Claude が `Read` で必要なものだけ読む設計
- Read も対象にすることで issue-scan など読み取り経路でも reference の案内を受けられる
- **二層 TTL トークン**（`~/.claude/tokens/py-kit/{session_id}.yaml`）で注入を重複排除。`patterns` と `references` の 2 名前空間を持つ YAML マップで、各エントリは `expires_at`（epoch 秒、= 注入時刻 + TTL）を持つ。`patterns` 層は注入済みパターンを `now < expires_at` の間スキップ、`references` 層は本セッションに（どのパターン経由であれ）既に本文注入済みの `required` を**パスのみ**表示する（複数パターンに紐づくリファレンス本文の二重注入を防ぐ）。どちらも `now >= expires_at` で再注入する
- TTL はデフォルト **3600 秒**、`settings.json` の `env` `PY_KIT_INJECTION_TTL`（秒、両層共通）で上書き可。発火のたびに全セッションのトークンを走査し、両名前空間の期限切れエントリを削除（空になったファイルは削除）
- **`PreCompact` フックはなし** — `/compact` 後は TTL 経過で本文が再注入される。専用の compact リフレッシュフックは不要と判断（PR156 で決定）

---

## バージョン

| バージョン | 主な変更 |
|---|---|
| 2.5.0 | 注入トークンを**二層**化（`patterns` + `references` 名前空間）。複数パターンで共有される `required` リファレンスはセッション中 1 回だけ本文注入し、以降のパターンではパスのみ表示（ref-inject テンプレから再生成、PR160） |
| 2.4.0 | 注入フックを `ref-inject` の仕組みへ移行（再生成は `/ref-inject:apply`）。`required` reference を再び **本文全量** で注入、`optional` は path + description。空マーカーファイルに代わり、パターン単位の **TTL トークン**（`{session_id}.yaml` マップ + `expires_at`、デフォルト 3600 秒、env `PY_KIT_INJECTION_TTL`）を導入。`PreCompact` フックなし（PR157） |
| 2.3.1 | 任意 companion の `session-kit`（プラグイン自体を削除）への言及を除去。注入トークンは常にセッション全体で生きる（once-per-pattern）。ドキュメント/コメントのみの修正でコード挙動の変更なし（PR155） |
| 2.3.0 | `core/comments.md`: マーカーだけでなく複数ステップ関数の中身にもコメント — 各ステップの意図 + 分岐ごとのラベルを、レイヤーに関係なく適用。「ログ出力のみの行はコメント不要」、サンプル例を追加（PR154） |
| 2.2.0 | 注入トークンをパターン単位に変更（旧: ファイル単位）。session-kit（任意）が UserPromptSubmit でターンごとにリセット。PR150 のマーカー/mtime 方式を撤回（PR151） |
| 2.1.2 | 注入トークンが session-kit のコンテキスト世代マーカーを参照 → /compact・/clear 後に再注入（PR150） |
| 2.1.1 | 注入フック: path+description のみを絶対パスで注入（本文なし）、Read マッチャーは維持（PR147） |
| 2.0.0 | 機能フォルダ型 + 関数ファースト + TypeScript 風へ全面刷新（PR138 で方針確定、PR140 で実装） |
| 1.0.0 | 純 DDD ベース（廃止） |

詳細は `changelogs/v{version}.md` を参照。

---

## 関連プラグイン

| プラグイン | 関係 |
|---|---|
| `next-kit` | Web 開発（Next.js App Router）の規約。py-kit から DB / Web 責務を切り出した |
| `claude-kit` | creator スキル群（skill-creator / rule-creator 等）と共通フック方針の元 |
| `dev-kit` | YAML 規約・dispatch フック等のベース |
