# dev-kit フック設計メモ

## 概要

dev-kit プラグインに PreToolUse フックを追加し、Python/YAML ファイル編集時に
対応スキルを自動案内する。

## 実装済み (PR104)

| フック | トリガー | 動作 |
|---|---|---|
| python-skill-dispatch | Edit/Write で `.py` ファイル | セッション初回のみ py-project / py-script の概要を注入 |
| yaml-skill-dispatch | Edit/Write で `.yaml`/`.yml` ファイル | セッション初回のみ dev-kit:yaml を案内 |

## 設計判断

- **スキル判定**: フックは判断せず、両スキルの概要を提示して AI が選択
- **注入頻度**: セッション単位フラグ（`/tmp/dev-kit-{py|yaml}-skill-{session_id}`）で初回のみ
- **実装方式**: hooks.json インライン (`-c`) — 外部スクリプトファイルなし
- **出力パターン**: 直接コンテンツ埋め込み方式（PR115/PR119 で "Read and follow" 1行参照パターンから変更）

## フックロジック（概要）

```
stdin の file_path が対象拡張子 → セッションフラグ確認
  フラグなし → touch + "Read and follow: /path/to/prompt.md" を block で返す
  フラグあり → exit 0（素通り）
```

## 関連ファイル

- `plugins/dev-kit/hooks/hooks.json`
- `plugins/dev-kit/hooks/prompts/python-skill-dispatch.md`
- `plugins/dev-kit/hooks/prompts/yaml-skill-dispatch.md`
- `plugins/dev-kit/changelogs/v2.1.0.md`
