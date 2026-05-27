<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# py-kit リファレンス — インデックス（日本語ミラー）

> このファイルは `CLAUDE.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `CLAUDE.md` にも反映してください。

py-kit の Python 規約は **トピック軸に分割された複数の reference ファイル** で構成されている。
編集対象に応じて必要なものだけ読めるように、以下のファイルで管理:

| ファイル | 役割 |
|---|---|
| **`index.yaml`** (英語) / **`index.jp.yaml`** (日本語ミラー) | reference 一覧 + 1 行 description。refs-inject-kit フックが英語版を parse（`REFS_INJECT_KIT_LANG=jp` 時に日本語版） |

注入ルール（どの pattern にどの reference を当てるか）は **py-kit にはない**。
**`refs-inject-kit/injection_rules.yaml`** に集約され、py-kit reference は `${py-kit}/path/to/ref.md` プレースホルダ記法で参照される。

---

## 読み方（手動の場合）

1. **`index.yaml`** を読んで、各 reference の概要を把握
2. 編集対象ファイルパスに対する rules は `refs-inject-kit/injection_rules.yaml` を見る（`pattern` がマッチするもの）

---

## 読み方（自動の場合）

**`refs-inject-kit` プラグイン**（同 PR で新設）が `Edit` / `Write` / `MultiEdit` のたびに自動で:

1. 自プラグインの中央 `injection_rules.yaml` を読む
2. 編集対象を `rules[].pattern` と照合し、`${plugin-name}/path` の reference を集める
3. `${py-kit}` を py-kit のインストール先 `references/` ディレクトリに解決
4. py-kit の `index.yaml` から各 reference の description を引く
5. 各 reference 本文を読む
6. Jinja2 テンプレで整形し `decision: block` で注入

セッション + ファイルハッシュ単位のトークンで、同一ファイルへの 2 回目以降はスキップ。

注入言語の切替は環境変数 `REFS_INJECT_KIT_LANG=jp` で（デフォルトは `en`）。

---

## SKILL からの呼び出し

`py-kit:py-project` / `py-kit:py-script` 各スキルの Step 1 は、まずこの `index.yaml` を最初に読む。
スキル固有のシナリオ（例: `py-script` なら `scripts/python-script.md` を強制注入）は
SKILL.md 側に書く。

---

## メンテナンス

- 新規 reference を追加したら: py-kit 側で **`index.yaml`** と **`index.jp.yaml`** を更新し、**`refs-inject-kit/injection_rules.yaml` に `${py-kit}/...` で rule を追加** する
- ファイル削除 / リネーム時も同様
- `references/CLAUDE.md` には個別 reference の説明を書かない。`index.yaml` のテーブルに集約
