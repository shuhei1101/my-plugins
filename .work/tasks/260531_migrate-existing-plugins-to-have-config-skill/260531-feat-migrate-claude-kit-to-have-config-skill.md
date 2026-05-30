# feat/migrate-claude-kit-to-have-config-skill

> 内部 ID: 231（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`plugin-config.md` の規約（PR175）により、ユーザー向け env トグルを持つプラグインには config スキルを追加することが義務付けられている。

`claude-kit` には以下のユーザー向け env 変数がある:
- `CLAUDE_KIT_JP_MIRROR` — JP ミラー作成の ON/OFF（デフォルト ON）
- `CLAUDE_KIT_INJECTION_LANG` — 注入リファレンスの言語（`en` / `jp`、デフォルト `en`）
- `CLAUDE_KIT_INJECTION_TTL` — 注入 TTL（整数・秒、デフォルト 3600）
- `CLAUDE_KIT_INJECTION_DISABLE` — マスターキルスイッチ（逆極性のため config スキル対象外）

このブランチでは `claude-kit:config` スキルを新規追加し、ユーザーが JSON を直接編集せずにトグルを変更できるようにする。
`INJECTION_TTL` は整数入力が必要なため、通常の ON/OFF トグルとは異なる扱いとする。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | - | QA を `## QA` に記録する |
| 2 | - | `.work/notes/` のノートを更新する |
| 3 | - | `claude-kit:config` スキルを新規作成（SKILL.md + SKILL.jp.md） |
| 4 | - | claude-kit バージョンバンプ + changelog |
| 5 | - | ルール / CLAUDE.md を更新する |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/claude-kit/skills/config/SKILL.md` | 新規 | claude-kit の env トグルをインタラクティブに設定するスキル | JP_MIRROR / INJECTION_LANG / TTL |
| 2 | `plugins/claude-kit/skills/config/SKILL.jp.md` | 新規 | 〃 の日本語ミラー | - |
| 3 | `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | バージョンバンプ | - |
| 4 | `plugins/claude-kit/CLAUDE.md` | 編集 | changelog に新バージョンエントリを追加 | - |
| 5 | `plugins/claude-kit/CLAUDE.jp.md` | 編集 | 〃 の日本語ミラーを同期 | - |
| 6 | `.claude-plugin/marketplace.json` | 編集 | claude-kit を新バージョンにバンプ | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | - | - | テスト変更なし | - |

## QA

### QA-001: INJECTION_TTL を config スキルに含めるか

**背景**: `INJECTION_TTL` は整数値（秒）であり、通常の ON/OFF トグルとは異なる入力形式が必要。`plugin-config.md` は「開発者向け内部設定のみのプラグインは config スキル不要」と述べており、TTL は開発者向けともいえる。

| # | 案 | 内容 |
|---|---|---|
| 1 | A | config スキルに含める（整数入力をプレーンテキストで受け付ける） |
| 2 | B | config スキルから除外し、手動 settings.json 編集にとどめる |

**推奨方式**: B — TTL は調整頻度が低く開発者向けの性質が強い。ON/OFF ループに整数入力を混在させると UX が複雑になる。config スキルは JP_MIRROR と INJECTION_LANG の 2 変数に絞る。

**状態**: 未解決

**決定したら反映先**: 作業内容 #3 の実装方針

### QA-002: INJECTION_LANG の選択肢（en/jp）を AskUserQuestion でどう表現するか

**背景**: `INJECTION_LANG` は ON/OFF トグルではなく `en`/`jp` の値選択。通常の「デフォルトに戻す / OFF」パターンは使えない。

| # | 案 | 内容 |
|---|---|---|
| 1 | A | Step 3 で INJECTION_LANG 専用の AskUserQuestion（`en` / `jp` / キー削除）を表示する |
| 2 | B | 他トグルと同一 Step 3 フローを維持し、値入力のみプレーンテキストで受け付ける |

**推奨方式**: A — AskUserQuestion で en/jp/キー削除の 3 択を表示するのが最も明快。Step 3 内で変数の種類を判定して分岐する。

**状態**: 未解決

**決定したら反映先**: 作業内容 #3 の実装方針

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-config.md`: config スキル設計ガイド
- `plugins/work/skills/config/SKILL.md`: 参照実装（work:config）
- `plugins/dev-kit/skills/config/SKILL.md`: 参照実装（dev-kit:config、opt-in/normal 両方式）
- `.work/notes/plugin-config-reference.md`: config スキル規約・設計判断メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | feat/migrate-existing-plugins-to-have-config-skill | dev-kit に config スキルを追加した先行ブランチ（PR229） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
