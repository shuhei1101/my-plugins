<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# work リファレンス

このフォルダには、work プラグインの `inject_references.py` フックが対象ファイル編集時に
自動注入するリファレンスドキュメントが含まれている。

## 手動で読む

リファレンスを読むには、`Read` ツールに絶対パスを指定する:

```
Read: plugins/work/references/{filename}.md
```

## 自動で読まれる仕組み

`PreToolUse` 注入フックが `Edit / Write / MultiEdit / Read` で発火し、編集ファイルのパスを
`references/_injection_rules.yaml` の glob パターンと照合する。マッチした `required` リファレンスは
本文全量を、`optional` はパスと説明のみを注入する。

注入は `~/.claude/tokens/work/{session_id}.yaml` の TTL トークンでセッション内重複排除される。
TTL 経過後に再注入される（デフォルト 3600 秒、`WORK_INJECTION_TTL` で変更可）。

## リファレンス一覧

説明付き一覧は `_index.yaml` を参照。

## メンテナンス

- **リファレンス追加**: `_index.yaml`（と `_index.jp.yaml`）にエントリを追加し、`_injection_rules.yaml` にパターンを追加する
- **リファレンス削除**: `_index.yaml`、`_index.jp.yaml`、`_injection_rules.yaml` から削除する
- **リファレンス更新**: `.md` とその `.jp.md` ミラーを同じコミットで更新する
