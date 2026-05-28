<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# __PLUGIN_NAME__ プラグイン開発ガイド

__PLUGIN_DESCRIPTION__

`ref-inject` テンプレートから生成。`Edit` / `Write` / `MultiEdit` / `Read` のたびに編集対象パスを
`references/injection_rules.yaml` と照合し、関連リファレンスを注入するフックを同梱する。

---

## 構成

```
__PLUGIN_NAME__/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── inject_references.py     # PreToolUse: パスを照合してリファレンスを注入
│   ├── refresh_on_compact.py    # PreCompact: セッショントークンを消し /compact 後に再注入
│   ├── hooks.json
│   └── templates/injection.md.j2 (+ injection.jp.md.j2)
└── references/
    ├── index.yaml (+ index.jp.yaml)   # path + description（フックがパース）
    ├── injection_rules.yaml           # 編集パスパターン → required / optional
    ├── CLAUDE.md (+ CLAUDE.jp.md)
    └── ...                            # リファレンス本体
```

---

## 注入の挙動

- `required` は**本文全量**、`optional` は**パス + description のみ**を注入
- パターン単位 TTL トークン（`~/.claude/tokens/__PLUGIN_NAME__/{session_id}.yaml`）で、
  `__ENV_PREFIX___INJECTION_TTL` 秒（デフォルト __DEFAULT_TTL__）以内の同一パターン再注入を抑制
- `/compact` でトークンが消え、以降は再注入される
- `__ENV_PREFIX___INJECTION_LANG=jp` で description/テンプレートを日本語に切替

TTL は `settings.json` で設定:

```jsonc
{ "env": { "__ENV_PREFIX___INJECTION_TTL": "3600" } }
```

---

## メンテナンス

フック・テンプレート・トークンの**仕組み**は `ref-inject` が所有する。仕組みを変えるときは
`ref-inject` のテンプレートを編集して `/ref-inject:create` で再生成する。ここのファイルを直接
編集するのは**リファレンス**の追加・調整（`references/` の中身 + `index.yaml` + `injection_rules.yaml`）に限る。
