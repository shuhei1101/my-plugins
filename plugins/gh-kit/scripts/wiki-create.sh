#!/usr/bin/env bash
# wiki-create.sh — GitHub Wiki ローカルリポジトリに 1 ページ作成して push する。
#
# 使い方:
#   GH_KIT_WIKI_PATH=/path/to/repo.wiki \
#     bash wiki-create.sh --page-name {カテゴリ}-{対象}.md --body-file /tmp/body.md
#
# 既存ファイルがある場合は上書きせず exit 2 で停止する（更新は wiki-sync 経由）。

set -euo pipefail

PAGE_NAME=""
BODY_FILE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --page-name) PAGE_NAME="$2"; shift 2 ;;
    --body-file) BODY_FILE="$2"; shift 2 ;;
    *) echo "ERROR: 未知の引数: $1" >&2; exit 1 ;;
  esac
done

if [ -z "${PAGE_NAME}" ] || [ -z "${BODY_FILE}" ]; then
  echo "ERROR: --page-name と --body-file は必須" >&2
  exit 1
fi

WIKI_PATH="${GH_KIT_WIKI_PATH:-}"
if [ -z "${WIKI_PATH}" ]; then
  echo "ERROR: GH_KIT_WIKI_PATH が未設定" >&2
  exit 1
fi
if [ ! -d "${WIKI_PATH}/.git" ]; then
  echo "ERROR: ${WIKI_PATH} は git リポジトリではない" >&2
  exit 1
fi
if [ ! -f "${BODY_FILE}" ]; then
  echo "ERROR: 本文ファイルが存在しない: ${BODY_FILE}" >&2
  exit 1
fi

case "${PAGE_NAME}" in
  */*) echo "ERROR: ページ名にスラッシュは使えない: ${PAGE_NAME}" >&2; exit 1 ;;
esac
case "${PAGE_NAME}" in
  *.md) ;;
  *) PAGE_NAME="${PAGE_NAME}.md" ;;
esac

DEST="${WIKI_PATH}/${PAGE_NAME}"
if [ -e "${DEST}" ]; then
  echo "ERROR: 既存ページがある: ${DEST}（更新は wiki-sync 経由）" >&2
  exit 2
fi

cp "${BODY_FILE}" "${DEST}"
echo "[wiki-create] wrote ${DEST}"

cd "${WIKI_PATH}"
git add -- "${PAGE_NAME}"
if git diff --cached --quiet; then
  echo "[wiki-create] no changes"
  exit 0
fi
git commit -m "wiki: ${PAGE_NAME%.md} を作成"
git push
echo "[wiki-create] pushed"
