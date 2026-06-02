# ISSUE-147: _index.yaml / _injection_rules.yaml が5ファイルの実在しないパスを参照している

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/references/.ref-inject/_index.yaml` と `_injection_rules.yaml` に登録されている 5 つのパスが、実際に存在するファイルと**ファイル名が食い違っている**。注入フックがこれらパスを解決しようとするとファイルが見つからず、注入が無声でスキップされる。

`_index.yaml` / `_injection_rules.yaml` に登録されているパス（左）と実際のファイル名（右）の対応：

| 登録パス（存在しない） | 実際のファイル名 |
|---|---|
| `python/architecture/依存パッケージ管理.md` | `python/architecture/依存関係管理.md` |
| `python/architecture/design-基本方針.md` | `python/architecture/設計原則.md` |
| `next/frontend/conventions/命名規則.md` | `next/frontend/conventions/命名規約.md` |
| `next/frontend/conventions/コメント.md` | `next/frontend/conventions/コメント規約.md` |
| `next/frontend/conventions/型定義.md` | `next/frontend/conventions/型規約.md` |

影響パターン（`_injection_rules.yaml`）:
- `**/main.py` → `依存パッケージ管理.md` + `design-基本方針.md`（両方 optional）
- `**/features/**/service.py` → `依存パッケージ管理.md` + `design-基本方針.md`
- `**/integrations/**/client.py` → `依存パッケージ管理.md`
- `**/*.{ts,tsx}` → `命名規則.md` + `コメント.md` + `型定義.md`（3 つとも optional）
- `**/app/(authenticated)/**/form.ts` → `型定義.md`

インシデント #2 (orphan-references-not-checked) の類型。

## 対応方針

`_index.yaml` / `_injection_rules.yaml` 内の誤ったパス 5 件を正しいファイル名に修正する（YAML 側を実ファイル名に合わせる）。`_index.md`（人間向けインデックス）も合わせて更新する。`_index.jp.yaml` でも同様のパスが登録されているため同時に修正する。

## 対象ファイル

- `plugins/dev-kit/references/.ref-inject/_index.yaml`: 5 件のパスを修正
- `plugins/dev-kit/references/.ref-inject/_index.jp.yaml`: 同 JP ミラー修正
- `plugins/dev-kit/references/.ref-inject/_injection_rules.yaml`: 5 件のパスを修正
- `plugins/dev-kit/references/_index.md`: リンク修正（該当箇所）

## QA

### QA-1: どの案で進めるか

A) YAML 側のパスを正しいファイル名に修正 / B) 実ファイルを YAML 登録名にリネーム

**推奨**: A — YAML だけ変更すれば済み、実ファイルの git 履歴を汚さない

**回答**: <!-- A / B -->

