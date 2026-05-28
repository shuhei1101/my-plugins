<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# ref-inject プラグイン開発ガイド

`ref-inject` は**ジェネレータ**プラグイン。`py-kit` / `next-kit` で使われている
リファレンス自動注入プラグイン（`*-kit` 形式）を新規生成する。生成物は、編集対象パスを
`injection_rules.yaml` と照合して関連リファレンスを注入する `PreToolUse` フックを持つ。

共通ランタイムの共有はしない（そのやり方は却下済み —
`premature-cross-plugin-centralization` 参照）。代わりに `templates/` から**独立コピー**を
吐き出し、インシデントログが「コピペの方が安い」と認めたやり方を自動化する。

---

## 構成

```
ref-inject/
├── .claude-plugin/plugin.json
├── CLAUDE.md / CLAUDE.jp.md
├── skills/create/SKILL.md (+ .jp.md)   # /ref-inject:create — 入力収集 → ジェネレータ実行
├── scripts/generate.py                  # テンプレコピー + プレースホルダ置換 + marketplace 登録
└── templates/                           # 新プラグインに展開される雛形
    ├── plugin.json                       # → {new}/.claude-plugin/plugin.json
    ├── CLAUDE.md (+ .jp.md)              # → {new}/CLAUDE.md
    ├── hooks/
    │   ├── inject_references.py          # PreToolUse: パス照合 → リファレンス注入
    │   ├── refresh_on_compact.py         # PreCompact: セッショントークン削除 → /compact 後に再注入
    │   ├── hooks.json
    │   └── templates/injection.md.j2 (+ .jp.md.j2)
    └── references/
        ├── index.yaml (+ index.jp.yaml)
        ├── injection_rules.yaml
        ├── CLAUDE.md (+ CLAUDE.jp.md)
        └── example/getting-started.md
```

---

## プレースホルダ

`scripts/generate.py` が全テキストテンプレートで置換する:

| プレースホルダ | 置換内容 | 例 |
|---|---|---|
| `__PLUGIN_NAME__` | プラグイン名（kebab） | `vue-kit` |
| `__ENV_PREFIX__` | 名前を大文字化、英数以外を `_` | `VUE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `vue-kit-references-injection` |
| `__DEFAULT_TTL__` | デフォルト TTL 秒 | `3600` |
| `__PLUGIN_DESCRIPTION__` | 1行説明 | … |

---

## 注入設計（生成フックに組み込み済み）

- `required` は**本文全量**注入 / `optional` は**パス + description のみ**
- トークン: `~/.claude/tokens/{plugin}/{session_id}.yaml`。pattern をキーにした YAML マップで各エントリに `injected_at`（epoch）。`now - injected_at >= TTL` で再注入。拡張可能（後でフィールド追加可）。
- TTL: デフォルト `3600` 秒、`settings.json` の `env` → `{PREFIX}_INJECTION_TTL` で上書き
- クリーンアップ: 発火のたびに全 `{session_id}.yaml` を走査し期限切れエントリを削除、空ファイルは削除
- `/compact`: `refresh_on_compact.py` がセッショントークンを削除し再注入させる
- 言語: `{PREFIX}_INJECTION_LANG=jp` で description/テンプレートを日本語に切替

これは旧方式（パターン単位の空ファイルトークン PR150/151、ポインタのみ注入 PR147）を
置き換える。TTL トークンが再注入を throttle するため `required` の本文注入を復活させた。

---

## 使い方

`/ref-inject:create`（または「リファレンス注入プラグインを作って」）。その後 `references/` を
実際の doc で埋め、`injection_rules.yaml` で紐付ける。

全生成プラグインの**仕組み**を変えるときは、ここの `templates/` を編集して各 consumer を
`/ref-inject:create --force` で再生成する（references 雛形を上書きするため、references を
再生成できるプラグインに限るか、hooks/ を手動コピーする）。

---

## 関連プラグイン

| プラグイン | 関係 |
|---|---|
| `py-kit` / `next-kit` | リファレンス注入の consumer。ref-inject 生成形式へ移行予定 |
| `claude-kit` | `plugin-creator` / creator スキルと共通フックポリシーの出所 |
