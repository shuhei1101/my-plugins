<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 引用なし YAML スカラー内のコロン+スペースでパースが壊れる

**日付**: 2026-05-29
**分類**: wrong-assumption

## 何が起きたか

PR159 で claude-kit の `references/index.yaml` を書く際、reference の description を引用なしスカラーで
書き、その中にコロン+スペースを含めてしまった:

```yaml
references:
  - path: rules.md
    description: ルールの作り方。… ユースケース指向の paths: 設計、統合/…
```

引用なし `description` 値の中の `paths: `（コロン + スペース）を YAML は**ネストしたマッピングキー**の
開始と解釈し、リテラル文字列として扱わない。結果 `yaml.safe_load` が
`mapping values are not allowed here` で失敗した。`inject_references.py` は `index.yaml` を
`yaml.safe_load` でパースするため、index が壊れるとそのプラグインの注入が黙って無効になる。

同じ危険は `injection_rules.yaml` や自由記述値を持つ他の YAML ファイルにも存在する。

## どう回避するか

- YAML の自由記述値（description / summary 等）を書くとき、**引用なしスカラーに `単語: `（コロン +
  スペース）を入れない**。コロン+スペースを避けて言い換える（`paths: 設計` → `paths 設計`）か、値全体を
  引用で囲む（`description: "… paths: 設計 …"`）。
- `index.yaml` / `index.jp.yaml` / `injection_rules.yaml` を編集したら検証する:
  `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>`。あわせて
  index ↔ injection_rules ↔ ファイルシステムの orphan チェックを実行する。
- 補足: トレーリングスペースの**ない**コロン（例 `a:b`）では発生しない。YAML がプレーンスカラーで特別扱い
  するのは `: `（コロン+スペース）と ` #` である。

## コンテキスト

- 影響範囲: `plugins/*-kit/references/index.yaml`（+ `index.jp.yaml`）、`injection_rules.yaml`、
  および `inject_references.py` が消費する YAML。
- PR159（claude-kit → ref-inject 移行）で、orphan チェックスクリプトが `index.yaml` のパースに
  すら失敗したことで発覚。
