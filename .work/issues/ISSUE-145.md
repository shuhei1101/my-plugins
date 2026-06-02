# ISSUE-145: example/はじめに.md のパス参照が古い（.ref-inject/ サブフォルダ構造を反映していない）

**作成日**: 2026-06-02

## 問題

`plugins/ref-inject/templates/references/example/はじめに.md` に、実際のファイル配置と異なる古いパスが記載されている。

```markdown
- `references/index.yaml` (+ `index.jp.yaml`) — the path + description
- `references/injection_rules.yaml` — the edit-path patterns that should trigger it
```

実際のファイルは以下のパスに配置されている：
- `references/.ref-inject/_index.yaml`（+ `_index.jp.yaml`）— `_` プレフィックスあり・`.ref-inject/` サブフォルダ内
- `references/.ref-inject/_injection_rules.yaml`

このテンプレートから生成されるファイルを読んだユーザーや Claude が間違ったパスで登録操作をしようとし、ファイルが見つからないという混乱が起きる可能性がある。

## 対応方針

`はじめに.md` 内のパス参照を実際のファイル構造に合わせて更新する。

```markdown
- `references/.ref-inject/_index.yaml` (+ `_index.jp.yaml`) — the path + description
- `references/.ref-inject/_injection_rules.yaml` — the edit-path patterns that should trigger it
```

## 対象ファイル

- `plugins/ref-inject/templates/references/example/はじめに.md`: パス参照箇所を修正

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
