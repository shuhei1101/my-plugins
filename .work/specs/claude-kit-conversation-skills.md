# claude-kit: conversation-history skills

## 概要

claude-kit プラグインに、現在のセッションの会話履歴を活用して
Claude Code の各種アーティファクトを生成する統合スキル `conversation-capture` を提供する。

旧スキル `conversation-to-skill` と `conversation-to-rule` は本スキルに統合・廃止。

---

## スキル

### conversation-capture（統合版）

**目的**: 会話履歴を分析し、最適なアーティファクト種別を提案してユーザーに選択させ、
対応するクリエイタースキルで実装する

**生成物（選択に応じて変わる）**:
| 選択 | 生成物 | 委譲先 |
|---|---|---|
| スキル | `.claude/skills/<name>/SKILL.md` 等 | `claude-kit:skill-creator` |
| ルール | `.claude/rules/<name>.md` 等 | `claude-kit:rule-creator` |
| フック | `settings.json` の hooks エントリ | `claude-kit:hook-creator` |
| CLAUDE.md | `CLAUDE.md` への追記・新規作成 | `claude-kit:claude-creator` |

**フロー**:
1. 会話を分析して「何が行われたか」を把握
2. 既存アーティファクトをスキャンし、統合可能なものを特定
3. 最適なアーティファクト種別を複数提案（新規/既存編集の別を明示）
4. ユーザーが種別を選択
5. 選択に応じたクリエイタースキルを起動

**アーティファクト種別の判定基準**:
- **スキル**: 3ステップ以上の繰り返し作業フロー、ユーザーとの対話を含む手順
- **ルール**: ファイル依存関係の発見、パス構成・役割の知識
- **フック**: 特定イベント（ツール使用前後・セッション開始等）への自動反応
- **CLAUDE.md**: プロジェクト全体に適用する規約・ガイドライン・禁止事項

---

## 設計方針

- 全アーティファクト種別を1スキルでカバーし、ユーザーが起動先を意識不要にする
- 提案は複数（通常2〜3種別）提示し、ユーザーが選択する
- 各クリエイタースキル（skill-creator / rule-creator / hook-creator / claude-creator）に処理を委譲する
- ユーザーとの対話を重視し、自動生成のみに頼らない
- 既存の記述を破壊しない（追記のみ）
