# PR182 — dev-kit-plugin-update-skill

## 概要

dev-kit プラグインに `plugin-update` スキルを追加する。

### 背景

PR168 で claude-kit の plugin authoring guide (`plugins/claude-kit/references/plugin-structure.md`) に「全プラグインは `plugin-update` 同等のスキルを必ず同梱する」という必須化を明文化した。workspace は PR168 で本体実装を済ませている。本 PR では同じ規約を dev-kit にも適用する。

### 何をするか

- `plugins/dev-kit/skills/plugin-update/SKILL.md` (+ `.jp.md`) を新規作成
- dev-kit がプロジェクトに展開する静的成果物（references / hooks 系テンプレ / 各言語の共通ルール用テンプレ等）を、現在インストール済みの dev-kit バージョンに合わせて更新するロジック
- workspace の `plugin-update` SKILL.md (`plugins/workspace/skills/plugin-update/SKILL.md`) を参考実装として参照する
- dev-kit の plugin.json と `.claude-plugin/marketplace.json` を MINOR bump、changelog 追加

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | dev-kit が展開する静的成果物を洗い出す | - dev-kit のソース全体 |
| 済 | `plugins/dev-kit/skills/plugin-update/SKILL.md` (+ jp) を作成（workspace 版を参考に） | - 新規 |
| 済 | dev-kit を MINOR bump (4.0.0 → 4.1.0) | - `plugins/dev-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | changelog を CLAUDE.md の `## Changelog` 表に追記 (PR171 で `changelogs/` 廃止のため) | - `plugins/dev-kit/CLAUDE.md`<br>- `plugins/dev-kit/CLAUDE.jp.md` |
| 済 | Skills 表に `plugin-update` 行を追加 | - `plugins/dev-kit/CLAUDE.md`<br>- `plugins/dev-kit/CLAUDE.jp.md` |
| 済 | コミット | - 70069d9 |
| 済 | レビュー指摘対応: dev-kit:plugin-update スキルから workspace 依存（`/workspace:work-start`, `/workspace:merge`, `.work/` 検出）を全削除し、master/main 拒否＋ユーザー責務コミット方式に書き換え | - `plugins/dev-kit/skills/plugin-update/SKILL.md`<br>- `plugins/dev-kit/skills/plugin-update/SKILL.jp.md` |
| 済 | claude-kit リファレンス `plugin-structure.md` (+ jp) の `plugin-update` 標準仕様表から workspace 依存記述を除去し「プラグイン間依存ゼロ」を明文化 | - `plugins/claude-kit/references/plugin-structure.md`<br>- `plugins/claude-kit/references/plugin-structure.jp.md` |
| 済 | claude-kit を PATCH bump (3.38.0 → 3.38.1) し Changelog 表を新設 | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json`<br>- `plugins/claude-kit/CLAUDE.md`<br>- `plugins/claude-kit/CLAUDE.jp.md` |
| 済 | dev-kit v4.1.0 の Changelog 記述を「自己完結設計」へ更新 | - `plugins/dev-kit/CLAUDE.md`<br>- `plugins/dev-kit/CLAUDE.jp.md` |
| 済 | 追加コミット | - a5bfda6 |
| 済 | 概念修正: plugin-update の本質を「静的ファイルのコピー」から「プロジェクト既存成果物が現行規約に逸脱していないかを検査・修正する」へ書き直し | - `plugins/dev-kit/skills/plugin-update/SKILL.md`<br>- `plugins/dev-kit/skills/plugin-update/SKILL.jp.md` |
| 済 | claude-kit `plugin-structure.md` (+ jp) の `plugin-update` 概念説明も同様に修正 | - `plugins/claude-kit/references/plugin-structure.md`<br>- `plugins/claude-kit/references/plugin-structure.jp.md` |
| 済 | PR184 / PR185 の事前仕様文書を正しい概念に合わせて更新 | - PR184 task doc<br>- PR185 task doc |
| 済 | コミット | - 915ff25 |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/dev-kit/skills/plugin-update/SKILL.md` | 新規 | dev-kit:plugin-update スキル本体（英語） | workspace 版を参考に dev-kit の同期対象（html-implement / html-debug-fab）に差し替え |
| `plugins/dev-kit/skills/plugin-update/SKILL.jp.md` | 新規 | JP ミラー | 先に jp を書いて英語版を生成 |
| `plugins/dev-kit/.claude-plugin/plugin.json` | 編集 | version 4.0.0 → 4.1.0 | MINOR bump（新スキル追加） |
| `.claude-plugin/marketplace.json` | 編集 | dev-kit エントリ version 4.0.0 → 4.1.0 | 3 箇所同期維持 |
| `plugins/dev-kit/CLAUDE.md` | 編集 | Skills 表に `plugin-update` 行追加 / `## Changelog` 表を新設し v4.1.0 + v4.0.0 を追記。v4.1.0 サマリに「自己完結設計」追記 | PR171 で `changelogs/` ディレクトリ廃止のため表形式に移行 |
| `plugins/dev-kit/CLAUDE.jp.md` | 編集 | 同上の日本語ミラー | - |
| `plugins/claude-kit/references/plugin-structure.md` | 編集 | `plugin-update` 標準仕様表から `/workspace:work-start` への依存記述を削除し、「master/main 拒否」「ブランチ管理しない」「プラグイン間依存なし」を仕様として明文化 | プラグイン間依存ゼロ化方針 |
| `plugins/claude-kit/references/plugin-structure.jp.md` | 編集 | 上記の日本語ミラー | - |
| `plugins/claude-kit/.claude-plugin/plugin.json` | 編集 | version 3.38.0 → 3.38.1 | PATCH bump（ドキュメント修正） |
| `.claude-plugin/marketplace.json` | 編集 | claude-kit エントリ version 3.38.0 → 3.38.1 | 3 箇所同期 |
| `plugins/claude-kit/CLAUDE.md` | 編集 | `## Changelog` 表を新設し v3.38.1 を記録 | claude-kit 初の Changelog 表 |
| `plugins/claude-kit/CLAUDE.jp.md` | 編集 | 上記の日本語ミラー | - |

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（ドッグフードで検証） | - |

## QA

特になし。

## 参考ドキュメント

- `plugins/workspace/skills/plugin-update/SKILL.md` — 参考実装
- `plugins/claude-kit/references/plugin-structure.md` — `## Required skills` セクションで規定

## 関連PR

| PR番号 | 概要 |
|---|---|
| #168 | plugin authoring guide に `plugin-update` 必須化を追加（本 PR の発端） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| dev-kit html ルールを静的ファイル配布から injection 方式に移行 | `html-implement` が `.claude/rules/` に静的コピーしている `css-js-link.md` / `common-component-first.md` を廃止し、ref-inject と同じ injection hook 方式に切り替える。具体的には: (1) 両ファイルを `references/html/` に移動、(2) `injection_rules.yaml` の既存 html パターン（`**/*.html|css|js`）に `required` として追記、(3) `templates/html/rules/` ディレクトリを削除、(4) `html-implement` SKILL のルールコピー手順を削除、(5) `plugin-update` SKILL のステップ2（ルールテンプレ再コピー）を削除、(6) dev-kit を MINOR bump。調査結果: `injection_rules.yaml` には既に `html/principles.md` が html パターンに紐付いており、同じ仕組みに乗るだけ。 | 即時実施可（PR182 マージ後） |
| claude-kit リファレンスに「プラグイン間依存ゼロ原則」を追記 | claude-kit の plugin authoring guide（`plugins/claude-kit/references/plugin-structure.md` + jp）に、**新規・既存どちらのプラグイン設計でもプラグイン間依存は極力ゼロにする**という原則セクションを追加する。`plugin-update` 仕様で既に「inter-plugin dependency: None」と書いたが、原則自体を独立セクションとして格上げし、`Why`／許容される例外（例: 同プラグイン内のスキル呼び出しは OK 等）／違反検出方法を明記する。| 即時実施可（PR182 マージ後） |
| 既存プラグイン間依存の棚卸とゼロ化対応 | `plugins/**/skills/**/SKILL.md` / `hooks/**` / `references/**` を全件 grep し、他プラグインのスキルやコマンドを呼び出している箇所をリストアップしてユーザーに提示する。レビュー後、可能なものから順次「プラグイン内自己完結」へ書き換え、最終的に依存件数ゼロを目標とする。例: workspace の skills 内に dev-kit/claude-kit への参照がないか、ref-inject の apply で他プラグインを操作していないか等を確認。 | 上記「プラグイン間依存ゼロ原則」PR のマージ後（原則を先に確立してから棚卸する方が判断軸が安定するため） |
