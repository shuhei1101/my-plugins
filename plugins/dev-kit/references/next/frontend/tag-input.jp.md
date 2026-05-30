<!-- This file is a Japanese mirror of tag-input.md. When updating the English original, update this file too. -->
# `<TagInput>` — IME 対応タグ入力

Enter でタグ確定、削除、IME 入力中の Enter を無視する共通コンポーネント。

---

## 実装

```tsx
'use client'

import { useState } from "react"
import { Input } from "./ui/input"
import { Badge } from "./ui/badge"
import { X } from "lucide-react"

type Props = {
  value: string[]
  onChange: (next: string[]) => void
  placeholder?: string
}

/** タグ入力 — Enter で追加、× で削除、IME 入力中の Enter は無視 */
export const TagInput = ({ value, onChange, placeholder }: Props) => {
  const [draft, setDraft] = useState("")
  const [composing, setComposing] = useState(false)

  const commit = () => {
    const v = draft.trim()
    if (!v) { setDraft(""); return }
    if (value.includes(v)) { setDraft(""); return }     // 重複防止
    onChange([...value, v])
    setDraft("")
  }

  return (
    <div className="flex flex-wrap gap-1 p-2 border rounded-md">
      {value.map((tag) => (
        <Badge key={tag} variant="secondary" className="gap-1">
          {tag}
          <button type="button" onClick={() => onChange(value.filter((t) => t !== tag))}>
            <X className="h-3 w-3" />
          </button>
        </Badge>
      ))}
      <Input
        className="flex-1 border-0 shadow-none focus-visible:ring-0 h-6 p-0"
        value={draft}
        onChange={(e) => setDraft(e.currentTarget.value)}
        onCompositionStart={() => setComposing(true)}
        onCompositionEnd={() => setComposing(false)}
        onBlur={commit}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !composing) {
            e.preventDefault()
            commit()
          }
        }}
        placeholder={placeholder ?? "タグを追加..."}
      />
    </div>
  )
}
```

---

## shadcn `<Form>` での使い方

```tsx
<FormField control={form.control} name="tags" render={({ field }) => (
  <FormItem>
    <FormLabel>タグ</FormLabel>
    <FormControl>
      <TagInput value={field.value} onChange={field.onChange} placeholder="タグを追加..." />
    </FormControl>
    <FormDescription>最大 10 件</FormDescription>
    <FormMessage />
  </FormItem>
)} />
```

---

## ルール

- IME 入力中（`composing === true`）の Enter は **無視必須**（日本語変換確定との衝突防止）
- 重複タグは追加しない
- 空文字は追加しない（trim 後）
- onBlur でも commit（フォーカスアウト時に確定）
- × でタグ削除

## 関連 references

- `frontend/components-catalog.md`
- `frontend/form-component.md` — `<FormField>` 内での利用例
- shadcn `<Badge>` `<Input>`

## 禁止

- IME 制御を画面ごとに手書きする
- 重複チェックなし
- onBlur で commit しない（モバイルでフォーカスアウトで失われる）
