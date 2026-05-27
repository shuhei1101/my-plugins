<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# py-kit リファレンス — インデックス（日本語ミラー）

> このファイルは `CLAUDE.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `CLAUDE.md` にも反映してください。

py-kit の Python 規約は **トピック軸に分割された複数の reference ファイル** で構成されている。
編集対象に応じて必要なものだけ読めるように、メタデータと注入ルールを
`index.yaml` に集約してある。

---

## 最初に読むファイル

**`plugins/py-kit/references/index.yaml`**

このファイルには:
- 全 reference の `path` と 1 行の `description`
- 編集対象ファイルパスに対する `injection_rules`（star chart）

---

## 読み方（手動の場合）

1. **`index.yaml` を読む**
2. **編集対象ファイルのパスを `injection_rules` の `pattern` と照合**する
   - 例: `src/{pkg}/features/chat/service.py` を編集する → `**/*.py` と `**/features/**/service.py` がマッチ
3. **マッチしたルールの `required` を全部、`optional` から関連するものを必要に応じて読む**
4. 不足を感じたら `references` の `description` を見て、該当しそうなファイルを追加で読む

---

## 読み方（自動の場合）

次 PR `add-py-kit-references-injection-hook` で実装される **PreToolUse フック** が、
編集対象ファイルパスに対して `injection_rules` を自動で評価し、
`decision: block` で必要な reference を Claude へ注入する。

フック実装後は、ユーザーが `Edit` / `Write` を呼ぶたびに必要な reference が
自動的にコンテキストへ流れ込むので、Claude 側で `index.yaml` を都度読む必要はない。

---

## SKILL からの呼び出し

`py-kit:py-project` / `py-kit:py-script` 各スキルの Step 1 は、
このディレクトリの `index.yaml` を最初に読むよう指示する。
スキル固有のシナリオ（例: `py-script` なら `scripts/python-script.md` を強制注入）は
SKILL.md 側に書く。

---

## メンテナンス

- 新規 reference を追加したら `index.yaml` の `references:` と `injection_rules:` の両方を必ず更新する
- ファイル削除 / リネーム時も同様に `index.yaml` を更新する
- `references/CLAUDE.md` には、原則として「`index.yaml` を読め」以外の情報を書かない
  （個別 reference の説明は `index.yaml` の `description` に集約する）
