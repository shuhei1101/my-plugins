# plugin-config スキル設計メモ — PR167

## 概要

PR164 で追加された env トグル群を、ユーザーが簡単に ON/OFF できるスキルを作成する。

## UX フロー（案）

1. `/plugin-config` を呼び出す
2. 現在の env 変数の状態を読み取り（settings.json の env ブロックを参照）
3. AskUserQuestion で各トグルの ON/OFF を選択肢で提示
4. 選択に基づき settings.json の env ブロックを更新

## 実装上の注意

- settings.json はユーザースコープ（`~/.claude/settings.json`）かプロジェクトスコープ（`.claude/settings.json`）かを選択させる
- env 未設定 = デフォルト有効のため、「ON（デフォルト）」の場合は env キーを削除する設計にする
- `INJECTION_DISABLE` のみ逆極性（truthy で無効化）— 表示ラベルを「注入を無効にする」にする

## 実装済み（PR167）

- `plugins/work-kit/skills/plugin-config/SKILL.md` — スキル定義
- `plugins/work-kit/skills/plugin-config/SKILL.jp.md` — JP ミラー
- work-kit v2.38.0 → v2.39.0 バンプ

## 参照

- `.work/notes/env-toggles-for-hooks-and-steps.md` — PR164 の env トグル実装メモ
