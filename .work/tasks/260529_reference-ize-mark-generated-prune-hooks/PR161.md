# PR161 — reference-ize-mark-generated-prune-hooks

## 概要

PR159 で claude-kit の creator スキルを reference 自動注入へ移行した流れの続き。
「AI が呼び出すスキル/チェックは reference 注入や既存ルールに寄せて減らす」方針で、残りの AI 呼び出し系を整理する。

対象（ユーザー指示 / QA-001 解決後の確定スコープ = **claude-kit 単独**）:
1. **claude-refactor 薄化**: Step1 で references を読むのに Step2-A/4-B/5-A/6 で同じ判定基準表をインライン重複コピーしている。これを削って「Step1 で読んだ references を基準に判定」へ寄せる。ワークフロー骨格は維持（呼び出し型なので skill のまま）。
2. **mark-generated を provenance reference 化 + 薄ラッパー存置**（QA-001）: スタンプ書式の正本を `references/provenance.md`(+jp) に移す（書式テーブル・version の出どころ plugin.json・配置 frontmatter 直後・JP ミラー警告・`.json` スキップ）。フックが authoring ファイル編集時に provenance を注入。mark-generated スキルは**薄ラッパーとして残し**、provenance.md に従ってスタンプ文字列を返す（フック非発火のスクリプト生成物・非マッチ型のフォールバック用）。**claude-kit 自身**の Write/Edit 経路の呼び出し元（creator 5本/version-sync/common.md/skills.md/CLAUDE.md）からは明示呼び出しを除去。**work-kit/html-kit は無変更**。
3. **j2-stamp-check 削除**: `j2_stamp_check.py` + prompts + hooks.json エントリ。`.j2` の出自は provenance 注入（`**/*.j2` パターン）でカバー。
4. **jp-mirror-check 削除**: `jp_mirror_check.py`（PostToolUse）+ hooks.json エントリ + prompts。JP ミラー同期は既存 `*-jp-mirror-sync` ルール群が担保。

### 実施条件

即時実施可（PR159 マージ済み、QA-001 解決済み）。

### 関連PR

| PR番号 | 概要 |
|---|---|
| #159 | claude-kit を ref-inject へ移行（creator スキル → reference 注入）。本 PR はその続き |
| #156 | ref-inject プラグイン（注入の仕組み） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md の未決定事項（QA-001）を解消する | - `PR161/QA.md` |
| 済 | `references/provenance.md`(+jp) を作成（mark-generated の書式仕様を移管・自己完結化） | - `plugins/claude-kit/references/provenance.md` (+jp) |
| 済 | injection_rules / index に provenance を紐付け（全 authoring パターン + `**/*.j2`）。common.md の出自スタンプ節は provenance.md へ移し撤去 | - `plugins/claude-kit/references/injection_rules.yaml`, `index.yaml`(+jp), `common.md`(+jp) |
| 済 | mark-generated を薄ラッパー化（provenance.md に従ってスタンプ文字列を返す。フォールバック用に存置） | - `plugins/claude-kit/skills/mark-generated/SKILL.md` (+jp) |
| 済 | claude-kit 自身の Write/Edit 経路の呼び出し元から mark-generated 明示呼び出しを除去（provenance 注入に委譲） | - creator 5本(+jp)/skills.md(+jp)/CLAUDE.md(+jp)。version-sync は記述参照のみ（呼び出し無し）で据え置き |
| 済 | claude-refactor を薄化（インライン重複基準を削除し references 参照へ。407→約160行） | - `plugins/claude-kit/skills/claude-refactor/SKILL.md` (+jp) |
| 済 | j2-stamp-check フック削除 | - `plugins/claude-kit/hooks/j2_stamp_check.py`, `hooks/hooks.json`, `hooks/prompts/j2-stamp-check.{md,jp.md}` |
| 済 | jp-mirror-check フック削除 | - `plugins/claude-kit/hooks/jp_mirror_check.py`, `hooks/hooks.json`, `hooks/prompts/jp-mirror-check.{md,jp.md}` |
| 済 | claude-kit 版バンプ(3.31.0) + marketplace 同期 + changelog | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `changelogs/v3.31.0.md` |
| 済 | `.work/notes/ref-inject-generator.md` に結論を追記 | - `.work/notes/ref-inject-generator.md` |
| 済 | ルール・glossary・CLAUDE.md を整備（mark-generated 薄ラッパー化 / フック2件削除を反映） | - `.claude/rules/core/glossary.md`(+rules-jp), `plugins/claude-kit/CLAUDE.md`(+jp) |
| 済 | 検証（orphan/構文/JSON/フックスモークテスト） | - |

## 参考ドキュメント

- `.work/notes/ref-inject-generator.md`（PR156/157/159）: ref-inject 設計メモ
- `plugins/claude-kit/references/common.md`: 現状の出自スタンプ手順（provenance.md へ移す元）
- `.claude/rules/feature/claude-kit-skill-dependencies.md`: creator/claude-refactor の references 依存ルール

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {実装中に判明した課題があれば追記} | - | - |

## QA

なし
