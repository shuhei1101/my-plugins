---
name: rules-creator
description: （日本語訳）`.claude/rules/` に新しい path-scoped ルールをスキャフォールドするスキル。ルールマーケットに該当がない場合に、ゼロからカスタムルールを作成する。
---

> このファイルは `SKILL.md` の日本語翻訳です。Claude Code には自動読み込みされません。
> 変更する場合は、まずこのファイルを更新し、その後 `SKILL.md`（英語本体）にも同じ変更を反映してください。

---

# rules-creator — 新しい path-scoped ルールのスキャフォールド

ユーザーがルールマーケットに存在しない新しい `.claude/rules/<name>.md` を必要とするときに使う。
`claude-rule` の記述規約で定められた 4 ステップに沿ってファイルを作成する。

---

## 事前確認：まずルールマーケット

作成前に必ず `/claude-rule:rule-market list` を実行する。
マーケットにあればインストールして終了する。このスキルは「マーケットに該当なし」の場合のみ続行する。

---

## 手順

### Step 1: ユーザーに 3 つ質問する

`AskUserQuestion` で:

1. **ルール名** — `<name>.md` の `<name>` 部分（例: `api-conventions` / `db-schema`）
2. **対象パス** — `paths:` frontmatter 用のグロブパターン（例: `src/api/**/*.ts`）。複数可
3. **一行の説明** — このルールが何を制御し、なぜ必要か

ユーザーがトピックだけ言った場合（例:「データベース層のルール作って」）は、パスと一行説明を提案して確認する。

---

### Step 2: 重複チェック

`.claude/rules/*.md` を `Glob` で確認し、同じ対象をカバーする既存ルールがないか確認する。
存在する場合はそちらに追記するか提案する。

---

### Step 3: JP ミラーを書く（`.claude/rules-jp/<name>.md`）

テンプレート:

```markdown
---
paths:
  - "<path-pattern>"
---

# <Area> ルール（日本語ミラー）

> Claude には読み込まれません。本体は `.claude/rules/<name>.md`。

## なぜ必要か

<このルールがないと何が起きるか — 1〜3行>

## ルール

- ✅ やる: <肯定形ルール>
- ❌ やらない: <禁止事項>

## 参照ドキュメント

- <関連する仕様・設計ドキュメントへのリンク>

## 編集ルール

- このファイルを編集したら、必ず `.claude/rules/<name>.md` 側も同期する
```

---

### Step 4: 英語本体を書く（`.claude/rules/<name>.md`）

JP ミラーを行単位で翻訳する。
- XML タグを適切なセクションに適用する（`<when_to_apply>`, `<hard_rules>`, `<steps>` 等）
- "やる/やらない" は "Do: ..." / "Don't: ..." ペアに変換
- "Claude には読み込まれません" の注記は英語版には不要（削除する）

---

### Step 5: `CLAUDE.md` を更新する

`CLAUDE.md` に `Folder-scoped rules` テーブルがあれば行を追加する:

```markdown
| `<name>.md` | `<path-pattern>` — <一行説明> |
```

テーブルがない場合はスキップ。ファイル全体を再構成しない。

---

### Step 6: 動作確認の案内

ユーザーに説明する:

1. 対象パスにマッチするファイルを新しい Claude Code セッションで開く
2. `<system-reminder> Contents of .claude/rules/<name>.md` が表示されることを確認
3. 読み込まれない場合は `paths:` グロブを見直す（`*.py` は再帰しない / `**/*.py` は再帰する）

---

### Step 7: コミット

以下 4 ファイルを必ず同じコミットに含める（部分コミット禁止）:
- `.claude/rules/<name>.md`
- `.claude/rules-jp/<name>.md`
- `CLAUDE.md`（更新した場合）
- `CLAUDE.jp.md`（更新した場合）

```
docs(rules): <name>.md 新規追加 (<path-pattern>)
```

---

## やってはいけないこと

- `.claude/rules/<name>.md` を日本語で書かない（Claude がそのまま指示として読む）
- JP ミラーを `.claude/rules/` 内に置かない（自動ロードされる）→ 必ず `.claude/rules-jp/` に置く
- 英語本体だけ作って JP ミラーを省略しない
- `CLAUDE.md` テーブルがあるのに行追加をスキップしない

---

## 関連スキル

- `/claude-rule:rule-market` — ライブラリからルールをインストール（まずこちらを確認）
- `/claude-rule:claude-rule` — 記述規約の全詳細（英日ミラー規約・XML タグ・配置場所）
