#!/usr/bin/env bash
# gh-kit ラベル名定義 — Issue/PR 操作で参照する全ラベル名を一元管理する。
# 各 SKILL/agent から:
#   . "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# で読み込み $LABEL_* を参照する。
# ラベル名を変えるときはここだけ書き換えればよい。

# 共通排他 — 何らかの作業中。誰も触らない印
LABEL_PROCESSING="processing"

# 共通レビュー
LABEL_NEEDS_AI_REVIEW="needs-ai-review"        # AI レビュー必要（必ず付く）
LABEL_NEEDS_USER_REVIEW="needs-user-review"    # ユーザーレビュー必要（AI が状況判断）
LABEL_NEEDS_FIX="needs-fix"                    # レビュー結果、修正必要

# Issue 専用
LABEL_AI_CODE_SCAN="ai-code-scan"              # claude code がスキャンして起票した Issue

# PR 専用
LABEL_WIP="wip"                                # Draft 雛形 PR

# ラベルの色（label create のとき使用）
LABEL_COLOR_PROCESSING="FBCA04"
LABEL_COLOR_NEEDS_AI_REVIEW="0E8A16"
LABEL_COLOR_NEEDS_USER_REVIEW="C5DEF5"
LABEL_COLOR_NEEDS_FIX="D93F0B"
LABEL_COLOR_AI_CODE_SCAN="1D76DB"
LABEL_COLOR_WIP="C2E0C6"
