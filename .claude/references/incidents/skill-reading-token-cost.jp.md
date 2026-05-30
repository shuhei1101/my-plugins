<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
> ⚠️ **Japanese mirror** — not loaded by Claude. When updating this file, always update the English original `.claude/references/incidents/skill-reading-token-cost.md` at the same time.

# インシデント: スキルが他スキルを読み込むとトークンが膨張する

**日付**: 2026-05-23
**PR**: PR68 (conversation-to-claude-improve)

## 何が起きたか

`conversation-to-claude` には Step 0 があり、提案前に4つのクリエータースキル（`skill-creator`・`rule-creator`・`hook-creator`・`claude-creator`）を読み込んでいた。正確な判定基準を Claude に与えるための設計だった。

しかし Claude Code の各スキルは ~2500 トークンが上限のため、4スキルの読み込みで起動のたびに ~10,000 トークンを消費していた。

## 根本原因

「正確に提案するには完全なスキルを読む必要がある」という思い込み。実際に必要なのは各スキルの「いつ使うか」の判定基準だけだった。

## 修正

Step 0 を完全削除。各クリエータースキルから必要な判定基準だけを抽出し、`conversation-to-claude` の References セクション（`§ Artifact type knowledge`）に直接埋め込んだ。スキルが自己完結するようになった。

## 再発防止ルール

**起動時に他のスキルを読み込む設計にしない。** 他スキルの判定基準が必要な場合は、関連する意思決定ルールだけを抽出してインラインで埋め込むこと。スキルは自己完結させること。
