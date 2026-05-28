<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# CLAUDE.md 作成ガイド

プロジェクトまたはサブフォルダの `CLAUDE.md`（およびその `CLAUDE.jp.md` ミラー）の設計・作成・
評価の方法。本ガイドは自己完結している: （`CLAUDE.md` を編集しているため）注入されたら、これに
従ってファイルを直接執筆すること。`common.md` を併読すること。
英語原本: `references/claude-md.md`

---

## 読み込まれるタイミング

| 配置 | 読み込まれるタイミング |
|---|---|
| プロジェクトルート | セッション開始のたび — 常時ロード |
| サブフォルダ | 遅延、Claude がそのフォルダまたはサブフォルダ内のファイルを読んだとき |

**ルート**の CLAUDE.md はプロジェクト全体のワークフロー、コミット規則、サーバー管理、
フォルダスコープのルール表を定義する。**サブフォルダ**の CLAUDE.md はそのフォルダの内容と
ローカル規約を記述し、毎セッションロードせずに Claude にコンテキストを与える。

---

## 重要: 薄く保つ

ルートの CLAUDE.md は**毎**セッションでロードされる — 内容が多いほどコンテキストを消費する。

### 外出し先ガイド

| 内容の性質 | アクション |
|---|---|
| 特定ファイルを編集するときだけ必要 | `.claude/rules/` に移す |
| 複数ステップのワークフローや手順 | `.claude/skills/` に移す |
| 特定フォルダにだけ関係する | そのサブフォルダの `CLAUDE.md` に移す |
| 詳細説明/参照（ときどき読む） | `.claude/references/` に移し、CLAUDE.md にはパスだけ書く |
| プロジェクトに既にある仕様/ドキュメント | パスだけ書く。内容を複製しない |

### 行数ガイドライン

- ルートの CLAUDE.md は 200 行未満を目標とする
- 200 行を超えたら、ドメイン固有の内容を `.claude/rules/` に外出しする

---

## 作成ワークフロー

### ステップ 1 — 詳細を集める

- **配置** — プロジェクトルート（`CLAUDE.md`）かサブフォルダ（例: `src/CLAUDE.md`）か？
- **ルートの場合**: 全体ワークフローのステップ、禁止事項、フォルダスコープのルール表のエントリ
- **サブフォルダの場合**: フォルダ内のファイル、その役割、ローカル規約
- **内容の概要** — どんな指示/説明を含めるか

### ステップ 2 — CLAUDE.md が正しい種別か検証する

| 内容が… | 判定 |
|---|---|
| プロジェクト全体のワークフローやグローバル規約 | ✅ CLAUDE.md（ルート） — 正しい |
| 単一フォルダの規約/説明 | ✅ co-location なら CLAUDE.md（サブフォルダ）。監査性が優先なら `.claude/rules/` |
| クロスパスのファイル同期（「X を編集 → 別の場所の Y, Z も更新」） | ⚠️ `.claude/rules/` |
| ユーザー操作を伴う複数ステップのワークフロー | ⚠️ `.claude/skills/` |
| 混在 | ⚠️ ファイル種別を跨いで分割する |

### ステップ 3 — まず `CLAUDE.jp.md` を書き、次に翻訳する

CLAUDE.md は**ステップ形式ではなく記述形式**を使う。まず `CLAUDE.jp.md` を日本語で執筆し、
約 200 行未満に保ち（長ければドメイン内容を `.claude/rules/` に外出し）、それから英語の
`CLAUDE.md` を（手作業または `jp-mirror-translator` エージェントで）作る。両方にスタンプを付ける（`common.md` 参照）。

---

## `.claude/references/` について

概念的には CLAUDE.md に属するが毎セッションのロードが不要な内容のための場所。
CLAUDE.md にはファイルパスだけを書く — Claude は実際に必要になったときにそのファイルを読む。

---

## 必須セクション

| セクション | 内容 | 必須/推奨 |
|---|---|---|
| タイトル | H1 見出し | 必須 |
| `## Overview` | プロジェクト/フォルダの説明 | 必須 |
| `## Folder structure` | パス→概要の表 | 推奨 |
| `## Constraints` | Claude が常に守るべきルールと禁止事項 | 推奨 |
| （その他のセクション） | 必要に応じて自由に追加 | 任意 |

---

## 構造例

```markdown
# Project Name

## Overview
Description of this project or folder.

## Folder structure

| Path | Summary |
|------|---------|
| `src/` | Implementation code |
| `docs/specs/` | Specification documents |
| `.claude/` | Claude Code configuration |

## Constraints

- Always run `npm test` before committing
- Never push directly to `main`
```

---

## サブフォルダ CLAUDE.md vs rules

| 優先 | 選択 |
|---|---|
| **ルールをコードに隣接させたい**（近接性） | サブフォルダ `CLAUDE.md` |
| **有効なルールを一箇所で見たい**（監査性） | `.claude/rules/<name>.md` |

クロスパスのリンクは常に `.claude/rules/` に属する。
