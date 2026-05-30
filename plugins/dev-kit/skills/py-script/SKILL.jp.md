<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->
# SKILL.jp.md — dev-kit:py-script（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: dev-kit:py-script
**トリガー**: 単一ファイルまたは数ファイル程度の簡易 Python スクリプト作成依頼時。
「スクリプト作って」「ちょっとした Python ファイル書いて」「自動化スクリプトほしい」など。
`pyproject.toml` や `tests/` を必要とする本格プロジェクトには使わない → `dev-kit:py-project` を使う。

---

# dev-kit:py-script — 簡易 Python スクリプト作成

dev-kit Python 規約に従った単一ファイル / 数ファイルのスクリプトを作成する。

---

## 作業内容

### ステップ1: 規約を読み込む

まず references のインデックスを読む:

```
{plugin_root}/references/python/index.yaml
```

スキルファイルの 2 階層上がプラグインルート（例: `Base directory: .../skills/py-script` → プラグインルートは `.../dev-kit/`）。

このスキルで読むべきもの:
- `{plugin_root}/references/python/core/naming.md` — 命名規約
- `{plugin_root}/references/python/core/comments.md` — docstring とフィールド説明
- `{plugin_root}/references/python/core/type-hints.md` — PEP 695 / 型注釈
- `{plugin_root}/references/python/core/language-rules.md` — 日本語コメント / 英語ログ
- `{plugin_root}/references/python/core/style.md` — ruff / 行長
- `{plugin_root}/references/python/scripts/python-script.md` — スクリプト構造

bat ランチャーも作るなら:
- `{plugin_root}/references/python/scripts/launchers-windows.md`

UNIX ランチャーなら:
- `{plugin_root}/references/python/scripts/launchers-unix.md`

tkinter GUI なら:
- `{plugin_root}/references/python/scripts/tkinter.md`

→ ステップ2へ

---

### ステップ2: 要件を確認する

#### 処理内容

1. スクリプトの目的が不明な場合は確認する
2. 必要なサードパーティパッケージを特定する
3. 出力先とファイル名を確認する
4. GUI（tkinter）が必要かどうか確認する
5. ランチャー（bat / sh）が必要かどうか確認する

→ ステップ3へ

---

### ステップ3: スクリプトを書く

#### 処理内容

1. `scripts/python-script.md` の標準テンプレートに従ってファイルを作成:
   - モジュール docstring（1 行目で何をするか）
   - `from __future__ import annotations`
   - 標準ライブラリ → サードパーティ → 自モジュール の順で import
   - 定数（`UPPER_SNAKE_CASE`）
   - logger セットアップ
   - `_parse_args()` で argparse
   - 処理本体の関数（`process(...)` 等）
   - `main() -> int` でまとめる
   - `if __name__ == "__main__": sys.exit(main())`
2. 型ヒントを全箇所に付ける（PEP 695）
3. 必要なパッケージは `# pip install {package}` をファイル先頭のコメントで明示
4. `core/naming.md`（snake_case 関数、UpperCamel 型）と `core/comments.md`（exported 関数 docstring）に従う
5. `print()` ではなく `logger` を使う。ログメッセージは **英語**
6. 例外処理: 想定例外は捕まえる、未捕捉は `logger.exception` で traceback ごと残す
7. ランチャーが必要なら同時に作成（`scripts/launchers-windows.md` / `scripts/launchers-unix.md`）

→ 完了

#### 出力

- dev-kit Python 規約に従ったスクリプトファイル
- 必要なら bat / sh ランチャー

#### 補足

##### 禁止事項

- `pyproject.toml` を作らない（必要なら `dev-kit:py-project` で本格プロジェクト化）
- `logger.py` / `settings.py` / `errors.py` 等の `shared/` モジュールを作らない（インライン）
- `tests/` フォルダを作らない
- 1 回限りのスクリプトに不要な抽象化を加えない（YAGNI）
- 単体テストを書かない（dev-kit Python 全体の方針）

---

## 参考資料

詳細は `{plugin_root}/references/python/index.yaml` を参照。

主要 reference:
- `core/*` — 言語ルール
- `scripts/python-script.md` — スクリプトの骨格
- `scripts/launchers-*.md` — ランチャー
- `scripts/tkinter.md` — GUI 付ける場合
