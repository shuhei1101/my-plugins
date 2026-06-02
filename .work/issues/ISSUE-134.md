# ISSUE-134: dev-kit: injection_rules / _index.yaml に未バインドの孤立ファイルが 9 件（next backend・frontend・python/architecture）

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない / 様子見

## QA

### QA-1: どの案で進めるか

A) 各ファイルに対して適切な injection pattern を追加し _index.yaml にも登録する / B) 不要なファイルは削除し必要なものだけを登録する

**推奨**: A — ファイルはいずれも実体のある内容を持つ（最小 2195 bytes）ため、適切なパターンに紐づけることで有効活用できる

**回答**: A / B

---

## 概要

`plugins/dev-kit/references/` 配下に存在するが `_injection_rules.yaml` のどのパターンにも紐づいていない（かつ `_index.yaml` にも未登録または未バインドの）ファイルが 9 件ある。これらはどの編集操作でも注入されず、作成した目的が達成されない。

## 背景

インシデント `orphan-references-not-checked`（No.2）：`_injection_rules.yaml` 編集後は YAML とファイルシステムを突合する孤立チェックを実行し、紐づかない reference を残さないという規約がある。

## 現状

以下の 9 ファイルがディスクに存在するが、いずれのパターンにもバインドされていない:

| ファイル | サイズ | _index.yaml 登録 |
|---|---|---|
| `next/backend/リアルタイム.md` | 7217 bytes | ○ |
| `next/backend/ローカルYAML開発DB.md` | 14072 bytes | ○ |
| `next/frontend/Zustandパターン.md` | 2798 bytes | ○ |
| `next/frontend/appフォルダ概要.md` | 2195 bytes | ○ |
| `next/frontend/コンテキストパターン.md` | 2603 bytes | ○ |
| `next/frontend/ストリーミング.md` | 7001 bytes | ○ |
| `next/frontend/状態管理判断基準.md` | 2755 bytes | ○ |
| `python/architecture/依存関係管理.md` | 5612 bytes | × |
| `python/architecture/設計原則.md` | 3395 bytes | × |

`python/architecture/依存関係管理.md` と `設計原則.md` は `_index.yaml` にも未登録。前者は YAML に誤って旧名 `依存パッケージ管理.md` で参照されており別イシューとも連動している。

## 原因

新しいリファレンスファイルを追加した際、または既存ファイルをリネームした際に injection_rules への pattern 追加と _index.yaml 登録が漏れた。

## 期待される状態

全ファイルが少なくとも 1 つのパターンにバインドされ、`_index.yaml` にも登録されていること。または不要なファイルは削除されていること。

## 対応案

各ファイルの内容を確認し、どの編集ファイルパターンに対応する場面で注入されるべきかを判断して pattern を追加する。例:
- `next/backend/リアルタイム.md` → `**/server/ws/**/*.py` や websocket 関連パターン
- `python/architecture/依存関係管理.md` → YAML の旧参照 `python/architecture/依存パッケージ管理.md` を新名に書き換え（別イシュー参照）

## 横展開

`python/architecture/依存関係管理.md` と `設計原則.md` は別イシュー（python/architecture ファイル名変更）と連動している。先にそちらを対応することで一部が解決する。
