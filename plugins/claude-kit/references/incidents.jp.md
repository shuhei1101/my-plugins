<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# incidents — 再発防止フォーマット

失敗・誤解・思い込みを記録して同じミスを繰り返さないための `incidents` ルールの
構造と使い方を定義する。

---

## ファイル構成

```
.claude/rules/
└── incidents.md                    # インデックス — 常時読み込み、短く保つ

.claude/references/incidents/
├── {slug}.md                       # 詳細（英語）
└── {slug}.jp.md                    # 詳細（日本語）
```

インデックスは `.claude/rules/` に置くことで毎セッション自動読み込みされる。
詳細ファイルは `.claude/references/incidents/` に置き、**自動読み込みされない**
設計にする — Claude はインデックスのリンクをたどったときだけ参照する。

### incidents.md（インデックス）

毎セッションのシステムプロンプトとして常時読み込まれる。短く保つこと — 1行ごとに
コンテキストウィンドウを消費する。概要は1行だけ書き、詳細はサブフォルダに置く。

```markdown
# Incidents

| 日付 | 概要 | 詳細 |
|---|---|---|
| YYYY-MM-DD | {何が問題でどう避けるかを1行で} | [詳細](../references/incidents/{slug}.md) |
```

**執筆の心得**: 簡潔さを最優先にする。1エントリ1行。概要が80文字を超えそうなら
短くする — 詳細はリンク先を見ればよい。

### {slug}.md（詳細 — 英語）

```markdown
# {Title}

**Date**: YYYY-MM-DD
**Category**: {command-error | wrong-assumption | tool-misuse | other}

## What Happened

{試みたこと・失敗した内容・正しいアプローチを具体的に記述}

## How to Avoid

{次回適用すべき具体的なルールやチェック方法}

## Context

{任意: 適用するプロジェクト・環境・条件}
```

### {slug}.jp.md（詳細 — 日本語）

`{slug}.md` と同じ構造で日本語で記述する。

---

## slug の命名

ケバブケースで、一目で内容がわかる名前にする:

- `python-encode-utf8-not-cp932`
- `git-worktree-path-relative`
- `marketplace-version-out-of-sync`

---

## 記録するタイミング

以下のときに incidents エントリを書く:
- コマンドを実行して失敗し、正しいコマンドが判明したとき
- 思い込みで回答したがユーザーに訂正されたとき
- ツール・フラグ・API が想定と異なる挙動をしたとき

以下には書かない:
- スキルやルールに書くべき一般的な知識
- すでに他の場所に記録済みの内容
- 再発可能性が低い単純なミス
