# インシデント — marketplace.json マージコンフリクトを sed で解消した結果 version 行が重複

## 何が起きたか

PR175 のマージ作業中、master を取り込んで `.claude-plugin/marketplace.json` に
バージョン衝突（claude-kit: 3.44.0 vs 3.43.2）が発生した。

これを次の sed で解消しようとした：

    sed -i '/<<<<<<< HEAD/,/=======/{ /<<<<<<< HEAD/d; /=======/d }; />>>>>>> master/d'

意図は「`<<<<<<< HEAD` から `=======` までの区切り行 2 本と `>>>>>>> master` 行を削除する」
だったが想定通り動かず、HEAD 側の version 行（3.44.0）と master 側の version 行
（3.43.2）が **両方残る** 結果になった：

    "version": "3.44.0"
    "version": "3.43.2"

JSON としては不正だが、後続のコミット時にも気づかず master に流れた（commit 82865846、14c2badb）。

## なぜ気づけなかったか

- sed 実行直後に cat で見たがバージョン行が 1 行に見えて OK と誤判定した（実際は 2 行）
- JSON 妥当性検証（json.load）をしなかった
- git diff --staged を確認せず staging に進めた
- Stop hook で人間が後から気付いてやっと判明（重複行が大量の未コミット差分の中に埋もれていた）

## 教訓（再発防止）

1. コンフリクトを sed や手動編集で解消したら、必ず妥当性検証を入れる
   - JSON: python -c "import json; json.load(open('path'))"
   - YAML: python -c "import yaml; yaml.safe_load(open('path'))"
2. git diff --staged を見てから commit する: マーカー残留 / 重複 / 想定外の削除がないか目視
3. コンフリクト解消は sed より Edit ツールを推奨: コンテキストつきで「old → new」の置換を書く方が誤動作しにくい
4. 作業ツリーに大量の未コミット差分があるときは要警戒: stash pop の残骸など、後から致命的な問題が混ざっている可能性

## 修正

PR220 (fix/marketplace-json-duplicate-version) で 21 行目を削除し、JSON 妥当性を検証して master にマージ。
