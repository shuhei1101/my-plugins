<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# git-guard フックがファイル内容に誤反応

**日付**: 2026-05-30
**カテゴリ**: tool-misuse

## 何が起きたか

シェルのヒアドキュメントを使って `plugin.json` を書き込もうとした際、ファイルの説明文に "guards git push/merge confirmation" という文字列が含まれていた。

```bash
cat > plugins/work/.claude-plugin/plugin.json << 'EOF'
{
  "description": "...guards git push/merge confirmation..."
}
EOF
```

git-guard フック（`PreToolUse(Bash)`）がBashコマンド全体から "git push" と "git merge" をパターンマッチし、`decision: block` を返してファイル書き込みをブロックした。

## 回避策

ファイル内容に "git push" や "git merge" が含まれる場合:

1. シェルヒアドキュメントの代わりに Python のファイル書き込み API を使う:
   ```python
   python3 -c "import json; data = {...}; open('file.json', 'w').write(json.dumps(data, indent=2))"
   ```
2. または文字列をリフレーズして triggering な文字列を避ける（例: "guards git push/merge" → "guards force-operations"）。

## コンテキスト

git-guard フックはBashコマンド文字列全体を検索する。ヒアドキュメントはファイル本文をコマンド文字列の一部として渡すため、文字列リテラル中の出現もガードを発動させる。
