<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 新規 reference 追加後の orphan チェック漏れ（PR140）

## 何が起きたか

py-kit references を 38 → 43 ファイル、10 トピックフォルダに再構築。`injection_rules.yaml` は手書きで書いた。3 コミット目のあと、ユーザーが「ちゃんと全部のフォルダに紐づくようになっているか調べて」と質問。
簡単な YAML vs filesystem 差分スクリプトで **5 件の orphan**（`references/` 配下に存在するが、どの `rules[].pattern` からも参照されていない）が発覚:

- `scripts/python-script.md`
- `scripts/tkinter.md`
- `fastapi/health.md`
- `performance/cheatsheet.md`
- `architecture/refactoring-judgement.md`

これらは AI が:
- reference を作成した時に紐付けルールを書き忘れた
- 手動呼び出しのみと暗黙的に想定していた（`cheatsheet.md`、`tkinter.md` など）
- パスパターンを意識せず「補足説明用」として作った

## 根本原因

AI は reference を追加するだけで検証ステップを実行しなかった。38 個以上の reference と 20 個以上の rule を一気に扱うと、**両者間の silent drift はスクリプトでチェックしないと見えない**。

## 教訓

**`injection_rules.yaml` を編集したら必ず orphan 検出スクリプトを実行する。** 最小 Python（pyyaml 以外の依存なし）:

```python
import yaml, pathlib
refs_dir = pathlib.Path('plugins/py-kit/references')
rules = yaml.safe_load((refs_dir / 'injection_rules.yaml').read_text(encoding='utf-8'))['rules']

used = set()
for r in rules:
    for k in ('required', 'optional'):
        for p in r.get(k) or []:
            used.add(p)

existing = {
    md.relative_to(refs_dir).as_posix()
    for md in refs_dir.glob('**/*.md')
    if md.name not in ('CLAUDE.md', 'CLAUDE.jp.md')
    and not md.name.endswith('.jp.md')
}

orphans = sorted(existing - used)
unknowns = sorted(used - existing)
print('orphan:', orphans)
print('unknown:', unknowns)
```

実行タイミング:
- 新規 reference 作成時
- `injection_rules.yaml` 編集時
- references に触る PR をマージする前

パスパターンに本当に当てはまる場所がない reference（例: `performance/cheatsheet.md` — 手動のプロファイリング作業時にしか読まれない）は、`injection_rules.yaml` に YAML コメントで意図的例外を明示する **か**、ベストフィットなパターンを当てる（例: `**/benchmarks/**/*.py`）。

## 関連

- PR140 修正: コミット 2492991（5 パターン追加で orphan 吸収）
- `references/` + `injection_rules.yaml` を使う他プラグインにも同じパターンが適用される
