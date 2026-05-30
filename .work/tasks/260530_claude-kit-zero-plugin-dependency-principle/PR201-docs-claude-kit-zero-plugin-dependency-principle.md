# PR201 — claude-kit-zero-plugin-dependency-principle

## 概要

claude-kit の plugin authoring guide（`plugins/claude-kit/references/plugin-structure.md` + jp）に、
**全プラグイン設計でプラグイン間依存は極力ゼロにする**という独立原則セクションを追加する。

### 背景（PR182 から引き継ぎ）

PR182 で `plugin-update` 標準仕様表に "Inter-plugin dependency: None" を追加したが、
これは plugin-update 限定のルール扱い。実際にはユーザーは **新規・既存どちらのプラグイン設計でも**
プラグイン間依存をゼロに近付けたいと表明している。

そのため標準仕様表内の 1 行ではなく、`## Required skills` の手前あたりに **独立した原則セクション**
として格上げし、後続の棚卸 PR（PR202 予定）の判断軸として参照可能にする。

### 何をするか

`plugins/claude-kit/references/plugin-structure.md` および `.jp.md` に、以下の構成で
`## Zero inter-plugin dependency principle` セクションを新規追加する:

- **Why**: プラグインは独立した配布単位。他プラグインへの参照があるとインストール順依存・
  リネーム時の連動修正・並行 PR でのコンフリクト等が増える
- **許容される例外**:
  - 同プラグイン内の skill 同士の呼び出しは OK
  - ref-inject:apply による静的テンプレ展開（他プラグインに配布する設計が前提）は OK
  - claude-kit の references injection 機構（他プラグインがオプトインで取り込む）は OK
- **禁止される依存例**:
  - skill A の手順内で `/other-plugin:skill-B` を呼ぶ
  - hook が他プラグインのスクリプトファイルパスを直接参照する
  - reference が他プラグインのコマンドを「実行してから戻ってこい」と指示する
- **違反検出方法**:
  - `grep -rn "/[a-z-]\+:[a-z-]\+" plugins/*/skills/` 等で他プラグインスキル呼び出しを抽出
  - hook 設定で他プラグインの `${CLAUDE_PLUGIN_ROOT}` 以外のパス参照を確認

加えて claude-kit を PATCH bump し Changelog 表に行追加。

### 実施条件

即時実施可（PR182 マージ済）

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | jp 側で原則セクションのドラフトを書く | - `plugins/claude-kit/references/plugin-structure.jp.md` |
| 済 | 英語版に翻訳して追加 | - `plugins/claude-kit/references/plugin-structure.md` |
| 済 | claude-kit を PATCH bump（3.43.1 → 3.43.2） | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| skip | CLAUDE.md の Changelog 表に追記（既存表が無いので skip） | - 該当箇所 |
| 済 | コミット | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|

## テスト

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| - | - | テスト追加なし（ドキュメントのみ） | - |

## QA

特になし。

## 参考ドキュメント

- `plugins/claude-kit/references/plugin-structure.md` — 追記対象
- PR182（マージ済）の `plugin-update` 標準仕様表 — 既に "Inter-plugin dependency: None" を記載済（本 PR で原則として独立化）

## 関連PR

| PR番号 | 概要 |
|---|---|
| #182 | dev-kit:plugin-update スキル追加。plugin-update 標準仕様にプラグイン間依存ゼロを暗黙的に導入（本 PR の発端） |

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| existing-inter-plugin-dependency-audit-and-zero-out | `plugins/**/skills/**/SKILL.md` / `hooks/**` / `references/**` を全件 grep し、他プラグインのスキルやコマンドを呼び出している箇所をリストアップしてユーザーに提示する。レビュー後、可能なものから順次「プラグイン内自己完結」へ書き換え、最終的に依存件数ゼロを目標とする。例: work plugin の skills 内に dev-kit/claude-kit への参照がないか、ref-inject の apply で他プラグインを操作していないか等を確認。判断軸として PR201 で追記した原則セクションを参照する。 | 即時実施可（本 PR201 マージ後） |
