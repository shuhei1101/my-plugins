# `<PageHeader>` — ページタイトル + actions

各 Screen の冒頭で使うヘッダー。

---

## 実装

```tsx
// app/(shared)/components/PageHeader.tsx
type Props = {
  title: React.ReactNode
  description?: React.ReactNode
  actions?: React.ReactNode
}

export const PageHeader = ({ title, description, actions }: Props) => (
  <div className="flex items-start justify-between mb-6">
    <div>
      <h1 className="text-2xl font-bold">{title}</h1>
      {description && <p className="text-muted-foreground mt-1">{description}</p>}
    </div>
    {actions && <div className="flex items-center gap-2">{actions}</div>}
  </div>
)
```

---

## 使い方

```tsx
<PageHeader title="リソース一覧" />

<PageHeader
  title="リソース一覧"
  description="登録済みのリソースを管理します"
  actions={<Button asChild><Link href={RESOURCE_URL.new}>新規作成</Link></Button>}
/>

<PageHeader
  title={resource.name}
  actions={resource.canEdit && (
    <Button asChild><Link href={RESOURCE_URL.edit(resource.id)}>編集</Link></Button>
  )}
/>
```

---

## ルール

- title は **`<h1>`** （a11y / SEO）
- actions 領域はボタン群
- 1 Screen に 1 つ
- title / description はサーバーが返した値を直接渡す（i18n 不要前提）

## 関連 references

- `frontend/components-catalog.md`
- `frontend/screen-wrapper.md`

## 禁止

- 1 画面に複数 `<PageHeader>`
- title を `<h2>` 以下にする
- ハードコードした URL を actions に直書き（`URL` 定数経由）
