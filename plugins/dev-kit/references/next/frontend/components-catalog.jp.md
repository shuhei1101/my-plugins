<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# app/(shared)/components/ — 共通コンポーネントカタログ

新規コンポーネントを作る前に **必ずこの表をチェック**。

---

## 自前ラッパー（`app/(shared)/components/` 直下）

| Component | 詳細 reference |
|---|---|
| `ScreenWrapper` | `frontend/screen-wrapper.md` |
| `PageHeader` | `frontend/page-header.md` |
| `LoadingButton` | `frontend/loading-button.md` |
| `EmptyState` | `frontend/empty-state.md` |
| `RequiredMark` | `frontend/required-mark.md` |
| `TagInput` | `frontend/tag-input.md` |
| `AutosaveIndicator` | `frontend/autosave-indicator.md` |
| `Pagination` | shadcn `<Pagination>` ラッパー |
| `NavigationLink` | `<Link>` + `<Button>` 組み合わせ |
| `ConfirmDialog` provider | `frontend/confirm-dialog.md` |

---

## shadcn/ui primitive（`app/(shared)/components/ui/`）

`pnpm dlx shadcn@latest add {name}` で追加。

```
button, input, textarea, label, select, checkbox, switch, radio-group, slider,
form, card, sheet, dialog, alert-dialog, popover, tooltip, hover-card, dropdown-menu,
tabs, accordion, avatar, badge, separator, skeleton, alert,
table, pagination, calendar, command, scroll-area, toggle, toggle-group,
sonner, breadcrumb, collapsible, drawer, navigation-menu, progress, resizable
```

必要なものを随時追加。詳細は shadcn 公式ドキュメント。

---

## 用途別早見表

### ボタン

| 用途 | コンポーネント |
|---|---|
| 通常のクリック | shadcn `<Button>` |
| 非同期処理（mutation 等） | `<LoadingButton>` |
| リンク遷移 | `<Button asChild><Link>...</Link></Button>` |
| アイコンのみ | `<Button size="icon">` |
| 破壊的 | `<Button variant="destructive">` |

### レイアウト

| 用途 | コンポーネント |
|---|---|
| Screen の外殻 | `<ScreenWrapper>`（必須） |
| ページタイトル + actions | `<PageHeader>` |
| 縦並び | `<div className="flex flex-col gap-4">` |
| 横並び | `<div className="flex items-center gap-2">` |
| カード | shadcn `<Card>` |
| タブ | shadcn `<Tabs>` |

### フォーム入力

| 用途 | コンポーネント |
|---|---|
| ラベル + エラー込み | shadcn `<FormField>` + `<FormItem>` + `<FormControl>` + `<FormLabel>` + `<FormMessage>` |
| Text | shadcn `<Input>` |
| Number | shadcn `<Input type="number">` |
| Date | shadcn `<Calendar>` + `<Popover>` |
| Select | shadcn `<Select>` |
| Multi-select | shadcn `<Command>` + `<Popover>` |
| Multi-line | shadcn `<Textarea>` |
| Tag | `<TagInput>` |
| Toggle | shadcn `<Switch>` |
| 必須マーク | `<RequiredMark />` |

### フィードバック

| 用途 | コンポーネント |
|---|---|
| Loading skeleton | shadcn `<Skeleton>` または `loading.tsx` |
| Toast | `toast.success` / `toast.error` (sonner) |
| Inline alert | shadcn `<Alert>` |
| 確認 dialog | `useConfirmDialog()` 経由 |
| Empty state | `<EmptyState>` |
| Autosave 状態 | `<AutosaveIndicator>` |

### ダイアログ系

| 用途 | コンポーネント | 詳細 |
|---|---|---|
| コンテンツ dialog | shadcn `<Dialog>` | `frontend/patterns/dialog.md` |
| 確認 dialog | `useConfirmDialog()` | `frontend/confirm-dialog.md` |
| サイドパネル | shadcn `<Sheet>` | `frontend/patterns/dialog.md` |
| モバイル下シート | shadcn `<Drawer>` | `frontend/patterns/dialog.md` |
| Popover | shadcn `<Popover>` | `frontend/patterns/dialog.md` |

---

## App shell（layout 用、`app/(authenticated)/` 系）

| Component | 役割 |
|---|---|
| `AppShell` | サイド/ボトムナビ切替 |
| `SideNav` | PC サイドナビ |
| `MobileNav` | モバイル下ナビ |
| `AppHeader` | トップバー |
| `ThemeToggle` | ダーク/ライト |

これらは layout レベル PR でしか触らない。

---

## 新規コンポーネントを作る前

1. **本カタログをチェック** — 該当 role のものがあるか
2. **shadcn primitive をチェック** — `shadcn add` で取れるか
3. **Radix UI を直接使う** — shadcn になくても Radix にあれば
4. **作る** — 上記がなければ `app/(shared)/components/` に追加し、本カタログを更新

「3 回目に同じものを書きそうになったら抽出」が目安。

---

## ルール

- フィーチャ固有のコンポーネントは `{feature}/components/`（カタログ対象外）
- 共通は `app/(shared)/components/` 直下
- shadcn copy は `app/(shared)/components/ui/` 直下
- アンダースコア prefix 禁止（PR135 で `_components/` 廃止）
- 全 Screen で `<ScreenWrapper>` 必須

## 関連 references

各コンポーネントの個別 reference（上記表の「詳細 reference」列）。
