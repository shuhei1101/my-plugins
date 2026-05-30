<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# インシデント: pr-handoff が同じ PR 番号で複数の候補を予約する

## 日時

2026-05-30

## 何が起きたか

`/work-kit:pr-handoff` が次の PR 候補を 2 つ予約する際、両方とも `index.yaml` で `id: 165` を取得してしまった。
結果として同じ ID を持つ 2 つのエントリが生成された:

```yaml
- id: 165
  title: PR165 — add-plugin-config-skill
  ...
- id: 165
  title: PR165 — remove-mark-generated
  ...
```

ユーザーが「PR165 を開始する」と指示したときに、2 つのワークツリー（`my-plugins-wt-PR165` と
`my-plugins-wt-PR165b`）が存在し、どちらを使うべきか不明確になった。

## 原因

`pr-handoff` は「即時実施可」の候補を順番に `/work-kit:work-start` で予約するが、
`index.yaml` は gitignore されており、ローカルのみで更新される。
2 つの work-start 呼び出しが間近に実行され、両方が `last_id: 164` を読み込むと、
両方とも `last_id: 165` を書き込むため、ID が重複する。

## 適用した修正

1. ブランチ `PR165/feat/add-plugin-config-skill` を `PR167/feat/add-plugin-config-skill` にリネーム
2. ワークツリーを `my-plugins-wt-PR165` から `my-plugins-wt-PR167` に移動
3. `index.yaml` を更新: `id: 165`（add-plugin-config-skill）を `id: 167` に変更、`last_id: 166` を `167` に変更
4. タスクフォルダ `PR165/` を `PR167/` にリネームし、TODO.md の見出しを更新

## 予防方法

`pr-handoff` 実行後に複数の候補が予約された場合、重複 ID がないことを確認する:

```bash
python -c "
import yaml
data = yaml.safe_load(open('.work/tasks/index.yaml'))
ids = [p['id'] for p in data.get('prs', [])]
dupes = [i for i in ids if ids.count(i) > 1]
print('Duplicates:', dupes if dupes else 'none')
"
```

重複が見つかった場合、後で予約された PR を手動で `last_id + 1` に番号変更し、以下を更新する:
- `index.yaml` エントリ id とタイトル
- ブランチ名（`git branch -m`）
- ワークツリーパス（削除 + 再追加）
- タスクフォルダ（`PR{old}/` → `PR{new}/`）
- TODO.md の見出し

理想的には、`index-tool.py` の `add` コマンドを修正して `last_id` を書き込む前にアトミックに再読込するか、
pr-handoff の候補予約を遅延を入れて順次実行するようにする。
