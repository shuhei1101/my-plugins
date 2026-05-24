<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# statusline-python-quote-nesting

## 何が起きたか

`apply-statusline.py` が生成する statusLine コマンド（`python -c "..."` 形式）の中に、`r5["resets_at"]` という辞書アクセスがダブルクォートで書かれていた。

シェルが `python -c "..."` の外側ダブルクォートを内側 `"resets_at"` のダブルクォートで切ってしまい、`resets_at` がベア単語（未定義変数）として Python に渡された。

結果として `rate_limits.resets_at` が存在する瞬間（トークン消費でレート情報が確定したとき）に `NameError: name 'resets_at' is not defined` でステータスラインが落ちる。

このバグは元々存在していたが、PR116 の緑色追加変更と同タイミングで顕在化したため、原因切り分けに長時間を費やした。

## なぜ起きたか

- 辞書アクセスを `r5["resets_at"]` と書く際、外側コマンド全体が `python -c "..."` のダブルクォートに包まれていることを意識していなかった
- シェルのクォート解釈ルール（ネストされたダブルクォートは外側を終端する）を考慮していなかった
- テスト時に rate_limits データを含めずにテストしていたため、resets_at の条件分岐が走らず、バグが発見できなかった

## 修正

`r5["resets_at"]` → `r5.get('resets_at')` に変更。シングルクォートで完結させ、外側ダブルクォートと衝突しないようにした。`r7` も同様。

```python
# Before (bug)
"...tt(r5[\"resets_at\"],'%H:%M')..."

# After (fix)
"...tt(r5.get('resets_at'),'%H:%M')..."
```

## 再発防止

`python -c "..."` 形式のインラインコマンドを JSON に格納する場合、内側のすべての文字列・キーアクセスはシングルクォートで統一すること。ダブルクォートが必要な場合は `\"` ではなく別の表記（`.get()` メソッドなど）で回避する。

テスト時は必ず本番想定の入力（rate_limits・context_window などすべてのフィールドを含む）でコマンドを実行すること。
