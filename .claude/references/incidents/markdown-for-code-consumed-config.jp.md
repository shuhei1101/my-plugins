<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# コードが parse する config を Markdown 化した（PR140）

## 何が起きたか

`plugins/py-kit/references/index.yaml` を再編成する過程で、AI は「ユーザーが直接眺める、Markdown のほうが見やすい」という理由で `index.md` / `index.jp.md`（Markdown テーブル）に変換した。フック `inject_references.py` は path → description を抽出するために Markdown テーブルの正規表現パーサーで書き直しになった。

ユーザーがレビューで即指摘：**「これ YAML にしとかなあかんでしょ / なんでマークダウンにした / Python の処理でさ注入できんやん」**。AI は撤回せざるを得なくなり、`index.yaml`（英語 description）+ `index.jp.yaml`（日本語ミラー）を復元、正規表現パーサーを削除、`yaml.safe_load` 直接 iterate に戻した。

## 根本原因

この変換は 2 つのニーズを混同していた:

- **人間の閲覧** 用に reference 一覧を見せる → Markdown テーブルは見栄えが良い
- **マシンの parse** で description を引く → YAML は信頼性◎、Markdown は壊れやすい

ファイルが両方を兼ねるとき、**YAML が勝つ** 理由:

- `yaml.safe_load` は 1 行。Markdown テーブルの正規表現は脆い（セパレータ行、エスケープされたパイプ、複数行セル）
- YAML はコメントが書ける、Markdown は書けない
- YAML を読む人間も path / description のペアリングは明確に読める

Markdown は **書式付きの散文** のためのフォーマット。**構造化データを目視確認** するためのものではない。

## 教訓

**ファイルがコードで parse されるなら、構造化フォーマット（YAML / JSON / TOML）で保持する。** Markdown 化は consumer が **人間だけ** の場合に限る。

「人間の可読性のために Markdown にしたい」という欲求が出たが、そのファイルがコードでも消費される場合:

1. データは YAML のまま保持
2. どうしても Markdown ビューが欲しいなら、YAML から生成する（Markdown を SoT として手書き保持しない）
3. オリジナルの YAML が単一の真実源として残る

## 関連

- PR140 で撤回（コミット bfe3f74）
- 同じ原則が適用される: `injection_rules.yaml`, `prompts/index.yaml`, フックが読むあらゆるカタログ
