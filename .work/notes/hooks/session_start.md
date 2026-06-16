# session_start — work プラグイン規約の SessionStart 注入 (Jinja2)

## 概要

セッション開始時に「やってはいけないこと」一覧を `additionalContext` として注入する
SessionStart フック。テンプレートは `session_start.j2` (Jinja2)。env で各ガードを
ON/OFF している場合、対応する箇条書きは `{% if %}` で出し分けられる。

## 構成

| No | ファイル | 役割 |
|---|---|---|
| 1 | `session_start.py` | 起動エントリ。env を読んで context を構築し `.j2` を render |
| 2 | `session_start.j2` | 表示テンプレート。`{% if %}` で env による出し分けを行う |
| 3 | `hooks.json` の `SessionStart` 登録 | `session_start.py` に `session_start.j2` の絶対パスを渡す |

jinja2 がインストールされていない環境ではフォールバックして生のテンプレ文字列を
そのまま注入する (stderr に warning)。

## 出し分けマトリクス

| env | デフォルト | 影響する表示 |
|---|---|---|
| `WORK_PROTECTED_BRANCHES` | `master,main,develop` | 保護ブランチ名 (例: `master` / `main` / `develop`) のプレースホルダ |
| `WORK_ALLOW_MASTER_COMMIT` | `false` | true 時、保護ブランチ系の禁止 3 行と「cwd ずれ補足」を非表示 |
| `WORK_GUARD` | `true` | false 時、`git push` / `git merge` 確認と `pre-merge-check` 2 行を非表示 |
| `WORK_BRANCH_ENFORCEMENT` | `true` | false 時、`/work:start` 実行を促す文言を代替文言に差し替え |

env の値解釈は `_is_true()` ヘルパで統一: `false` / `0` / `no` / `off` を false に、
それ以外を true に。デフォルトは env 未設定時のフォールバック。

## 環境変数オーバーライド表示

テンプレ末尾に「環境変数オーバーライド (現在のセッション)」表を出す。
ユーザーが明示的に export した env のみを並べる (デフォルトと同じ値で並べない)。

## 参考リンク

- `plugins/work/hooks/session_start.py`: render エントリ
- `plugins/work/hooks/session_start.j2`: Jinja2 テンプレ本体
- `plugins/work/hooks/inject_rules.py`: 同じ Jinja2 セットアップを参照 (`inject_message.j2` のレンダリングと共通)
