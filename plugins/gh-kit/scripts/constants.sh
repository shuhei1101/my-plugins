#!/usr/bin/env bash
# gh-kit 定数定義。Session Start フックで自動実行され、環境変数としてセッション内に展開される。
# 定数名にはプラグイン名プレフィックス GH_KIT_ を付与する。

export GH_KIT_LABEL_PROCESSING="processing"
export GH_KIT_LABEL_NEEDS_AI_REVIEW="needs-ai-review"
export GH_KIT_LABEL_NEEDS_USER_REVIEW="needs-user-review"
export GH_KIT_LABEL_NEEDS_FIX="needs-fix"
export GH_KIT_LABEL_AI_CODE_SCAN="ai-code-scan"
export GH_KIT_LABEL_WIP="wip"

export GH_KIT_LABEL_COLOR_PROCESSING="FBCA04"
export GH_KIT_LABEL_COLOR_NEEDS_AI_REVIEW="0E8A16"
export GH_KIT_LABEL_COLOR_NEEDS_USER_REVIEW="C5DEF5"
export GH_KIT_LABEL_COLOR_NEEDS_FIX="D93F0B"
export GH_KIT_LABEL_COLOR_AI_CODE_SCAN="1D76DB"
export GH_KIT_LABEL_COLOR_WIP="C2E0C6"
