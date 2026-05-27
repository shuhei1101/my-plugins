<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# SKILL.jp.md — refs-inject-kit:add-plugin（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: refs-inject-kit:add-plugin
**トリガー**: reference を持つプラグイン（`py-kit`、`next-kit` 等）を `refs-inject-kit` の中央
`injection_rules.yaml` に登録する。プラグインの利用可能な reference を
`references/index.yaml` から一覧表示し、ユーザーが rules を書くのを補助する。
「refs-inject-kit にプラグイン追加」「add-plugin」「{plugin-name} を refs-inject-kit に登録」など。

---

# refs-inject-kit:add-plugin — プラグインを登録する

`py-kit` / `next-kit` などの reference を持つプラグインを `refs-inject-kit` の中央
`injection_rules.yaml` に追加する。

スコープは **意図的に小さい**: プラグインの reference を一覧表示し、`enabled_plugins:` に
スタブを追加するだけ。具体的な rules はユーザーが（または同じチャットで AI 支援を受けて）
手書きで書く。スキルが自動生成することはしない。

---

## 作業内容

### ステップ1: プラグインを解決

#### 条件

- 常に最初に実行

#### 処理

1. `$ARGUMENTS` からプラグイン名を取得（例: `py-kit`）。なければユーザーに尋ねる
2. プラグインの `references/` ディレクトリを以下の順で解決:
   1. `${CLAUDE_PROJECT_DIR}/plugins/{plugin}/references/`（marketplace 開発時）
   2. `${HOME}/.claude/plugins/cache/*/{plugin}/*/references/`（インストール済み）
3. どちらも存在しなければ失敗を報告して終了

→ ステップ2へ

---

### ステップ2: プラグインの利用可能 reference を一覧表示

#### 条件

- ステップ1 完了

#### 処理

1. 解決した `references/index.yaml` を読む
2. `references[].path` を `description` 付きで番号付きリスト表示し、利用可能な reference を可視化

→ ステップ3へ

---

### ステップ3: `injection_rules.yaml` を更新

#### 条件

- ステップ2 完了

#### 処理

1. `${refs-inject-kit-root}/injection_rules.yaml` を読む
2. `enabled_plugins:` にプラグイン名を追加（既存なら何もしない）
3. `rules:` の末尾にコメント付きスタブを追記:

   ```yaml
     # ========== {plugin-name} ==========
     # ここにパスパターン → reference の rules を追加してください。
     # 例:
     #   - pattern: "**/*.py"
     #     required:
     #       - "${{plugin-name}}/core/naming.md"
   ```

4. ファイルを保存
5. メッセージ: 「`{plugin-name}` を enabled_plugins に追加し、rules セクションにスタブを挿入しました。`injection_rules.yaml` を編集して具体的な rules を追加してください — reference パスは `${{plugin-name}}/sub/path.md` 形式で書きます」

→ 完了

---

## 補足

### 禁止事項

- **rules を自動生成しない。** rules は「どの reference をどの pattern に当てるか」の判断が必要で、これは人間の判断（または同じ会話の AI 補助）で書く。スキルがやらない
- 同一プラグインの既存 rules を上書きしない。追記のみ

### 関連

- `${refs-inject-kit-root}/CLAUDE.md` — プラグイン全体ガイド
- `${refs-inject-kit-root}/injection_rules.yaml` — このスキルが編集するファイル
