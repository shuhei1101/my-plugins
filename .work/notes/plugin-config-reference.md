# plugin-config リファレンス設計メモ — PR175

## 概要

PR167 で確立した `work:config` スキルのパターンを、claude-kit の references/ に「設計ガイド」として文書化する。

## 実装方針

### hooks.json vs _injection_rules.yaml

当初仕様では「hooks/hooks.json に PreToolUse フックを追加する」と記載していたが、
既存の `inject_references.py` 機構を活用する方が一貫性があるため、
`_injection_rules.yaml` に `plugin-config.md` を optional 参照として追加する方式を採用した。

- SKILL.md 編集時: optional 注入（既存パターンに追加）
- plugin.json / marketplace.json 編集時: optional 注入（既存パターンに追加）

### 注入タイプ: optional（required ではなく）

- required にすると毎回フル本文が注入され、コンテキストを圧迫する
- optional は「パス + 説明のみ」が注入され、Claude が必要に応じて Read する
- ガイドとして「存在を知らせる」用途には optional が適切

## reference の内容

`references/plugin-config.md` に記載した主な内容:

1. なぜ config スキルが必要か
2. 管理トグルの規約（キーなし = ON / "false" = OFF）
3. 5 ステップの AskUserQuestion ループ構造
4. 最小 SKILL.md テンプレート
5. リリース前チェックリスト

## 参考実装

- `plugins/work/skills/config/SKILL.md` — work:config スキル（模範例）
- `.work/notes/plugin-config-skill.md` — PR167 の設計メモ（UX フロー詳細）

## Step 2 パターン変更（追記）

当初は Step 2 も AskUserQuestion を使う設計だったが、以下の理由で番号入力形式に変更：

- AskUserQuestion は 4 オプション上限があり、env トグルが多いプラグインでは制限になる
- 番号付きテキストリストなら全トグルを上限なしに表示できる
- 値・スコープの選択（Step 3）はバイナリ選択なので引き続き AskUserQuestion を使用

`work:config` スキル本体（参照実装）は旧パターンのまま。合わせる場合は別 PR で対応。

## 次PR候補

- `migrate-existing-plugins-to-have-config-skill`: py-kit / next-kit / html-kit に config スキルを追加
