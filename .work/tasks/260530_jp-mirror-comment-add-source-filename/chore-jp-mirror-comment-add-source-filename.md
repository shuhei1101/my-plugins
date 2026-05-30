# chore/jp-mirror-comment-add-source-filename

> 内部 ID: 207（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`*.jp.md` 冒頭の JP ミラー警告コメントにソースの英語ファイル名を追加し、全ファイルに一括適用する。

**現在のフォーマット:**
```
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
```

**新フォーマット:**
```
<!-- This file is a Japanese mirror of {source_file.md}. When updating the English original, update this file too. -->
```

各 `foo.jp.md` に対してソースファイル名は `foo.md`（ベース名のみ、フルパスなし）。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - |
| 済 | `.work/notes/` の関連ノートを確認・更新する | - |
| 済 | 全 `*.jp.md` の旧形式コメントをソースファイル名入り新形式に一括置換する | `plugins/**/*.jp.md`（211ファイル） |
| 済 | コメント定義を参照するドキュメントを新形式に更新する | `references/common.md`, `common.jp.md`, `jp-mirror-translator.md`, `jp-mirror-translator.jp.md` |
| 済 | ルール・CLAUDE.md を更新する | - |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/**/*.jp.md` | 編集 | 旧形式コメント → 新形式コメント（ソースファイル名追加） | 211ファイル |
| `plugins/claude-kit/references/common.md` | 編集 | コメント記法の定義を新形式に更新 | - |
| `plugins/claude-kit/references/common.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/references/references-sync.md` | 編集 | コメント例・チェックリストを新形式に更新 | - |
| `plugins/claude-kit/references/references-sync.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/references/hooks.md` | 編集 | チェックリストを新形式に更新 | - |
| `plugins/claude-kit/references/hooks.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/references/claude-md.md` | 編集 | チェックリストを新形式に更新 | - |
| `plugins/claude-kit/references/claude-md.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/references/skills.md` | 編集 | チェックリストを新形式に更新 | - |
| `plugins/claude-kit/references/skills.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/agents/jp-mirror-translator.md` | 編集 | コメント例を新形式に更新 | - |
| `plugins/claude-kit/agents/jp-mirror-translator.jp.md` | 編集 | 同上の日本語ミラー | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| (テストなし) | - | - | - |

## QA

QA 事項なし。

## 参考ドキュメント

- `.work/notes/JPミラーポリシー.md`: JP ミラーポリシーのメモ

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| `feat/claude-kit-jp-mirror-env` | JP ミラー env var（PR201） |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| `claude-kit-markdown-env-var-audit` | 他の `.md` ファイルで「`echo $VAR`」等の誤った env var 確認指示がないか調査・修正 | 即時実施可 |
| `claude-kit-jinja2-authoring-rules` | `references/jinja2/` フォルダを作成し Jinja2 テンプレート作成時の注意事項をドキュメント化 | 即時実施可 |
