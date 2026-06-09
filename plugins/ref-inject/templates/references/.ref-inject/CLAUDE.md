<!-- This file is a Japanese mirror of CLAUDE.md. When updating the English original, update this file too. -->

# __PLUGIN_NAME__ リファレンス

`__LOG_TAG__` フックが編集ファイルのパスに基づいてリファレンスドキュメントを自動インジェクトする。

## 手動で読む

- `_index.yaml` — 全リファレンスのリスト（パス + 1行説明; フックがパース）
- `_injection_rules.yaml` — 編集パスのパターン → `required` / `optional` リファレンスのマッピング

## 自動で読み込まれる

`PreToolUse(Edit | Write | MultiEdit | Read)` 時に `hooks/scripts/inject_references.py` が:

1. 編集ファイルのパスを `_injection_rules.yaml` のパターンにマッチさせる
2. マッチした `required` リファレンスを**本文全体**でインジェクト、`optional` は**パス + 説明のみ**でインジェクト
3. `~/.claude/tokens/__PLUGIN_NAME__/{session_id}.yaml` の二段階 TTL トークンで重複除去
   （`__ENV_PREFIX___INJECTION_TTL` 秒経過後に再インジェクト、デフォルト __DEFAULT_TTL__）:
   - `patterns`: マッチしたパターンは有効期間中はスキップ
   - `references`: 本文が既にセッション内でインジェクト済みの `required` リファレンスは（どのパターン経由でも）**パスのみ**表示し、複数パターンにまたがるリファレンスが二重インジェクトされない

`__ENV_PREFIX___INJECTION_LANG=jp` を設定すると日本語説明（`_index.jp.yaml` + `injection.jp.md.j2`）でインジェクトする。

## メンテナンス

- リファレンスを追加: ファイルを作成し、`_index.yaml`（と `_index.jp.yaml`）に追加し、`_injection_rules.yaml` のパターンにバインドする
- `1 リファレンス = 1 ユースケース` を維持し、単一の編集ファイルが無関係なドキュメントを引き込まないようにする
- `_injection_rules.yaml` を編集したら、孤立したリファレンス（インデックスに載っているがパターンにバインドされていない、またはその逆）がないか確認する
