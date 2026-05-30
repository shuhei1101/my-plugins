<!-- This file is a Japanese mirror of yaml.md. When updating the English original, update this file too. -->
# YAML — dev-kit 共通リファレンス（日本語ミラー）

> このファイルは `yaml.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `yaml.md` にも反映してください。

アセットカタログとプロジェクト設定に使う YAML ファイルの規約。
`dev-kit:yaml` スキルが操作を実行し、このドキュメントが従うべきルールを定める。

---

## 3ファイル構成

物理ファイル（アセット・メディア等）はどのようなフォルダ構成に置いてもよい。
プログラムやAIはファイルパスをハードコードせず、必ず YAML 経由でファイルを参照する。

機能ごと：

```
{機能名}/
├── index.yaml           # アセットカタログ（コミット対象・環境共通）
├── settings.yaml        # ローカル設定（gitignored・開発者ごと）
└── settings.yaml.sample # テンプレート（コミット対象）
```

---

## index.yaml

- 値は**環境に依存しない** — すべての開発者・環境で共通
- 「何が存在するか」を記述するマニフェスト
- YAML はデータとして最小限に保つ — ルールや変更履歴のコメントブロックは書かない
- 冒頭の1行ポインタコメントは OK：
  ```yaml
  # 管理規約は .claude/rules/assets-{機能名}.md を参照
  ```

### 更新ルール

| イベント | アクション |
|---|---|
| 新しいアセット追加 | `index.yaml` にエントリを追加し、`settings.yaml.sample` にも対応するキーを追加 |
| アセット削除 | `index.yaml` で非アクティブ化または削除し、`settings.yaml.sample` からもキーを削除 |

---

## settings.yaml.sample（コミット対象のテンプレート）

- 各キーはプレースホルダー値と短いインラインコメントを付ける
- このファイルはコミットされる — 各開発者がコピーして `settings.yaml` を作り自分の値を入力する
- `settings.yaml` 本体は**コミットしない**（次節 gitignore 参照）

---

## gitignore

```
settings.yaml
```

`settings.yaml.sample` が `.gitignore` に**含まれていない**ことを確認する — テンプレートはコミット対象。

---

## worktree でのランタイム書き換え YAML

プロジェクトが git worktree を使用していて、かつ UI や API が実行時に YAML を書き換える場合
（例：`settings.yaml`、`runtime_state.yaml`）、そのファイルはすべての worktree から
メインリポジトリのコピーを参照するように解決しなければならない。
そうしないと、worktree を削除した瞬間に保存内容が**消失**する。

### 適用対象

| YAML | 対象? | 理由 |
|---|---|---|
| `settings.yaml` | ✅ | UI / 設定画面から書き換える |
| `mock_notes.yaml`・`runtime_state.yaml` 等 | ✅ | アプリが API 経由で書き込む |
| `index.yaml` | ❌ | 手で編集するカタログ — worktree ごとにコピーがある |
| `settings.yaml.sample` | ❌ | テンプレートでコミット対象 |

### 2つの実現方法

**A. ファイルシステムレベル（symlink / junction）**
worktree セットアップ時に `<worktree>/path/to/settings.yaml` を `<main-repo>/path/to/settings.yaml` へリンクする。
アプリは通常パスで読み書きし、リンクが透過的にメインへ向ける。symlink 不可の環境ではコピーへフォールバックする。

**B. アプリレベル（runtime path 解決）**
アプリ内で `main_repo_root()` のような helper を用意し、worktree から呼び出してもメインリポジトリのパスを返すようにする。
検出は `git rev-parse --git-common-dir` を使う：
- メインワークツリーでは `.git`（相対パス）が返る
- linked worktree では絶対パスでメインの `.git` ディレクトリが返る

アプリコード側で runtime-editable YAML のパスを必ず `main_repo_root() / "path/to/file.yaml"` のように組み立てる。

### ドキュメント化

採用方針は対応する `.claude/rules/<name>.md` に記録する：
- 解決方法（A: symlink / B: runtime helper のどちらか）
- 正本ファイルがどこに住むか（`<main-repo>/data/...` 等）
- gitignore の有無

---

## ルールファイル（.claude/rules/）

ドメイン固有の YAML 規約を持つ機能では、関連する YAML ファイルを `paths:` frontmatter で指定した
`.claude/rules/<機能名>.md` を作成する。ルールファイルは Claude が対象 YAML を読み込んだときに
自動でコンテキストに入るため、データファイルを膨らませずに背景把握ができる。

ルールファイルに含める内容：
- 各フィールドの意味
- 更新手順（index.yaml vs settings.yaml.sample のどちらをいつ更新するか）
- 対象の場合は runtime 解決方法
- やってはいけないこと

**ルールの内容を YAML ファイル内に複製してはいけない。** YAML 冒頭に短いポインタコメント（1行）を
置くのは OK — ただしルールの本文を YAML 内に書かない。

---

## 各ファイルの更新タイミング

| イベント | index.yaml | settings.yaml.sample | settings.yaml |
|---|---|---|---|
| 新しいアセット追加 | エントリ追加 | キーをプレースホルダーで追加 | キーをローカル値で追加 |
| アセット削除 | 非アクティブ化または削除 | キーを削除 | キーを削除 |
| 新しい設定項目追加 | — | キーとコメントを追加 | キーをローカル値で追加 |
| 構造変更 | 更新 | 更新 | 手動で更新 |
