# Stop フック複数同時発火によるレースコンディション

## 概要

複数の Stop フックが同時発火する場合、`"Read and follow: /path"` 方式（間接参照）の指示が `stop_hook_active` ガードによって無効化される。

## 発生条件

- 2つ以上の Stop フックが同時に `{"decision":"block","reason":"..."}` を返す
- うち1つが直接指示文（例: notify-aituber）、もう1つが `"Read and follow: /path"` の間接参照

## 発生シーケンス

```
1. Claude が停止 → stop_hook_active=false で全フックが発火
   - フックA (notify-aituber): reason="Invoke the /notify-aituber skill now: ..."  ← 直接指示
   - フックB (work-kit):       reason="Read and follow: /path/stop.md"             ← 間接参照

2. Claude が両方の reason を受け取る
3. Claude がフックAの直接指示を実行（notify-aituber を呼ぶ）
4. Claude が再度 Stop

5. Stop フックが再発火 → stop_hook_active=true
   - フックA: stop_hook_active=true → sys.exit(0)
   - フックB: stop_hook_active=true → sys.exit(0)

6. ブロックなし → Claude が正常に停止
   ※ フックBの stop.md 指示が一度も実行されなかった
```

## 原因

`stop_hook_active` フラグはセッション全体に適用される。一度でも Stop がブロックされた後に Claude が再停止すると、すべてのフックが `stop_hook_active=true` でスキップされる。Claude が複数の reason を受け取っても一度に処理しきれない場合、処理されなかった間接参照は二度と実行されない。

## 修正

`"Read and follow: /path"` 方式を廃止し、ファイル内容を reason/stdout に直接埋め込む方式に戻す（PR89 以前の方式）。

```python
# Before（間接参照 — 複数フック競合時に失敗）
reason = "Read and follow: " + str(path)

# After（直接埋め込み — 確実に実行される）
reason = path.read_text('utf-8')
```

## 教訓

複数の Stop フックが共存する環境では、間接参照（Claude にファイルを読ませる方式）は信頼できない。直接指示を reason に埋め込む方が確実。
