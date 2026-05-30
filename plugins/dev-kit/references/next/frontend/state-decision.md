# State の置き場所 — 決定フロー

「この状態をどこに持つべきか」を判断する。

---

## 決定フロー

```
データはサーバーから来る?
  ├─ Yes → Server Component で取得（SSR） + TanStack Query で再取得
  └─ No → 次へ

ユーザーが見ているものに反映? シェア / ブックマーク / リフレッシュで保持?
  ├─ Yes → URL クエリ string（nuqs or useSearchParams）
  └─ No → 次へ

複数のルート / コンポーネントで共有?
  ├─ Yes → Context（更新少） or Zustand（頻繁更新 / selector 必要）
  └─ No → 次へ

3+ レベルの prop drilling?
  ├─ Yes → 短く Context、または hook 抽出
  └─ No → useState
```

---

## 用途別 早見表

| 状態 | 置き場所 |
|---|---|
| 取得した記事一覧 | TanStack Query (initialData = Server Component) |
| 現在のフィルタ・ソート・ページ | URL クエリ |
| 現在のタブ | URL クエリ |
| Modal 開閉（リンク不要） | useState |
| Modal 開閉（deep link 可能にしたい） | URL クエリ |
| Sidebar 開閉（モバイル一時的） | useState |
| Sidebar 開閉（永続化） | Zustand or Context |
| 編集中のフォーム値 | react-hook-form |
| ダーク / ライト | next-themes（cookie + Context） |
| 未読通知数 | サーバー（TanStack Query）or Zustand |
| Toast | sonner（自前 state） |
| 確認ダイアログ | useConfirmDialog (Zustand) |

---

## 各ツールのリファレンス

| Tool | Reference |
|---|---|
| TanStack Query | `frontend/use-query-pattern.md`, `frontend/use-mutation-pattern.md`, `frontend/query-client-setup.md` |
| URL state | `frontend/use-url-state-pattern.md` |
| Context | `frontend/context-pattern.md` |
| Zustand | `frontend/zustand-pattern.md` |
| react-hook-form | `frontend/form-component.md`, `frontend/use-form-pattern.md` |
| next-themes | shadcn / next-themes 公式 |

---

## ルール

- **軽い tool から選び**、必要に応じてエスカレート
- サーバーデータを `useState` で持たない（→ TanStack Query）
- シェア可能 UI state を `useState` で持たない（→ URL）
- フォーム値を Context / URL / Zustand に入れない（→ react-hook-form）
- エラー state をローカルに持たない（→ `handleAppError` 経由 toast）

## 禁止

- サーバーデータをローカル state（`useState`）で抱える
- 共有 UI state を prop drilling だけで解決（3+ レベルで Context）
- フォーム値を URL / Zustand / Context に入れる
- 不必要に Zustand を使う（Context で済むなら Context）
