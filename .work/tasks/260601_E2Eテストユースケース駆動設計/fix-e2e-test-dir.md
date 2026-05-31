# fix/e2e-test-dir

> 内部 ID: 12（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`E2Eテスト.md` のディレクトリ構成を `e2e/` トップレベルから `tests/e2e/` に変更し、
`テスト戦略.md` / `フィクスチャー.md` / `ユニットテスト.md` と整合させる。
同時に `E2Eテスト.jp.md` JP ミラーを新規作成する。
`_injection_rules.yaml` のパターンは既に `tests/e2e/` ベースで正しいため変更不要。

`docs/e2e-usecase-driven-design`（ユースケース駆動設計への変更案）は不採用とし、
本ブランチで上書きする形で確定させる。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA を `## QA` に記録する（なし） | - |
| 済 | `E2Eテスト.md` を `tests/e2e/` ベースに書き換え・他ファイルと整合 | - `plugins/dev-kit/references/next/testing/E2Eテスト.md` |
| 済 | `E2Eテスト.jp.md` JP ミラーを新規作成 | - `plugins/dev-kit/references/next/testing/E2Eテスト.jp.md` |
| 済 | `_injection_rules.yaml` のフック条件を確認（変更不要） | - `plugins/dev-kit/references/.ref-injects/_injection_rules.yaml` |
| 済 | `_index.yaml` の description 修正・JP ミラーエントリ追加 | - `plugins/dev-kit/references/.ref-injects/_index.yaml` |
| 済 | `.work/notes/` のノートを更新 | - `.work/notes/コーディング規約・スタイル/E2Eテスト設計方針.md` |
| - | ルール / CLAUDE.md を更新 | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/dev-kit/references/next/testing/E2Eテスト.md` | 編集 | `e2e/` → `tests/e2e/` に統一、テスト戦略.md と整合 | - |
| `plugins/dev-kit/references/next/testing/E2Eテスト.jp.md` | 新規 | JP ミラー作成 | - |
| `plugins/dev-kit/references/.ref-injects/_index.yaml` | 編集 | description 修正・JP ミラーエントリ追加 | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| （テストファイルなし） | - | - | - |

## QA

（なし）

## 参考ドキュメント

- `.work/notes/コーディング規約・スタイル/E2Eテスト設計方針.md`: E2E テスト設計方針ノート

## 関連ブランチ

| ブランチ | 概要 |
|---|---|
| `docs/e2e-usecase-driven-design` | E2Eテスト.md のユースケース駆動設計案（本ブランチで上書き・不採用確定） |

## 次ブランチ候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| （なし） | - | - |
