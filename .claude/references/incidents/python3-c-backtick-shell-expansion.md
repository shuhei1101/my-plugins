<!-- This file is a Japanese mirror of python3-c-backtick-shell-expansion.md. When updating the English original, update this file too. -->
# python3 -c でバッククォートがシェル展開される

**日付**: 2026-05-30
**カテゴリ**: command-error

## 何が起きたか

バッククォートで囲まれた文字列（Markdownのコードスパン: `` `plugins/work/` `` など）を含む Python コードを `python3 -c "..."` に渡したとき、Bash がバッククォートをコマンド置換として扱い、展開してしまった。

```bash
python3 -c "
content = '''
| `plugins/work/` | 編集 | ...
'''
"
```

バッククォート内がコマンドとして実行され（空文字列に展開され）、テーブルのセルが空白になってしまった。

## 回避策

シングルクォートのヒアドキュメント区切り文字（`PYEOF`）を使い、Bash がヒアドキュメント本体を展開しないようにする:

```bash
python3 << 'PYEOF'
content = """
| `plugins/work/` | 編集 | ...
"""
PYEOF
```

`<< 'PYEOF'`（シングルクォート）にすると、Bash はブロック全体をリテラル文字列として扱い、変数展開・コマンド置換・バックスラッシュ処理を一切行わない。

## コンテキスト

Python コードに Markdown のコードスパン（バッククォート）が含まれる場合に発生する。`python3 -c "..."` 形式では Bash 文字列パース中にバッククォートがコマンド置換として解釈される。クォートされたヒアドキュメントを使えばこの問題を完全に回避できる。
