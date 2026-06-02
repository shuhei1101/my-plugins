---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-129: セットアップウィザード.md の内部クロスリファレンス名称が不正確

**作成日**: 2026-05-31

## 問題
`references/plugin/セットアップウィザード.md` に以下の 2 つの不正確な記述がある。

**1. 行32: `config` スキルの名称が不統一**

```
`setup-wizard` delegates env configuration to **its own plugin's `config` skill**.
```

同ファイルの他の箇所（行107, 109, 132, 163, 180）では一貫して `plugin-config` と呼んでいるが、この 1 箇所のみ `config` と省略されている。

**2. 行133: 内部クロスリファレンス先のセクション名が不正確**

```
| `plugin-migrate` | Version sync. See the "Required skills" section in this reference |
```

`セットアップウィザード.md` 内に「Required skills」というセクションは存在しない。実際には行126に「Related required skills」というセクションがある。また `plugin-migrate` の詳細は `プラグイン構造.md` の「Required skills」セクションに記述されており、参照先が曖昧になっている。

## 修正案

1. 行32の `config skill` を `plugin-config skill` に修正する。
2. 行133の `See the "Required skills" section in this reference` を `See the "Related required skills" section below` に修正し、必要に応じて `プラグイン構造.md` へのリンクも追加する。

JP ミラー（`セットアップウィザード.jp.md`）も合わせて確認・修正する。
