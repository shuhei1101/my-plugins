<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# SKILL.jp.md — py-kit:py-script（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: py-kit:py-script
**トリガー**: 単一ファイルまたは数ファイル程度の簡易 Python スクリプト作成依頼時。
「スクリプト作って」「ちょっとした Python ファイル書いて」「自動化スクリプトほしい」など。
`pyproject.toml` や `tests/` を必要とする本格プロジェクトには使わない → `py-kit:py-project` を使う。

---

# py-kit:py-script — 簡易 Python スクリプト作成

py-kit 規約に従ったクリーンな単一ファイルスクリプトを作成する。

---

## 作業内容

### ステップ1: 規約を読み込む

まずインデックスファイルを読み込む：

```
{plugin_root}/references/CLAUDE.md
```

スキルファイルの2階層上がプラグインルート（例: `Base directory: .../skills/py-script` → プラグインルートは `.../{plugin-name}/`）。

続いて以下を読む：
- `{plugin_root}/references/python-core.md` — 命名規則・型ヒント・コメントルール・言語ルール
- `{plugin_root}/references/python-scripts.md` — 簡易スクリプト構造

→ ステップ2へ

---

### ステップ2: 要件を確認する

#### 処理内容

1. スクリプトの目的が不明な場合は確認する。
2. 必要なサードパーティパッケージを特定する。
3. 出力先とファイル名を確認する。

→ ステップ3へ

---

### ステップ3: スクリプトを書く

#### 処理内容

1. `python-scripts.md` の「簡易スクリプト構造」に従ってファイルを作成（ファイルヘッダー docstring → 標準ライブラリ → サードパーティ → 定数 → プライベート関数 → `main()` → `parse_args()` → `if __name__ == "__main__"`）。
2. 型ヒントを全箇所に付ける。
3. 必要なパッケージは `# pip install {package}` でインラインコメント。
4. `python-core.md` の命名規則・コメントルールを適用する。
5. `print()` / ログ出力は英語のみ。

→ 完了

#### 出力

- py-kit 規約に従ったスクリプトファイルが作成済み

#### 補足

##### 禁止事項

- `pyproject.toml`・`logger.py`・`config.py`・bat ファイル・setup スクリプト・`tests/` フォルダを作らない（それらはフルプロジェクト用）
- 一回限りのスクリプトに不要な抽象化を加えない

---

## 参考資料

- `{plugin_root}/references/python-core.md` — 命名規則・型ヒント・コメントルール・言語ルール
- `{plugin_root}/references/python-scripts.md` — 簡易スクリプト構造
