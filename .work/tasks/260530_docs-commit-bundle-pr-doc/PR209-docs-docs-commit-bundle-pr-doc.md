# PR209 — docs-commit-bundle-pr-doc

## 概要

`.work/` 配下の変更は実装コードのコミットとは別コミットにするという規約を、
ref-inject を使って `.work/**` 編集時にインジェクトされるリファレンスとして追加する。

合わせて `templates/.work/CLAUDE.md` の内容をリファレンスに移転し、テンプレートから削除する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `work-dot-work-dir.jp.md` を新規作成（JP ミラー） | - `plugins/work/references/work-dot-work-dir.jp.md` |
| 済 | `work-dot-work-dir.md` を新規作成（英語正本） | - `plugins/work/references/work-dot-work-dir.md` |
| 済 | `_index.yaml` / `_index.jp.yaml` にエントリを追加 | - `plugins/work/references/_index.yaml`<br>- `plugins/work/references/_index.jp.yaml` |
| 済 | `_injection_rules.yaml` に `.work/**` パターンを追加 | - `plugins/work/references/_injection_rules.yaml` |
| 済 | `templates/.work/CLAUDE.md` と `CLAUDE.jp.md` を削除 | - `plugins/work/templates/.work/CLAUDE.md`<br>- `plugins/work/templates/.work/CLAUDE.jp.md` |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/work/references/work-dot-work-dir.jp.md` | 新規 | `.work/` ディレクトリガイド（JP ミラー） | - |
| `plugins/work/references/work-dot-work-dir.md` | 新規 | `.work/` ディレクトリガイド（英語正本） | - |
| `plugins/work/references/_index.yaml` | 編集 | `work-dot-work-dir.md` エントリを追加 | - |
| `plugins/work/references/_index.jp.yaml` | 編集 | `work-dot-work-dir.md` エントリを追加（JP） | - |
| `plugins/work/references/_injection_rules.yaml` | 編集 | `.work/**` → `work-dot-work-dir.md` のルールを追加 | - |
| `plugins/work/templates/.work/CLAUDE.md` | 削除 | 内容をリファレンスに移転 | - |
| `plugins/work/templates/.work/CLAUDE.jp.md` | 削除 | 内容をリファレンスに移転 | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## QA

特になし

## 参考ドキュメント

## 関連イシュー

## 関連PR

| PR番号 | 概要 |
|---|---|

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
