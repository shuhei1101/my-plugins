<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# creator-skill-inline-duplication — creator スキルの判断基準インライン二重管理

## 何が起きたか

`rule-creator`・`skill-creator`・`hook-creator`・`claude-creator` の各スキルが
ファイルタイプ使い分けガイド（いつルールを使うか、いつスキルを使うかなど）を
それぞれの Step 0 の「要点」として inline で書いていた。

同時に `references/file-types.md` という外部参照ファイルも存在していたため、
同じ内容が5か所以上に分散して二重管理状態になっていた。

## 原因

PR68 でトークン効率改善のために「判定知識はスキル本体に埋め込む」方針を採用した。
しかし Step 0 で外部ファイルを読む設計も残ったため、
内側（inline）と外側（references/）の両方に同じ内容が書かれる状態になった。

## 修正内容（PR71）

1. `references/file-types.md` を削除し、目的別の5ファイルに分割:
   - `references/common.md` — 共通（判断基準・JP/EN ミラールール）
   - `references/rules.md` — ルール専用（2種類・ユースケース指向・フォルダ構成）
   - `references/skills.md` — スキル専用
   - `references/hooks.md` — フック専用（ループ防止含む）
   - `references/claude-md.md` — CLAUDE.md 専用（薄化原則）

2. 各 creator スキルの Step 0 inline「要点」を削除し、担当する references/ ファイルを読む1行に置き換えた

3. `claude-refactor` スキルを新設し、全 references/ ファイルを読んで横断監査を行う設計にした

## 再発防止

複数のスキルで共有すべき判断基準・ガイドラインは最初から `references/` に書く。
スキル本体には「どのファイルを読むか」だけ書き、内容は references/ に集約する。

- ✅ 1箇所のファイルを更新すれば全スキルに反映される
- ✅ 各スキルは自分に必要なファイルだけ読む（トークン効率）
- ❌ inline に書くと変更時に全スキルを個別更新する必要がある
