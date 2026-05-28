<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# next-kit references — インデックス

next-kit の規約は **1 ファイル = 1 ユースケース** の reference に分割されている。
編集対象に該当するものだけを読む。

管理は 2 種類のファイルに分かれる:

| File | 役割 |
|---|---|
| **`index.yaml`** (英語) / **`index.jp.yaml`** (日本語ミラー) | reference 一覧 + 1 行 `description`。フックは英語版を parse して注入する（日本語版は人間用ミラー）。 |
| **`injection_rules.yaml`** | 編集対象ファイルパスのパターン → 必須/任意 reference のマッピング（言語非依存）。 |

---

## 手動で読む

1. **`index.yaml`** で各 reference の内容を確認
2. 編集対象ファイルパスを **`injection_rules.yaml`** の `rules[].pattern` と照合
   - 例: `src/app/api/v1/resources/route.ts` を編集 → `**/*.{ts,tsx}` と `**/app/api/v1/**/route.ts` の両方にマッチ
3. マッチした rule の `required` を全部読み、必要に応じ `optional` も読む

---

## 自動で読む

`next-references-injection` フック（PreToolUse）が `Edit` / `Write` / `MultiEdit` / `Read` ごとに以下を実行する:

1. `injection_rules.yaml` を読み、マッチした rule を収集
2. 各 reference の description を `index.yaml` から取得
3. `required` reference の本文を全量読み込む（`optional` は path + description のみ）
4. Jinja2 テンプレ（`hooks/templates/injection.md.j2`）でレンダリング
5. `decision: block` の `reason` で注入

パターン単位の TTL トークン（`~/.claude/tokens/next-kit/{session_id}.yaml`）で、TTL 期間内（デフォルト 3600 秒、env `NEXT_KIT_INJECTION_TTL`）は同じパターンを再注入しない。

注入言語切替: `NEXT_KIT_INJECTION_LANG=jp` で日本語版（デフォルトは英語）。

---

## TypeScript 型チェックフック

`next-ts-check` フック（PostToolUse、`hooks/ts_check.py`）が `*.ts` / `*.tsx` ファイルへの `Edit` / `Write` / `MultiEdit` 後に自動実行される:

1. 編集ファイルのディレクトリから親方向に `tsconfig.json` を探索（モノレポ対応）
2. 見つかったディレクトリで `tsc --noEmit --incremental` を実行
3. 型エラーがあれば stdout に出力 → Claude がコンテキストとして受け取り修正できる
4. ブロックしない（`decision: block` は使用しない）— エラーは参考情報として扱う

ビルドキャッシュを無効にしたい場合は `tsc --noEmit`（`--incremental` なし）に変更する。

---

## SKILL から利用

| スキル | 役割 | 使うタイミング |
|---|---|---|
| `next-kit:implement` | 編集対象ファイルに対応する reference を読み込み、それに従って実装する | 特定のファイルを作成・編集するとき |
| `next-kit:plan` | ユーザーのリクエスト範囲に合わせた references を読み込み、実装計画書（ファイルツリー・各ファイルの役割・規約ポイント）を出力する | 実装を始める前に作成するファイルを計画するとき |

---

## メンテナンス

- 新規 reference 追加時は **`index.yaml`、`index.jp.yaml`、`injection_rules.yaml`** の 3 つを揃えて更新
- 削除・リネーム時も同様
- この `references/CLAUDE.md` は最小限に保つ — 個別 reference の description は `index.yaml` (と JP ミラー) にしか書かない

---

## キット間の同期

py-kit も同じ構造（`index.yaml` + `injection_rules.yaml` + `hooks/inject_references.py` + Jinja2 テンプレ）を採用している。
**片方を変えたらもう片方も変える** — `.claude/rules/feature/kit-hooks-index-sync.md` 参照。
