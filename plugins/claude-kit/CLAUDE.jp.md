<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# claude-kit プラグイン開発者ガイド

## オーサリング知識は `references/` にあり、自動注入される

各指示ファイル種別のオーサリングガイドは `references/`（`common.md`, `skills.md`,
`rules.md`, `hooks.md`, `claude-md.md`, `plugin-structure.md`、加えて `glossary.md` / `incidents.md`）に
ある。`claude-kit-references-injection` フック（`hooks/inject_references.py`）が、対応するファイル
（`SKILL.md` / ルール / `CLAUDE.md` / `hooks.json` / `plugin.json` …）を編集したとき、該当ガイドを
**本文全量**で注入する。パス → reference の対応は `references/_injection_rules.yaml` 参照。

- creator スキル（`skill-creator` / `rule-creator` / `hook-creator` / `claude-creator` /
  `plugin-creator`）は references に委譲する**薄いラッパー**。対象ファイルを直接編集すれば
  ガイドが注入される。ラッパーは明示起動と呼び出し元（`conversation-to-claude`,
  `notes-to-claude`）のために残している。
- **Step 0 で他スキルを読み込まない** — スキルの起動時読み込みは 2500 × N トークンを消費する。
  注入機構が旧来の「Step 0: 背景資料を読む」パターンを置き換える。

この注入構造は全 `*-kit` プラグイン（dev-kit / claude-kit）で共通 — `kit-hooks-index-sync`
ルール参照。プラグインへの付与は `/ref-inject:apply <plugin>`。機構をプラグインごとに手編集しない
（`ref-inject` テンプレを変えて再適用する）。

## フック

claude-kit のフックは今や2つだけ: `claude-kit-references-injection` フック
（`hooks/inject_references.py`, `PreToolUse(Edit | Write | MultiEdit | Read)`）と `PreCompact` の
再注入リマインダ。**ディスパッチ/チェック系ガードは無い** — リファレンス注入へ寄せて廃止した
（creator-dispatch は PR159、`j2-stamp-check` と PostToolUse の `jp-mirror-check` は PR161）。
JP ミラー同期はプロジェクトの `*-jp-mirror-sync` ルールで担保。

> 今後ガード系フックを戻すときの一般指針: `UserPromptSubmit`（ユーザー入力テキストしか見ない）でなく
> `PreToolUse` を使う。セッション単位フラグ（`/tmp/{hook}-{session_id}`）でセッション 1 回だけ発火させる。
> ロジックはインライン `-c` でなくスクリプトファイルに抽出する（インライン python はクォートのネストで
> 壊れやすい — incident `statusline-python-quote-nesting`）。
