# claude-kit: conversation-history skills

## 概要

claude-kit プラグインに、現在のセッションの会話履歴を活用して
ルールまたはスキルを自動生成する2つのスキルを追加する。

---

## スキル一覧

### conversation-to-rule

**目的**: 会話中に発見したファイルの依存関係・フォルダ構成の知識をルールとして永続化する

**生成物**:
- `.claude/rules/<name>.md` — パススコープルール（英語）
- `.claude/rules-jp/<name>.md` — 日本語ミラー
- `CLAUDE.md` への `## Repository Structure` 追記（新知識があれば）

**フロー**:
1. 会話を分析してファイルリンク候補・フォルダ構成知識を抽出
2. ユーザーと確認して範囲を確定
3. 既存ルールの重複チェック
4. `rule-creator` を起動してルールを作成
5. フォルダ構成インデックスを追記（既存記述は維持）

**ステップ5の検索方針**:
- 検索対象: `CLAUDE.md` + `.claude/rules/` 配下の `paths:` なし（常時ロード）ルール
- セクション名は固定しない（`Repository Structure`・`フォルダ構成`・`Architecture` 等）
- フォルダ構成が書かれているセクションを内容で判断して探す
- 見つかれば追記、なければ `CLAUDE.md` 末尾に新規追加

---

### conversation-to-skill

**目的**: 会話で実施した作業手順を再利用可能なスキルとして記録する

**生成物**:
- `.claude/skills/<name>/SKILL.jp.md`
- `.claude/skills/<name>/SKILL.md`

**フロー**:
1. 会話を分析して繰り返し使えそな作業フローを抽出
2. 3段階の質問でユーザーと対話（対象範囲・名前と起動条件・前提条件）
3. ステップ構造に変換してユーザーに確認
4. `skill-creator` を起動してスキルを作成

---

## 設計方針

- どちらのスキルも既存のスキル（`rule-creator` / `skill-creator`）に処理を委譲する
- ユーザーとの対話を重視し、自動生成のみに頼らない
- 既存の記述を破壊しない（追記のみ）
