# removeEventListener に匿名関数を渡しても解除できない

## 何が起きたか

`uidev.js` の `stop()` 関数で `topCopyBtn.removeEventListener("click", copyAndStop)` を呼んでいたが、`copyAndStop` が `startPicker()` 内の閉包（クロージャ）で、`addEventListener` 時と `removeEventListener` 時で**同じ関数参照**を使っているように見えても、アロー関数やインライン関数を直接渡すと参照が一致せず解除に失敗するケースがある。

今回は `copyAndStop` 自体は名前付き関数として同スコープに定義されていたため直接の問題にはならなかったが、より安全な設計として修正した。

## 修正

イベントリスナーとして登録・解除する関数は、必ず**名前付き関数**として定義して渡す。

```js
// 問題になりやすいパターン
topCopyBtn.addEventListener("click", () => copyAndStop(topCopyBtn)); // 匿名アロー関数 → 解除不可
topCopyBtn.removeEventListener("click", () => copyAndStop(topCopyBtn)); // 別の参照になる

// 正しいパターン
function onTopCopyClick() { copyAndStop(topCopyBtn); }
topCopyBtn.addEventListener("click", onTopCopyClick);
topCopyBtn.removeEventListener("click", onTopCopyClick); // 同じ参照 → 解除できる
```

## 教訓

`removeEventListener` を後で呼ぶ予定があるなら、リスナーは必ず名前付き関数で定義・保持する。アロー関数をインラインで渡すと `remove` できない。
