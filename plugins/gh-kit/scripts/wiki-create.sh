#!/usr/bin/env bash
# wiki-create.sh — GitHub Wiki ローカルリポジトリに 1 ページ作成して push する。
#
# 使い方:
#   GH_KIT_WIKI_PATH=/path/to/repo.wiki \
#     bash wiki-create.sh --page-name {カテゴリ}-{対象}.md --body-file /tmp/body.md \
#       [--category "カテゴリ名"] [--category-level 2|3]
#
# --category を指定すると _Sidebar.md の該当カテゴリセクション末尾にリンクを挿入する。
# カテゴリが存在しない場合は新規セクションを末尾に追加する。
# カテゴリ挿入後に Home.md を _Sidebar.md の内容に連動して自動更新する。
# --category-level: カテゴリ見出しレベル（2=##, 3=###）デフォルトは 2。
#
# 既存ファイルがある場合は上書きせず exit 2 で停止する（更新は wiki-sync 経由）。

set -euo pipefail

PAGE_NAME=""
BODY_FILE=""
CATEGORY=""
CATEGORY_LEVEL="2"

while [ $# -gt 0 ]; do
  case "$1" in
    --page-name) PAGE_NAME="$2"; shift 2 ;;
    --body-file) BODY_FILE="$2"; shift 2 ;;
    --category) CATEGORY="$2"; shift 2 ;;
    --category-level) CATEGORY_LEVEL="$2"; shift 2 ;;
    *) echo "ERROR: 未知の引数: $1" >&2; exit 1 ;;
  esac
done

if [ -z "${PAGE_NAME}" ] || [ -z "${BODY_FILE}" ]; then
  echo "ERROR: --page-name と --body-file は必須" >&2
  exit 1
fi

case "${CATEGORY_LEVEL}" in
  2|3) ;;
  *) echo "ERROR: --category-level は 2 または 3 のみ有効" >&2; exit 1 ;;
esac

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

# _Sidebar.md および Home.md を更新する
if [ -n "${CATEGORY}" ]; then
  SIDEBAR="${WIKI_PATH}/_Sidebar.md"
  PAGE_BASE="${PAGE_NAME%.md}"
  # GitHub Wiki のリンク形式: [[表示名|ページ名]]
  LINK_LINE="- [[${PAGE_BASE}|${PAGE_BASE}]]"

  # カテゴリ見出しのプレフィックス（## or ###）
  HEADING_PREFIX=""
  if [ "${CATEGORY_LEVEL}" = "2" ]; then
    HEADING_PREFIX="##"
  else
    HEADING_PREFIX="###"
  fi
  HEADING_LINE="${HEADING_PREFIX} ${CATEGORY}"

  if [ -f "${SIDEBAR}" ]; then
    # カテゴリが既存かどうか確認
    if grep -qF "${HEADING_LINE}" "${SIDEBAR}"; then
      # 既存カテゴリの次の同レベル以上の見出し行の直前にリンクを挿入する
      python3 - "${SIDEBAR}" "${HEADING_LINE}" "${LINK_LINE}" << 'PYEOF'
import sys, re

sidebar_path = sys.argv[1]
heading_line = sys.argv[2]
link_line = sys.argv[3]

with open(sidebar_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 見出しレベルを判定
heading_level = len(re.match(r'^(#+)', heading_line).group(1))

insert_idx = None
in_section = False
for i, line in enumerate(lines):
    stripped = line.rstrip('\n')
    if stripped == heading_line:
        in_section = True
        continue
    if in_section:
        # 同レベル以上の見出しが来たらそこに挿入
        m = re.match(r'^(#+)\s', stripped)
        if m and len(m.group(1)) <= heading_level:
            insert_idx = i
            break
        # リンクが既に存在する場合はスキップ
        if stripped == link_line:
            print(f"[wiki-create] link already exists in sidebar: {link_line}")
            sys.exit(0)

if insert_idx is not None:
    # 次の見出し直前の空行をスキップして、その手前に挿入する
    actual_insert = insert_idx
    while actual_insert > 0 and lines[actual_insert - 1].strip() == '':
        actual_insert -= 1
    lines.insert(actual_insert, link_line + '\n')
else:
    # セクション末尾（ファイル末尾）に追記
    if lines and not lines[-1].endswith('\n'):
        lines.append('\n')
    lines.append(link_line + '\n')

with open(sidebar_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"[wiki-create] inserted link into existing category: {heading_line}")
PYEOF
    else
      # カテゴリが存在しない場合はファイル末尾に新規セクションを追加
      {
        echo ""
        echo "${HEADING_LINE}"
        echo ""
        echo "${LINK_LINE}"
      } >> "${SIDEBAR}"
      echo "[wiki-create] added new category section: ${HEADING_LINE}"
    fi
  else
    # _Sidebar.md が存在しない場合は新規作成
    {
      echo "# Sidebar"
      echo ""
      echo "${HEADING_LINE}"
      echo ""
      echo "${LINK_LINE}"
    } > "${SIDEBAR}"
    echo "[wiki-create] created new _Sidebar.md"
  fi

  # Home.md を _Sidebar.md の内容で更新する
  HOME="${WIKI_PATH}/Home.md"
  python3 - "${SIDEBAR}" "${HOME}" << 'PYEOF'
import sys, re

sidebar_path = sys.argv[1]
home_path = sys.argv[2]

with open(sidebar_path, 'r', encoding='utf-8') as f:
    sidebar_content = f.read()

# _Sidebar.md からカテゴリとリンク一覧を抽出してHome.md 用の目次を生成する
lines = sidebar_content.splitlines()
toc_lines = ['# Wiki Home', '', '## 目次', '']

i = 0
while i < len(lines):
    line = lines[i]
    # レベル2見出し (##) をカテゴリとして扱う
    m2 = re.match(r'^##\s+(.+)$', line)
    m3 = re.match(r'^###\s+(.+)$', line)
    if m2 and not m3:
        category = m2.group(1)
        # # Sidebar のような h1 は除外
        toc_lines.append(f'### {category}')
        toc_lines.append('')
    elif m3:
        category = m3.group(1)
        toc_lines.append(f'#### {category}')
        toc_lines.append('')
    elif line.startswith('- [['):
        toc_lines.append(line)
    i += 1

toc_lines.append('')
toc_lines.append('---')
toc_lines.append('*このページは `wiki-create.sh` により `_Sidebar.md` から自動生成されます。*')

with open(home_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(toc_lines) + '\n')

print(f"[wiki-create] updated Home.md from _Sidebar.md")
PYEOF
fi

cd "${WIKI_PATH}"
git add -- "${PAGE_NAME}"
[ -n "${CATEGORY}" ] && git add -- "_Sidebar.md" "Home.md" 2>/dev/null || true
if git diff --cached --quiet; then
  echo "[wiki-create] no changes"
  exit 0
fi
git commit -m "wiki: ${PAGE_NAME%.md} を作成"
git push
echo "[wiki-create] pushed"
