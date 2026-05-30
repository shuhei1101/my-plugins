# PR145 — update-ai-issue-discovery-notes-pr135

## 概要

`.work/notes/AIイシュー自動発見システム構想.md` を PR135 (review-next-kit-plugin) の成果に合わせて更新する。

**PR135 からの引き継ぎ背景**:

PR135 で next-kit references を「**1 ファイル = 1 ユースケース**」の 90 ファイルに全面再分割 (QA-073)、`hooks/inject_references.py` + `index.yaml` + `injection_rules.yaml` のフック自動注入構造を導入した (py-kit と同じ構造)。

これは「**AI イシュー自動発見**」構想の前提（リファレンスをフックで自動 inject する仕組み）の実装基盤になる。
notes を最新の構造で更新し、次の段階（自動イシュー発見の具体実装）に進めるようにする。

### 反映すべき主要事項

- next-kit references の 90 ファイル化 + ユースケース指向の設計原則
- next-kit のフック自動注入 (`next-references-injection`)、py-kit と構造同一
- `kit-hooks-index-sync` ルールで kit 間構造を強制同期する運用
- references 設計時のアンチパターン (「ベストプラ網羅型」の `bestprac-over-usecase-references-bloat` インシデント)

### 実施条件

即時実施可（PR135 がマージ済み）

### 関連PR

| PR番号 | 概要 |
|---|---|
| #135 | review-next-kit-plugin (本 PR の入力、references 全面再構築) |
| #140 | rebuild-py-kit-references (py-kit 側の同等の再構築、構造の祖) |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| ✅ | QA.md に未決定事項を記録する (もしあれば) | `.work/tasks/.../PR145/QA.md` |
| ✅ | `.work/notes/AIイシュー自動発見システム構想.md` を読み、現状記述を把握 | (参照) |
| ✅ | PR135 の成果 (90 ファイル分割、フック自動注入、kit-hooks-index-sync ルール) を反映 | `.work/notes/AIイシュー自動発見システム構想.md` |
| ✅ | references 設計原則 (1 ファイル = 1 ユースケース) を構想セクションに追記 | 同上 |
| ✅ | 関連インシデント (`bestprac-over-usecase-references-bloat`) を「学び」セクションに引用 | 同上 |
| ✅ | 次の段階（自動イシュー発見の具体実装）への入口を整理 | 同上 |

## 参考ドキュメント

- `.work/notes/AIイシュー自動発見システム構想.md`: 更新対象
- `plugins/next-kit/references/CLAUDE.md`: PR135 後の最新構造の入り口
- `.claude/references/incidents/bestprac-over-usecase-references-bloat.md`: 設計の教訓

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |

## QA

なし
