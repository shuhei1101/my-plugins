# ISSUE-129: セットアップウィザード.md の内部クロスリファレンス名称が不正確

**作成日**: 2026-05-31

## 概要

`references/plugin/セットアップウィザード.md` に、スキル名の不統一（`config` 対 `plugin-config`）と、存在しないセクション名へのクロスリファレンスという 2 つの不正確な記述がある。

## 背景

ファイル内の他の箇所では一貫した名称・セクション名が使われており、当該箇所のみ整合していない。

## 現状

**1. 行 32: `config` スキルの名称が不統一**

```
`setup-wizard` delegates env configuration to **its own plugin's `config` skill**.
```

同ファイルの他の箇所（行 107, 109, 132, 163, 180）では一貫して `plugin-config` と呼んでいるが、この 1 箇所のみ `config` と省略されている。

**2. 行 133: 内部クロスリファレンス先のセクション名が不正確**

```
| `plugin-migrate` | Version sync. See the "Required skills" section in this reference |
```

`セットアップウィザード.md` 内に「Required skills」というセクションは存在しない。実際には行 126 に「Related required skills」というセクションがある。また `plugin-migrate` の詳細は `プラグイン構造.md` の「Required skills」セクションに記述されており、参照先が曖昧になっている。

## 期待される状態

スキル名が `plugin-config` に統一され、クロスリファレンスが実在するセクション（または正しいファイル）を正確に指している。JP ミラーも合わせて修正されている。

## 対応案

1. 行 32 の `config skill` を `plugin-config skill` に修正する。
2. 行 133 の `See the "Required skills" section in this reference` を `See the "Related required skills" section below` に修正し、必要に応じて `プラグイン構造.md` へのリンクも追加する。

JP ミラー（`セットアップウィザード.jp.md`）も合わせて確認・修正する。

## 横展開

リファレンス内のクロスリファレンスがリネーム・再構成で陳腐化するパターン。セクション名変更時はファイル内の参照を grep で確認すると良い。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない
