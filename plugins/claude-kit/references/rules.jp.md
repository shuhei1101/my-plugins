<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# ルール作成ガイド

`.claude/rules/<name>.md` ファイル（パススコープルール）の設計・作成・評価の方法。
ルールは関連ファイルをドメインにまとめ、Claude が `paths:` パターンにマッチするファイルを
**読む**ときに自動ロードされる。本ガイドは自己完結している: （ルールファイルを編集しているため）
注入されたら、これに従ってルールを直接執筆すること。`common.md` を併読すること。
英語原本: `references/rules.md`

---

## ルールが読み込まれるタイミング

`paths:` パターンにマッチするファイルを Claude が**読む**ときにロードされる。

- ✅ ファイルを読む → ロードされる
- ✅ ファイルを編集する（Claude は編集前に読む） → ロードされる
- ❌ 読み込みを伴わないシェルのみのコマンド（`mv`, `rm` など） → ロードされない
- ❌ マッチするファイルにアクセスせず作業する → ロードされない

---

## ルールの 2 種類

### ① リンクルール（ファイル連携型）

関連ファイルを束ね、1 つを編集したら執筆者が他も確認するよう強制する。

- 関連ファイルすべてを `paths:` に列挙する
- 例: 抽象クラス + インターフェース + 子クラス + 親クラスを 1 つのルールに
- 例: 設定ファイル + 仕様書 + テストケース + 実装コードを束ねる
- **効果**: どれか 1 つを編集したとき、Claude が関係全体のコンテキストを把握できる

### ② コンテキストルール（トリガーロード型）

特定エリアで作業するとき、関連する知識・仕様・ガイドラインを自動ロードする。

- 触ったときにこのルールのロードをトリガーすべきファイルを `paths:` に設定する
- 例: `config/` を触る → 設定仕様ルールがロードされる
- 例: `src/` を触る → コーディング規約ルールがロードされる

---

## 作成ワークフロー

### ステップ 1 — 既存のカバレッジを確認する

`.claude/rules/**/*.md` を Glob し、各 `paths:` を読み、対象ファイルが既存ルールに既に
マッチするかテストする。カバーされていれば、新規ファイルを作らず**そのルールを拡張する**。

### ステップ 2 — ドメイン情報を集める

特定する:
- **ドメイン名** — kebab-case（例: `models`, `voice`, `assets-bgm`）
- **このドメインのファイル**、3 カテゴリで: 設定/スキーマ（YAML/JSON/定数）、ソースコード、ドキュメント（仕様/アーキテクチャ）
- **1 行の説明** — このドメインが何をするか、なぜこれらのファイルを同期させる必要があるか

### ステップ 3 — ルールが正しい種別か検証する

| ファイルが… | 判定 |
|---|---|
| 複数の異なるフォルダにまたがる | ✅ ルール — クロスパスリンクに正しい |
| すべて単一フォルダ内 | ✅ ルール（監査性）またはサブフォルダ `CLAUDE.md`（co-location） — ユーザーの好みを聞く |
| ワークフローや手順について | ⚠️ `.claude/skills/` の方が合うかも |
| 混在 | ⚠️ 分割する: クロスパスは rule、フォルダローカルはユーザー選択 |

クロスパスのリンクは常に `.claude/rules/` に属する。

### ステップ 4 — 既存の類似ルールを確認する

Glob して概要 + `paths:` を読む。重複時: 既存ルールに**統合する**、または明確な境界
（異なる更新トリガー / 所有権）がある場合のみ**別々に保つ**。

### ステップ 5 — まず JP ミラーを書き、次に翻訳する

まず `.claude/rules-jp/<name>.md` を日本語で執筆し、それから `.claude/rules/<name>.md` を
（手作業または `jp-mirror-translator` エージェントで）作る。両方にスタンプを付ける（`common.md` 参照）。

> ⚠️ JP ミラーを `.claude/rules/` の中に置か**ない**こと — `.claude/rules-jp/` を使う。rules
> ディレクトリは再帰的にスキャンされるため、ミラーが自動ロードされてしまう。

ドメイン内のファイルが追加・削除・リネームされたとき Claude がルール自体を更新できるよう、
常に `## Rule Maintenance` セクションを含めること。

---

## ユースケース指向の `paths:` 設計

**「いつ読まれるべきか」を起点にする。**

1. **ユースケースを特定する** — このルールはどんな作業で役立つか？
2. **トリガーファイル/フォルダを特定する** — その作業中に必ず触るファイルは何か？
3. **そのファイルを `paths:` に設定する** — それが触られるたびにルールがロードされる

**例 — 設定仕様のコンテキストルール**: `config/` を編集したら仕様をロードすべき →
`paths:` に `config/**` を設定する。

**例 — 常時オンのルール**（例: コーディング規約）: 任意のソースコードを触る →
`src/**` や `**/*.ts` のような広いパターンを設定する。

> by-name フォルダのパターンには `**/`（例: `**/tools/**/*.py`）を前置し、プロジェクトルートだけでなく
> モノレポのサブプロジェクトでもマッチするようにする。

---

## 統合・分離の基準

- **統合**: 同じドメインをカバーし内容が重複するルール → 1 つに統合する
- **分離**: 無関係なドメインをカバーする 1 つのルール → ドメインごとに分割する
  - 無関係なディレクトリにまたがる `paths:` は、触るたびに不要なコンテキストロードを起こす
  - 原則: 1 ドメイン = 1 ルールファイル

---

## フォルダ構成の基準

### 必須フォルダ

| フォルダ | 役割 | 何を入れるか |
|---|---|---|
| `core/` | プロジェクト全体の基礎ルール | コーディング規約、ワークフロー、環境設定、開発プロセス全般 |
| `feature/` | 機能固有のドメイン知識 | 機能ごとのルール、仕様、設計判断（1 機能 = 1 ファイル） |

### 任意フォルダ（コードベース依存）

| フォルダ | 追加する目安 |
|---|---|
| `ui/` | フロントエンドが存在: `components/`, `pages/`, `views/` など |
| `api/` | バックエンド API のルールが多い / `routes/` や `handlers/` ディレクトリ |
| `infra/` | Docker / CI/CD / デプロイ系のルールが多い |

---

## ルールファイルの必須セクション

| セクション | 内容 | 必須/推奨 |
|---|---|---|
| frontmatter `paths:` | ルールをトリガーする glob パターン | **必須** |
| `## Overview` | このルールが何を管理するかの説明 | 必須 |
| `## Related Files` | ファイルパスと役割 | 推奨 |
| `## When Editing` | このドメインで編集するとき検証する項目のチェックリスト | 推奨 |
| `## Rule Maintenance` | ファイル追加/削除/リネーム時にルール自体を更新する方法 | **推奨** |

---

## 構造例

```markdown
---
paths:
  - "src/models/**/*.py"
  - "tests/test_models.py"
  - "docs/specs/models.md"
---

## Overview

Rule linking implementation, tests, and specs for the models domain.
When editing any file in this domain, check all the others too.

## Related Files

| File path | Role |
|---|---|
| `src/models/**/*.py` | Implementation |
| `tests/test_models.py` | Tests |
| `docs/specs/models.md` | Specification |
| `.claude/rules/models.md` | This rule |

## When Editing

- [ ] Implementation and tests are consistent
- [ ] New fields are covered by tests
- [ ] Spec reflects current behavior
- [ ] New files added to this domain → updated `paths:` and Related Files?

## Rule Maintenance

- **Added a new file** → add it to `paths:` and Related Files
- **Deleted or renamed a file** → remove/update it in `paths:` and Related Files
- **Domain responsibilities changed** → update the Overview
```

---

## 単一フォルダの内容: rule vs サブフォルダ CLAUDE.md

| 優先 | 選択 |
|---|---|
| **有効なルールを一箇所で見たい**（監査性） | `.claude/rules/<name>.md` |
| **ルールをコードに隣接させたい**（近接性） | サブフォルダ `CLAUDE.md` |

クロスパスのリンクは常に `.claude/rules/` に属する。
