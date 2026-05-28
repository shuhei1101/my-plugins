<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# スキル作成ガイド

`.claude/skills/<name>/SKILL.md` ファイルの設計・作成・評価の方法。
スキルはオンデマンドのワークフローであり、明示的に（`/skill-name`）呼び出すか、`description`
frontmatter によって自動起動される。本ガイドは自己完結している: （`SKILL.md` を編集しているため）
注入されたら、これに従ってファイルを直接執筆すること。ファイル種別の判定、JP/EN ミラールール、
出自スタンプ手順については `common.md` を併読すること。
英語原本: `references/skills.md`

---

## スキルが読み込まれるタイミング

- `/skill-name` として明示的に呼び出されたとき
- `description` frontmatter の条件にマッチしたとき（自動起動）

デフォルトでは `disable-model-invocation: true` を使わないこと。
**例外**: 人間だけが実行すべきスキル（マージ・デプロイ・破壊的操作）には使う。
このフラグを持つスキルは「自動起動の禁止」を記述する必要はない — フラグが既にそれを強制している。

---

## ステップ 1 — スキルが正しい種別か確認する

執筆前に、内容に対して選択が妥当か検証する:

| 内容が… | 判定 |
|---|---|
| ユーザー操作や分岐を伴う複数ステップのワークフロー | ✅ スキル — 正しい |
| ユーザー確認ポイントが必要な繰り返しルーティン | ✅ スキル — 正しい |
| 3 つ以上の明確なステップ | ✅ スキル — 正しい |
| 1〜2 個の単純なルールや規約 | ⚠️ `CLAUDE.md` か `.claude/rules/` の方が単純 |
| 複数パスを跨ぐファイル同期（「X を編集 → Y, Z も更新」） | ⚠️ `.claude/rules/` の方が適切 |
| 毎回自動で発火すべきもの | ⚠️ `hooks` |
| ワークフロー + 同期ルールの混在 | ⚠️ 分割する: ワークフローは skill、同期は rules |

別のファイル種別の方が合うなら、そちらへ振り向ける（完全な判定表は `common.md` 参照）。

---

## ステップ 2 — 既存の類似スキルを確認する

1. `.claude/skills/**/SKILL.md` を Glob し、各 `description` + 概要を読む。
2. トリガーが重複する、または手順が似ているスキルがある場合:
   - **統合** — 既存スキルを拡張してこのケースもカバーする（トリガーが重複する場合に推奨）、または
   - **別々に保つ** — 明確な境界（異なるトリガー条件、異なるユーザーフロー）がある場合のみ。
3. 重複が無ければ → 続行する。

---

## ステップ 3 — `description` frontmatter（自動起動トリガー）

精密に書く — 「ユーザーが X と言ったとき」。曖昧な記述は誤起動を招く。
必要なのは `name` と `description` のみ。`allowed-tools` は**追加しない**こと。

```yaml
---
name: skill-name
description: |
  Trigger when the user says "〜したい", "〜して", or calls `/namespace:skill-name` explicitly.
---
```

---

## ステップ 4 — まず JP ミラー（`SKILL.jp.md`）を書き、次に翻訳する

`common.md` に従い、まず `.claude/skills/<name>/SKILL.jp.md` を日本語で執筆し、それから
英語の `SKILL.md` を（手作業または `jp-mirror-translator` エージェントで）作る。両ファイルに
スタンプを付ける（`common.md` の出自手順）。

### ステップ構造

各ステップは以下のパターンに従う。ステップが必要とするサブセクションのみ使う:

```markdown
### Step N: (Action name)

#### Condition
(Prerequisites for entering this step)

#### Input
(Data, files, prior step output, or user input used here)

#### Process
1. Do X
→ Proceed to Step N+1

#### Output
(What exists when this step is complete)

#### Notes
##### Checklist
##### Branching
##### Prohibitions
```

### SKILL.md の完全な雛形

```markdown
---
name: <skill-name>
description: |
  Precise trigger conditions. "When the user says X", "when editing Y".
---

# <skill-name> — one-line summary

<1–2 sentences: what this skill does.>

---

## Overview

<Background, purpose, why this skill exists.>

---

## Tasks

### Step 1: <action>
...
```

---

## 参考資料の配置

- **複数ステップから使われる** → 末尾の `## References` セクションに置く
- **1 ステップだけで使われる** → そのステップに直接埋め込む

大規模なスキルの場合、重い参考資料は `references/` に外出しし、スキルからパスでリンクする。

> 注: スキルは CLI 形式の引数を取れない — コンテキストにロードされる Markdown ファイルである。
> 期待する入力は自然言語の箇条書きで記述し、`--flag` の表では決して書かない。

---

## 最終チェックリスト

- [ ] `SKILL.md`（英語、Claude がロード）と `SKILL.jp.md`（JP ミラー）の両方が、構造を一致させて存在する
- [ ] `description` frontmatter に精密なトリガー条件がある。設定は `name` + `description` のみ
- [ ] 共有内容は `## References` にある。単一ステップの内容はそのステップに留まる
- [ ] 両ファイルとも `provenance.md` に従ってスタンプ済み（ファイルを書く際に自動注入される）
