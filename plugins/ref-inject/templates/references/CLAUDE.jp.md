<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# __PLUGIN_NAME__ references

編集対象ファイルパスに応じて `__LOG_TAG__` フックが自動注入するリファレンス。

## 手動で読む場合

- `index.yaml` — 全リファレンス一覧（path + 1行 description、フックがパース）
- `injection_rules.yaml` — 編集パスのパターン → `required` / `optional` リファレンス

## 自動注入

`PreToolUse(Edit | Write | MultiEdit | Read)` で `hooks/inject_references.py` が:

1. 編集対象パスを `injection_rules.yaml` のパターンと照合
2. マッチした `required` を**本文全量**、`optional` を**パス + description のみ**で注入
3. `~/.claude/tokens/__PLUGIN_NAME__/{session_id}.yaml` のパターン単位 TTL トークンで重複注入を抑制
   （`__ENV_PREFIX___INJECTION_TTL` 秒、デフォルト __DEFAULT_TTL__ 秒で再注入）
4. `hooks/refresh_on_compact.py` が `PreCompact` でトークンを消し、`/compact` 後に再注入させる

`__ENV_PREFIX___INJECTION_LANG=jp` で日本語 description を注入（`index.jp.yaml` + `injection.jp.md.j2`）。

## メンテナンス

- リファレンス追加: ファイル作成 → `index.yaml`（+ `index.jp.yaml`）に追記 → `injection_rules.yaml` のパターンに紐付け
- 「1 リファレンス = 1 ユースケース」を保ち、1ファイル編集で無関係な doc を引き込まない
- `injection_rules.yaml` 編集後は orphan（index にあるがパターン未紐付け、または逆）が無いか確認
