<!-- This file is a Japanese mirror of logger-tags.md. When updating the English original, update this file too. -->
# Logger — Component tag 命名

`logger.create("tag")` の tag 命名規約。集約サービスでのフィルタリングを統一する。

---

## tag フォーマット: `{layer}:{name}`

| Layer | Format | Example |
|---|---|---|
| Page | `page:{feature}` | `page:resources` |
| Screen | `screen:{Name}` | `screen:ResourceEditScreen` |
| Hook | `hook:{hookName}` | `hook:useResourceForm` |
| API route | `api:{resource}.{method}` | `api:resources.POST`, `api:resources/[id].PATCH` |
| Service | `service:{resource}` | `service:resource` |
| Action | `action:{resource}` | `action:resources`, `action:auth` |
| Client (fetch wrapper) | `client:{resource}` | `client:resources` |
| Component | `component:{Name}` | `component:ResourceCard` |
| Error boundary | `error-boundary:{path}` | `error-boundary:resources` |
| Hook (cross-cutting) | `hook:shared:{name}` | `hook:shared:useConfirmDialog` |
| Webhook | `webhook:{provider}` | `webhook:stripe` |
| Cron | `cron:{job}` | `cron:daily-summary` |
| Auth | `auth` または `auth:{event}` | `auth:login`, `auth:signout` |
| Provider | `provider:{name}` | `provider:QueryProvider` |

---

## ルール

- **必ず `{layer}:{name}` 形式**
- レイヤー名は短く、固定値
- name は kebab-case or PascalCase（layer の慣習に合わせる）
- API は `{resource}.{method}` で HTTP メソッド付け
- 集約サービス（Datadog 等）で `component` キーでフィルタ可能に

## 使い方の例

```ts
// route.ts
const log = logger.create("api:resources.POST")
log.info("request received")

// hook
const log = logger.create("hook:useResourceForm")
log.debug("form initialized", { resourceId })

// action
const log = logger.create("action:resources")
log.info("registered", { id })
```

## 関連 references

- `shared/logger-impl.md` — ロガー実装

## 禁止

- tag を省略してデフォルトロガー乱用
- tag 命名がバラバラ（`{layer}:{name}` 形式厳守）
- 同じ component で異なる tag を使う
