---
name: claude-refactor
description: |
  Audit and organize Claude configuration (rules / skills / CLAUDE.md / hooks).
  Trigger when the user says "ルールを整理して", "設定が肥大化してきた",
  "スキルに重複がある気がする", "CLAUDE.md が長くなってきた",
  ".claude/ をきれいにしたい", or calls `/claude-kit:claude-refactor` explicitly.
---
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# claude-refactor — Claude 設定の監査と再編成

`.claude/` 配下の rules / skills / CLAUDE.md / hooks を監査し、フォルダ再編成・過結合/重複検出・
ファイルタイプ移管・JP/EN ミラー整合チェックを提案する。

これらの判定基準はすべて本プラグインの `references/`（Step1 で読む）にある。このスキルは
**ワークフロー**（収集 → 分析 → 提案 → 実行）であり、基準をインラインで再掲しない。

---

## タスク

### ステップ 1: 対象ファイルの収集と基準の読み込み

#### 処理

1. リファレンスガイド（本プラグインの `references/`）を読む — 以下すべての判定の基準になる:
   - `common.md` — ファイル種別の判定基準、増殖防止ガード、JP/EN ミラー規則
   - `rules.md` — 2 種類のルール、ユースケース指向設計、統合/分離、フォルダ構成
   - `skills.md` — skill が適切な種別か、ステップ構造
   - `hooks.md` — フックイベント、使用時機
   - `claude-md.md` — 薄肉原則、抽出先
2. 対象を収集:

| スコープ | 収集対象 |
|---|---|
| rules | `.claude/rules/**/*.md` を glob。各 `paths:` と概要を読む |
| rules JP | `.claude/rules-jp/**/*.md` を glob。英語ルールとの対応を確認 |
| skills | `.claude/skills/**/SKILL.md` + `plugins/*/skills/**/SKILL.md` を glob。`name` / `description` を読む |
| skills JP | 各 `SKILL.jp.md` の存在を確認 |
| CLAUDE.md | すべての `CLAUDE.md`（ルート + サブフォルダ）を列挙。行数を確認 |
| CLAUDE.md JP | 各 `CLAUDE.jp.md` の存在を確認 |
| hooks | `.claude/settings.json` / `settings.local.json` / `hooks/hooks.json` の hooks セクションを読む |

→ ステップ 2 へ

---

### ステップ 2: 各スコープを references と照合して分析

#### 処理

Step1 の references の基準を適用する — ここで再導出しない。

- **rules**（`rules.md` + `common.md`）: フォルダ構成整理（フラットなファイル → `core/` / `feature/` / 任意フォルダ）、統合候補（同ドメイン / `paths:` 重複）、分離候補（無関係ドメインにまたがる `paths:`）、ファイルタイプ適合。
- **skills**（`skills.md` + `common.md`）: 類似スキルのペア（`description` トリガー重複 — 提示するが強制統合しない）とファイルタイプ適合（rule / CLAUDE.md 1 行にすべきか）。
- **CLAUDE.md**（`claude-md.md`）: 肥大化（約200行超、または他所に属す詳細/ワークフロー/参照資料）と節ごとの抽出先。
- **hooks**（`hooks.md`）: rules/CLAUDE.md 内でフック化すべき内容（イベント対応に従う）、および冗長/未使用の既存フックエントリ。
- **JP/EN ミラー**（`common.md`）: 欠けている `.jp.md` / `rules-jp/` / `CLAUDE.jp.md` の対応物。

→ ステップ 3 へ

---

### ステップ 3: 提案の提示と確認

#### 処理

1. 所見を次の表に整理する（項目が無い表は省略。空のスコープは「問題なし」と報告）:

   - **rules: フォルダ移動** — ファイル（現在）/ 移動先 / 理由
   - **rules: 統合** — 対象 / 統合先 / 理由
   - **rules: 分離** — 対象 / 分割案 / 理由（コンテキスト節約）
   - **ファイルタイプ移管** — 対象（現在）/ 移管先タイプ / 理由
   - **CLAUDE.md 抽出** — 節 / 抽出先 / 理由
   - **hook 移行** — 対象（現在）/ フックイベント / 理由
   - **類似スキル** — スキル A / スキル B / 類似点 / 相違点
   - **欠落 JP ミラー** — 英語ファイル / 作成すべき JP ミラー

2. ユーザーに尋ねる: **すべて実行** / **個別選択** / **キャンセル**。確認を待つ。

→ ステップ 4 へ

---

### ステップ 4: 確定した変更の実行

#### 処理

ユーザーが承認したものだけ適用する。**対象ファイルを直接編集する** — オーサリングガイド
（`skills.md` / `rules.md` / `claude-md.md` / `hooks.md` + `provenance.md`）は
`claude-kit-references-injection` フックがファイル書き込み時に自動注入するので、その場で従う。

- **ルールフォルダ再編成**: `git mv` で移動（履歴保持）。各フォルダに `_overview.md` を生成:

  ```markdown
  # {folder-name} — {一行カテゴリ説明}

  ## About this folder

  {このカテゴリのルール方針を1〜3文で}

  ## File list

  | File | Content |
  |---|---|
  | `{file}.md` | {一行説明} |
  ```

- **rule / skill / CLAUDE.md / hook の作成・変換・統合・分割**: 注入ガイドに従ってその場で編集。JP ミラーも同期。
- **JP ミラー作成**: `.jp.md` を執筆（または `jp-mirror-translator` エージェントを使う）。
- リネーム/移動後は、プロジェクト内の他所からの参照をすべて更新する。

→ ステップ 5 へ

#### 注意事項

##### 禁止事項

- `cp` ではなく `git mv` を使う（git 履歴を保持）
- リネーム/移動したファイルに言及する他のスキル/ルールの参照を必ず更新する

---

### ステップ 5: 結果報告

#### 処理

1. 変更 / 生成 / 削除したファイルを報告
2. ユーザーにレビューとコミットを促す

---

## 参照

判定基準は本プラグインの `references/`（Step1 で読む）にある: `common.md`, `rules.md`,
`skills.md`, `hooks.md`, `claude-md.md` — 加えて編集ファイルのスタンプ用に `provenance.md`。
