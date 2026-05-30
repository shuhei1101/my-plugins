# refactor/references-dot-ref-injects

> 内部 ID: 224（index.yaml 採番用 — クロスリファレンス目的）

## 概要

各プラグイン（claude-kit / dev-kit / work / ref-inject テンプレート）の `references/` 配下にある
ref-inject 内部ファイル（`_index.yaml`, `_index.jp.yaml`, `_injection_rules.yaml`, `CLAUDE.md`, `CLAUDE.jp.md`）を
`references/.ref-injects/` サブディレクトリに移動する。
あわせて、新しく `references/_index.md`（人間向けの日本語インデックス）を各プラグインに追加する。
`inject_references.py` のパス解決も `.ref-injects/` に対応させる。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する | - |
| - | `.work/notes/` のノートを更新 | - |
| 済 | `inject_references.py` テンプレートの参照パスを `.ref-injects/` に変更 | `plugins/ref-inject/templates/hooks/scripts/inject_references.py` |
| 済 | 各プラグインの ref-inject 内部ファイルを `.ref-injects/` に移動 | `plugins/*/references/{_index*,_injection_rules*,CLAUDE*}` |
| 済 | 各プラグインに `references/_index.md` を新規作成（日本語インデックス） | `plugins/*/references/_index.md` |
| 済 | CLAUDE.md 内のパス参照を更新（`.ref-injects/` への移動を反映） | 各 `.ref-injects/CLAUDE.md` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/ref-inject/templates/hooks/scripts/inject_references.py` | 編集 | `_injection_rules.yaml` / `_index.yaml` の参照先を `.ref-injects/` に変更 | - |
| `plugins/claude-kit/hooks/scripts/inject_references.py` | 編集 | 同上 | - |
| `plugins/dev-kit/hooks/scripts/inject_references.py` | 編集 | 同上 | - |
| `plugins/work/hooks/scripts/inject_references.py` | 編集 | 同上 | - |
| `plugins/claude-kit/references/.ref-injects/_index.yaml` | 新規（移動） | 旧 `references/_index.yaml` | - |
| `plugins/claude-kit/references/.ref-injects/_index.jp.yaml` | 新規（移動） | 旧 `references/_index.jp.yaml` | - |
| `plugins/claude-kit/references/.ref-injects/_injection_rules.yaml` | 新規（移動） | パターンも `.ref-injects/` パスに更新 | - |
| `plugins/claude-kit/references/.ref-injects/CLAUDE.md` | 新規（移動） | パス参照を更新 | - |
| `plugins/claude-kit/references/.ref-injects/CLAUDE.jp.md` | 新規（移動） | - | - |
| `plugins/claude-kit/references/_index.md` | 新規 | 日本語インデックス（14 ファイル、4 カテゴリ） | - |
| `plugins/dev-kit/references/.ref-injects/_index.yaml` | 新規（移動） | - | - |
| `plugins/dev-kit/references/.ref-injects/_index.jp.yaml` | 新規（移動） | - | - |
| `plugins/dev-kit/references/.ref-injects/_injection_rules.yaml` | 新規（移動） | - | - |
| `plugins/dev-kit/references/_index.md` | 新規 | 日本語インデックス（HTML/Python/Next.js の大規模インデックス） | - |
| `plugins/work/references/.ref-injects/_index.yaml` | 新規（移動） | - | - |
| `plugins/work/references/.ref-injects/_index.jp.yaml` | 新規（移動） | - | - |
| `plugins/work/references/.ref-injects/_injection_rules.yaml` | 新規（移動） | - | - |
| `plugins/work/references/.ref-injects/CLAUDE.md` | 新規（移動） | パス参照を更新 | - |
| `plugins/work/references/.ref-injects/CLAUDE.jp.md` | 新規（移動） | - | - |
| `plugins/work/references/_index.md` | 新規 | 日本語インデックス（5 ファイル、2 カテゴリ） | - |
| `plugins/ref-inject/templates/references/.ref-injects/_index.yaml` | 新規（移動） | - | - |
| `plugins/ref-inject/templates/references/.ref-injects/_index.jp.yaml` | 新規（移動） | - | - |
| `plugins/ref-inject/templates/references/.ref-injects/_injection_rules.yaml` | 新規（移動） | - | - |
| `plugins/ref-inject/templates/references/.ref-injects/CLAUDE.md` | 新規（移動） | パス参照を更新 | - |
| `plugins/ref-inject/templates/references/.ref-injects/CLAUDE.jp.md` | 新規（移動） | - | - |
| `plugins/ref-inject/templates/references/_index.md` | 新規 | テンプレート用の最小構成インデックス | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト変更なし | - |

## QA

（QA なし）

## 参考ドキュメント

- `.work/notes/_index.md`: 新規 _index.md のスタイル参考

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| - | - |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
