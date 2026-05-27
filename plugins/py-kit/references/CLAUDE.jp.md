<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# py-kit リファレンス — インデックス（日本語ミラー）

> このファイルは `CLAUDE.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `CLAUDE.md` にも反映してください。

py-kit の Python 規約は **トピック軸に分割された複数の reference ファイル** で構成されている。
編集対象に応じて必要なものだけ読めるように、次の 2 ファイルで管理:

| ファイル | 役割 |
|---|---|
| **`index.yaml`** (英語) / **`index.jp.yaml`** (日本語) | reference 一覧 + 1 行 description。注入時の description は英語版を使う（フックが parse する）。日本語版は人間が一覧確認するためのもの |
| **`injection_rules.yaml`** | 編集対象ファイルパスのパターン → 必読 / 任意 reference のマッピング（言語非依存） |

---

## 読み方（手動の場合）

1. **`index.yaml`（または `index.jp.yaml`）** を読んで、各 reference の概要を把握
2. 編集対象ファイルのパスを **`injection_rules.yaml`** の `rules[].pattern` と照合
   - 例: `src/{pkg}/features/chat/service.py` を編集する → `**/*.py` と `**/features/**/service.py` がマッチ
3. マッチしたルールの `required` を全部、`optional` から関連するものを必要に応じて読む

---

## 読み方（自動の場合）

**`refs-inject-kit` プラグイン**（同 PR で新設）が `Edit` / `Write` / `MultiEdit` のたびに自動で:

1. インストール済みプラグインから `references/injection_rules.yaml` を持つものを自動検出
2. 各プラグインの `injection_rules.yaml` を読んで該当 rule を集める
3. 各プラグインの `index.yaml` から各 reference の description を引く
4. 各 reference 本文を読む
5. Jinja2 テンプレ (`refs-inject-kit/hooks/templates/injection.md.j2`) で整形
6. `decision: block` の reason に注入

セッション + ファイルハッシュ単位のトークンで、同一ファイルへの 2 回目以降はスキップ。

注入言語の切替は環境変数 `REFS_INJECT_KIT_LANG=jp` で（デフォルトは `en`）。

---

## SKILL からの呼び出し

`py-kit:py-project` / `py-kit:py-script` 各スキルの Step 1 は、まずこの `index.yaml` を最初に読む。
スキル固有のシナリオ（例: `py-script` なら `scripts/python-script.md` を強制注入）は
SKILL.md 側に書く。

---

## メンテナンス

- 新規 reference を追加したら **`index.yaml` + `index.jp.yaml` + `injection_rules.yaml`** の 3 ファイルを必ず更新する
- ファイル削除 / リネーム時も同様
- `references/CLAUDE.md` には、原則として「2 ファイルの役割を読め」以外の情報を書かない
  （個別 reference の説明は `index.yaml` のテーブルに集約）
