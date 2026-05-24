# Stop フックの reason が会話セッションを汚染する

## 何が起きたか

Stop フックの `stop.py` スクリプトが `stop.md` の全文を読み込み、`reason` フィールドに埋め込んでいた。Claude がレスポンスを終えるたびに、この複数行の指示ブロックが会話セッションに注入されユーザーに表示されていた。見づらく、邪魔で、鬱陶しかった。

## 根本原因

フックの出力パターンが `{"decision":"block","reason":"<ファイル全文>"}` だった。`reason` テキストは Stop イベントのたびに会話セッションへ直接注入されてユーザーに見える。

## 修正方法

`reason` を1行のファイル参照に変更する: `"Read and follow: /path/to/stop.md"`。Claude が実際の指示をそのファイルから自分で読む方式にする。これにより `reason` を1行に保ちつつ、指示の全文を届けられる。

**修正前:**
```python
response = {"decision": "block", "reason": prompt_path.read_text("utf-8")}
```

**修正後:**
```python
reason = f"Read and follow: {prompt_path}"
response = {"decision": "block", "reason": reason}
```

また、専用の `stop.py` スクリプト自体も削除し、`hooks.json` のインライン python に一本化した。

## ルール

- **Stop フックの `reason` は必ず1行** — ファイル参照パターンを使うこと
- 指示の全文はプロンプトファイルに記述し、スクリプトはファイルパス参照のみを出力する
- このパターンは `hook-creator/SKILL.md` のステップ4 Notes に記載されている
