<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# SKILL.jp.md — dev-kit:yaml（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: dev-kit:yaml
**トリガー**: `index.yaml`・`settings.yaml`・`settings.yaml.sample` の作成・編集時、
アセット/メディアファイルを YAML で管理する設計時、新しいプロジェクトでアセット管理の
仕組みを構築するときに自動適用される。

---

# dev-kit:yaml — YAML ファイル管理

アセットカタログとプロジェクト設定のための `index.yaml`・`settings.yaml`・`settings.yaml.sample`
を作成・管理する。規約は `{plugin_root}/references/yaml/yaml.md` に定義されている。

---

## タスク

### ステップ1: 規約を読み込む

共通 YAML 規約を読み込む：

```
{plugin_root}/references/yaml/yaml.md
```

プラグインルートはこのスキルファイルの2階層上（例：`Base directory: .../skills/yaml` → プラグインルートは `.../{plugin-name}/`）。

→ ステップ2へ

---

### ステップ2: YAML 操作を特定する

#### 処理

ユーザーが何を必要としているかを判断する：

| ユーザーの要求 | 移動先 |
|---|---|
| 新しいアセットを登録したい・存在するものを一覧管理したい | ステップ3（index.yaml） |
| 環境ごとの設定を作成・更新したい | ステップ4（settings.yaml.sample） |
| settings.yaml の gitignore 設定 | ステップ5（gitignore） |
| worktree プロジェクトでランタイム書き換え YAML を扱う | ステップ6（worktree 安全対策） |
| このドメインの YAML 規約を文書化する | ステップ7（ルールファイル） |

→ 適切なステップへ進む

---

### ステップ3: index.yaml を作成・更新する

#### 条件

ユーザーがある機能のアセットを登録またはカタログ管理したいとき。

#### 処理

1. `references/yaml/yaml.md`（index.yaml セクション）の規約に従って `{機能名}/index.yaml` にエントリを追加する。
2. 新しいアセットを追加した場合 → `index.yaml` にエントリを追加し、`settings.yaml.sample` にも対応するキーを追加する。
3. アセットを削除した場合 → `index.yaml` で非アクティブ化またはエントリを削除し、`settings.yaml.sample` からもキーを削除する。

→ 新しいキーが追加された場合はステップ4へ進む

---

### ステップ4: settings.yaml.sample を作成・更新する

#### 条件

index.yaml に新しいキーが追加された、または新しい設定項目が追加されたとき。

#### 処理

1. `{機能名}/settings.yaml.sample` に新しいキーをプレースホルダー値と短いインラインコメントで追加する。
2. `settings.yaml.sample` はリポジトリにコミットされる**テンプレート** — 各開発者がこのファイルを `settings.yaml` にコピーして自分の値を入力する。
3. `settings.yaml` 本体は**コミットしない** — gitignore 設定を確認する（ステップ5参照）。

→ gitignore がまだ設定されていない場合はステップ5へ、済んでいれば完了

---

### ステップ5: gitignore を設定する

#### 条件

`settings.yaml` がまだ `.gitignore` に登録されていないとき。

#### 処理

1. `.gitignore` に `settings.yaml` を追加する。
2. `settings.yaml.sample` が `.gitignore` に**含まれていない**ことを確認する — これはコミット対象。

→ 完了

---

### ステップ6: worktree でのランタイム書き換え YAML を安全に扱う

#### 条件

プロジェクトが git worktree を使用していて、かつ UI または API が実行時に YAML を書き換える場合
（例：`settings.yaml`・`runtime_state.yaml`）。

#### 処理

1. `references/yaml/yaml.md`（worktree でのランタイム書き換え YAML セクション）の対象表に照らして適用対象かを確認する。
2. `references/yaml/yaml.md` の2つの実現方法のどちらかを選ぶ：
   - **A. ファイルシステムレベル**：worktree セットアップで symlink / junction。
   - **B. アプリレベル**：`git rev-parse --git-common-dir` を使ったランタイムパス解決。
3. 採用方針を対応する `.claude/rules/<name>.md` に記録する（ステップ7参照）：
   - 解決方法（A or B）
   - 正本ファイルがどこに住むか
   - gitignore の有無

→ 完了

#### 注意事項

このルールを守らないと、worktree A で UI から設定保存 → worktree 側のみ更新 → worktree 削除で
保存内容が**消失**する。

---

### ステップ7: ルールファイルに規約を記録する

#### 条件

新しい機能がドメイン固有の管理規約を持つ YAML ファイルを導入するとき。

#### 処理

1. 関連する YAML ファイルを `paths:` frontmatter で指定した `.claude/rules/<機能名>.md` を作成する。
2. `references/yaml/yaml.md`（ルールファイルセクション）に従って以下を含める：
   - 各フィールドの意味
   - 更新手順（index.yaml vs settings.yaml.sample のどちらをいつ更新するか）
   - 対象の場合は runtime 解決方法（ステップ6より）
   - やってはいけないこと

→ 完了

#### 注意事項

##### 禁止事項

- ルールの内容を YAML ファイル内に複製しない
- YAML 冒頭に短いポインタコメント（1行）を置くのは OK — ただしルールの本文を YAML 内に書かない

---

## 参考資料

`{plugin_root}/references/yaml/yaml.md`：
- 3ファイル構成
- index.yaml の規約
- settings.yaml.sample の規約
- worktree でのランタイム書き換え YAML
- ルールファイル（.claude/rules/）
- 各ファイルの更新タイミング表
