# async コピーハンドラが失敗時でも stop() を呼んでいた

## 何が起きたか

`uidev.js` の `copyAndStop()` 関数が、クリップボードコピー失敗時でも `stop()` を呼んでいた。
`stop()` は選択状態（`currentSelected`）をクリアするため、コピー失敗後に選択状態が失われ、ユーザーはリトライできなかった。

```js
// 問題のあったコード
async function copyAndStop() {
  const n = currentSelected.size;
  if (n > 0) {
    const ok = await copyJSON(buildPayload(Array.from(currentSelected)), topCopyBtn);
    if (ok) showToast(`✓ ${n} 件コピー`);
  }
  stop(); // ← 失敗時でも呼ばれる
}
```

## 原因

「コピーしてモードを終了する」という2つの処理を1つの関数に詰め込み、失敗時の分岐を考慮していなかった。

## 修正

コピー失敗時は早期リターンして `stop()` を呼ばないようにする。

```js
async function copyAndStop(feedbackBtn) {
  const n = currentSelected.size;
  if (n > 0) {
    const ok = await copyJSON(buildPayload(Array.from(currentSelected)), feedbackBtn);
    if (!ok) return; // ← 失敗時はピッカーを維持
    showToast(`✓ ${n} 件コピー`);
  }
  stop();
}
```

## 教訓

非同期処理を伴うハンドラでは、**成功・失敗の分岐を明示的に設計する**。  
「後処理（cleanup）」は成功時のみ呼ぶべきか、常に呼ぶべきかを意識すること。
