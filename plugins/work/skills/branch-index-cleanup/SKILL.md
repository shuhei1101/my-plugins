---
name: work:branch-index-cleanup
description: 
disable-model-invocation: true
---

# branch-index-cleanup — 未登録ブランチの整理

ローカルブランチと `index.yaml` / `index.archive.yaml` を比較し、
未登録ブランチをインタラクティブに分類・整理する。

---

## タスク

### ステップ 1: 未登録ブランチの収集

1. ローカルブランチをすべて取得:

```bash
git branch --format='%(refname:short)'
```

2. 両方のインデックスファイルから登録済みのブランチ識別子を読む（各エントリは `id` と/または `{type}/{title}` マッチングの `title` を持つ）:

```bash
python -c "
import yaml
branches = set()
for path in ['.work/tasks/index.yaml', '.work/tasks/index.archive.yaml']:
    try:
        data = yaml.safe_load(open(path))
        for entry in (data.get('branches') or []):
            if entry.get('branch'): branches.add(str(entry['branch']))
    except: pass
print('BRANCHES:', ' '.join(sorted(branches)))
"
```

3. 各ブランチ（`master` / `main` を除く）について、登録済みかどうかを確認:
   - **新形式**: ブランチが `{type}/{title}` → `titles` と照合
   - **レガシー形式**: ブランチが `PR{N}/{type}/{title}` → `{N}` を抽出して `ids` と照合
   - どちらにも当てはまらないブランチは未登録として扱う
4. **未登録ブランチ** のリストを作成

未登録ブランチが 0 件なら以下を報告して終了:

> すべてのブランチが index.yaml / index.archive.yaml に登録済みです。整理は不要です。

---

### ステップ 2: 各ブランチを分類

1. 未登録ブランチを表形式で表示:

   | ブランチ | 推定 ID | 推定タイトル | 分類 |
   |---|---|---|---|
   | feat/some-feature | (なし) | feat/some-feature | ? |
   | PR42/feat/legacy   | 42     | feat/legacy        | ? |
   | ... | | | |

2. 各ブランチについて自動推定:
   - `id` — レガシー `PR{N}/` プレフィックスを持つ場合のみ存在
   - `title` — ブランチ名全体（新形式）または `{type}/{title}` 部分（レガシー形式）
   - `type` — type 部分（feat/fix/refactor/docs/chore/test）、存在しない場合はデフォルト `chore`

3. ユーザーに各ブランチを A / B / C のいずれかに割り当てるよう要求:

   > 各ブランチを以下のいずれかに分類してください:
   > - **A** — 完了済み・不要（削除のみ）
   > - **B** — 完了済み・記録したい（archive に追記 → 削除）
   > - **C** — 作業継続（index.yaml に追記）

4. B/C ブランチの推定メタデータを修正したい場合は、進める前に受け入れる

結果は分類マップ: `{ branch: { class: A|B|C, id, title, type, summary? } }`

---

### ステップ 3: 分類ごとに処置を実行

B → C → A の順で実行する。

**Class B — archive 追記 + 削除**:

各 B ブランチについて:
1. `.work/tasks/index.archive.yaml` にエントリ追記:

```bash
python -c "
import yaml, sys
path = '.work/tasks/index.archive.yaml'
try:
    data = yaml.safe_load(open(path)) or {}
except: data = {}
branches = data.get('branches') or []
branches.append({
    'branch': sys.argv[1],
    'title': sys.argv[2],
    'type': sys.argv[3],
    'summary': sys.argv[4] if sys.argv[4] else '',
    'task': sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] else '',
    'completed': True,
})
data['branches'] = branches
yaml.dump(data, open(path, 'w'), allow_unicode=True, default_flow_style=False)
" {branch} {title} {type} "{summary}" {task_dir}
```

2. ブランチを削除:

```bash
git branch -d {branch}   # 未マージの場合は -D を使う
```

**Class C — index.yaml に追記**:

```bash
python {PLUGIN_ROOT}/scripts/index-tool.py add .work/tasks/index.yaml \
  --branch "{branch}" \
  --title "{title}" \
  --type {type} \
  --summary "{summary}" \
  --task "{task_dir}"
```

**Class A — 削除のみ**:

```bash
git branch -d {branch}   # 未マージの場合は -D を使う
```

注記:
- `git branch -d` が失敗した場合（完全にマージされていない）、ユーザーに警告して強制削除（`-D`）を確認
- `{PLUGIN_ROOT}` はワークスペースプラグインルートパスを指す

---

### ステップ 4: 結果を報告

サマリーテーブルを出力:

| 分類 | 件数 | ブランチ |
|---|---|---|
| A（削除） | N | branch1, branch2 |
| B（archive → 削除） | N | branch3 |
| C（index 追記） | N | branch4 |

最終状態を確認:

```bash
git branch --format='%(refname:short)' | grep -v master | grep -v main
```
