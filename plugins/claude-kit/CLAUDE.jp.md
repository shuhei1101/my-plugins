<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# claude-kit プラグイン開発者ガイド

## オーサリング知識は `references/` にあり、自動注入される

各指示ファイル種別のオーサリングガイドは `references/`（`common.md`, `skills.md`,
`rules.md`, `hooks.md`, `claude-md.md`, `plugin-structure.md`）にある。
`claude-kit-references-injection` フック（`hooks/scripts/inject_references.py`）が、対応するファイル
（`SKILL.md` / ルール / `CLAUDE.md` / `hooks.json` / `plugin.json` …）を編集したとき、該当ガイドを
**本文全量**で注入する。パス → reference の対応は `references/injection_rules.yaml` 参照。

- creator スキル（`skill-creator` / `rule-creator` / `hook-creator` / `claude-creator` /
  `plugin-creator`）は references に委譲する**薄いラッパー**。対象ファイルを直接編集すれば
  ガイドが注入される。ラッパーは明示起動と呼び出し元（例: `notes-to-claude`）のために残している。
- **Step 0 で他スキルを読み込まない** — スキルの起動時読み込みは 2500 × N トークンを消費する。
  注入機構が旧来の「Step 0: 背景資料を読む」パターンを置き換える。

この注入構造は全 `*-kit` プラグイン（py-kit / next-kit / claude-kit）で共通 — `kit-hooks-index-sync`
ルール参照。プラグインへの付与は `/ref-inject:apply <plugin>`。機構をプラグインごとに手編集しない
（`ref-inject` テンプレを変えて再適用する）。

## フック

claude-kit のフックは 1 つだけ: `claude-kit-references-injection` フック
（`hooks/scripts/inject_references.py`, `PreToolUse(Edit | Write | MultiEdit | Read)`）。
**ディスパッチ/チェック系ガードは無い** — リファレンス注入へ寄せて廃止した
（creator-dispatch は PR159、`j2-stamp-check` と PostToolUse の `jp-mirror-check` は PR161）。
JP ミラー同期はプロジェクトの `*-jp-mirror-sync` ルールで担保。

> 今後ガード系フックを戻すときの一般指針: `UserPromptSubmit`（ユーザー入力テキストしか見ない）でなく
> `PreToolUse` を使う。セッション単位フラグ（`/tmp/{hook}-{session_id}`）でセッション 1 回だけ発火させる。
> ロジックはインライン `-c` でなくスクリプトファイルに抽出する（インライン python はクォートのネストで
> 壊れやすい — incident `statusline-python-quote-nesting`）。フックスクリプトは `hooks/scripts/` 配下に置き、
> 共通ヘルパーは plugin 内 `_common.py` に集約する（PR180 で導入）。

## 環境変数

| 変数名 | 値 | デフォルト | 説明 |
|---|---|---|---|
| `CLAUDE_KIT_INJECTION_DISABLE` | `true`/`1`/`yes`/`on` | （未設定 = ON） | マスターキルスイッチ — truthy 値で注入機構全体を停止する |
| `CLAUDE_KIT_INJECTION_TTL` | 整数（秒） | `3600` | セッション単位注入トークンの TTL（patterns / references 共通） |
| `CLAUDE_KIT_INJECTION_LANG` | `en` / `jp` | `en` | 注入リファレンスの言語（`jp` で `index.jp.yaml` + `injection.jp.md.j2` を使用） |
