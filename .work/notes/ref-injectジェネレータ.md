---
created_at: 2026-05-29
updates:
  - 2026-05-29 — 初版（PR156 設計メモ）
  - 2026-05-29 — PR157: py-kit を移行。トークンフィールドを injected_at → expires_at に変更
  - 2026-05-29 — PR159: claude-kit を移行（creator スキル → reference 自動注入の拡張版）
  - 2026-05-29 — PR161: mark-generated を provenance.md 化（薄ラッパー存置）、claude-refactor 薄化、j2/jp-mirror チェックフック削除
  - 2026-05-30 — PR185: plugin-update スキルを追加（consumer 列挙 → フックファイル照合 → 更新）、1.5.0→1.6.0
  - 2026-05-31 — PR224: references/ 配下の内部ファイル（_index*/_injection_rules*/CLAUDE*）を references/.ref-injects/ に移動。各プラグインに人間向け日本語インデックス references/_index.md を追加
  - 2026-05-31 — #239: テンプレートとコンシューマーのドリフトを同期。TRUTHY 定数・キルスイッチ前置き（依存チェック前）をテンプレートに反映。_common.py コメントブロックをテンプレートに合わせて更新（全コンシューマー）
related_notes:
  - dev-kit-hooks.md
  - fix-read-hook.md
related_prs:
  - PR156
  - PR157
  - PR147
  - PR155
  - PR185
---

# ref-inject — リファレンス自動注入プラグインのジェネレータ

## 概要

py-kit / next-kit が手作業でコピペ共有していた「PreToolUse フックで編集対象パスに応じた reference を注入する仕組み」を、**雛形から展開して新プラグインを生成するジェネレータ** `ref-inject` に切り出す。共通ランタイムの共有（過去に却下された `refs-inject-kit` = `premature-cross-plugin-centralization`）ではなく、**独立コピーを吐き出すジェネレータ**である点が肝。インシデントが「コピペの方が安い」と言ったやり方を自動化する。

## 命名の経緯

- `*-kit` 命名から脱却（脳死で付けていたため）。
- `ref-inject`（creator 抜き）に決定。付与スキルは `/ref-inject:apply`（当初 `create` → 責務限定に伴い `apply` へリネーム）。

## 注入設計（生成される雛形に組み込む内容）

PR147 で「本文全量を毎操作で注入してコンテキストが膨らむ」問題から path+description のみに切り替えたが、トークンによる throttle が効くようになった今、**required は本文全量に戻す**。

| 項目 | 決定 |
|---|---|
| required | **本文全量**を注入 |
| optional | パス + description のみ（本文は AI が任意 Read） |
| TTL | デフォルト3600秒。env `{PLUGIN}_INJECTION_TTL`（秒）で上書き |
| 言語切替 | env `{PLUGIN}_INJECTION_LANG=jp`（維持） |

### トークン構造

`~/.claude/tokens/{plugin}/{session_id}.yaml` ── pattern をキーにした拡張可能 YAML マップ:

```yaml
# key = injection_rules の pattern（マッチしたパスglob）
# 値 = expires_at（注入時刻 + TTL の epoch 秒）
"src/**/route.ts":
  expires_at: 1716803600
"src/**/query.ts":
  expires_at: 1716803700
```

- 判定: 該当 pattern キーがあり `now < expires_at` ならスキップ / それ以外は注入して `expires_at = now + TTL` を書く。
- クリーンアップ: 発火のたびに全 `{session_id}.yaml` を走査し期限切れキー（`now >= expires_at`）を削除 → 空になったファイルごと削除（異常終了セッションも自然消滅）。
- 値を map にすることで将来フィールド追加（injected_count 等）が可能。
- 旧方式（pattern ハッシュごとの空ファイル乱立、自動削除なし）を置き換える。
- `injected_at` でなく `expires_at` を保存する（PR157 で変更）。判定が `now >= expires_at` で自明になる代わりに、TTL の env var 変更は既存エントリに遡及しない（注入時に期限が確定するため）。

### /compact について（PreCompact フックは持たない）

当初は `PreCompact` フックでセッショントークンを削除して即再注入する案だったが、**不要と判断して廃止**。
`/compact` で注入済み本文がコンテキストから消えても、トークンは TTL 経過で再注入されるだけで足りる。
そのためだけにフックを増やすのは無駄、という判断（PR156）。session-kit（PR155 で削除）の役割は TTL だけで代替する。

## ジェネレータの構成

```
plugins/ref-inject/
├── .claude-plugin/plugin.json
├── CLAUDE.md / CLAUDE.jp.md
├── skills/apply/SKILL.md (+jp)    # Claude がテンプレを読んで対象プラグインへ注入部分を書く手順
└── templates/                      # 対象プラグインにコピーする注入ファイル（注入部分のみ）
    ├── hooks/
    │   ├── inject_references.py     # 新注入設計（再利用される注入スクリプトのお手本）
    │   ├── hooks.json               # PreToolUse(Edit/Write/MultiEdit/Read)
    │   └── templates/injection.md.j2 (+jp)
    └── references/
        ├── _index.md                    # 人間向け日本語インデックス（PR224 で追加）
        ├── .ref-injects/                # ref-inject の内部ファイル（PR224 で集約）
        │   ├── _index.yaml (+jp) 雛形
        │   ├── _injection_rules.yaml 雛形
        │   └── CLAUDE.md (+jp) 雛形
        └── example/getting-started.md
```

**生成スクリプトは持たない**（当初 `scripts/generate.py` を作ったが、ユーザー判断で削除）。
apply スキルは、Claude が各テンプレートを `Read` → プレースホルダ（`__PLUGIN_NAME__` /
`__ENV_PREFIX__` / `__LOG_TAG__` / `__DEFAULT_TTL__`）を置換しながら対象プラグインへ `Write` する。
決定論的スクリプトよりこの方が構造がコンテキストに残り、プラグインごとに調整しやすい。
references 中身は雛形のまま利用者が埋める。

### なぜスクリプトをやめたか

ジェネレータをスクリプト化すると「ただのコピー」がブラックボックス化してコンテキストに残らない。
Claude が読みながら書く方式なら、生成過程そのものが会話に乗るため、その場で構造を理解・調整できる。
ユーザーが言っていた「スクリプト」は、`templates/hooks/inject_references.py`（各 kit で再利用する
注入スクリプトのお手本）を指していた。

### スキル名 create → apply、責務の限定

このスキルは「新規プラグインを作る」専用ではなく、**既存プラグインに注入部分を後付け**する
ケースもある。そのため名前を `create` → `apply` にリネーム。責務は**注入の仕組み（hooks +
references 雛形）だけ**に絞り、プラグインレベルの関心事（`plugin.json` / プラグインの
ルート `CLAUDE.md` / `marketplace.json`）は扱わない（それらは plugin-creator の領分）。
このため `templates/` から `plugin.json` と ルート `CLAUDE.md` 雛形を削除し、marketplace 登録
ステップも skill から外した。`__PLUGIN_DESCRIPTION__` プレースホルダも不要になり削除。

## スコープ

- PR156 = ref-inject 本体（apply スキル + 注入テンプレ）のみ。
- 次PR候補: py-kit（PR157 完了）/ next-kit（PR158 完了）/ claude-kit（PR159 完了）に `/ref-inject:apply` を適用して注入部分を統一。

## PR158: next-kit 移行

py-kit（PR157）に続き next-kit を ref-inject 注入形式へ移行（3.5.1→3.6.0）。
ref-inject テンプレートを `next-kit` / `NEXT_KIT` / `next-kit-references-injection` / `3600` で置換し、
`hooks/inject_references.py` と `hooks/templates/injection.{md,jp.md}.j2` を再生成。
結果は py-kit と完全一致（差分はプラグイン名のみ）。
- 旧トークン（パターンハッシュ空ファイル）→ pattern キーの YAML マップ（`expires_at` = 注入時刻 + TTL）
- 注入: required は本文全量 / optional は path + description のみ
- `hooks.json` は変更なし（PreToolUse はテンプレと同一、PostToolUse の `ts_check.py`(next-ts-check) はそのまま併設）
- references の実コンテンツ（index.yaml / injection_rules.yaml / 各本文）は保持。`references/CLAUDE.md`+jp の注入説明のみ更新。

## PR159: claude-kit 移行（拡張版）の結論

claude-kit は py-kit / next-kit のような「コーディング規約注入」プラグインではなく、**creator スキル群の本拠**。
当初は「creator-dispatch があるので ref-inject 不要」と評価したが、ユーザー判断で**方針を拡張**:

- creator スキル（skill / rule / hook / claude / plugin-creator）の**ステップ形式の手順を `references/` の自己完結ガイドに資料化**し、編集対象ファイルに応じて注入する。
- 旧 `creator_dispatch.py`（「creator スキルを使え」とブロック）の **creator 系ルールを廃止**し、ref-inject 注入で置換。非 creator 系の `j2-stamp-check` だけ `j2_stamp_check.py` に切り出して存置。
- creator スキルは**薄ラッパー化**して残す（明示起動 + 呼び出し元互換）。
- 出自スタンプ（mark-generated）は注入される `references/common.md` に明記し、直接編集フローでも担保。
- injection_rules: SKILL.md→skills.md / rule→rules.md / CLAUDE.md→claude-md.md / hooks.json・settings→hooks.md / plugin.json・marketplace→plugin-structure.md / glossary・incidents→各フォーマットガイド。common.md は creator 系パターンに required で同梱。
- claude-kit は `*-kit` グロブに一致するため `kit-hooks-index-sync` の対象に自動で含まれる（Overview に明記）。
- 注意: 既存の `jp_mirror_check.py`（PostToolUse）と `pre-compact.md`（PreCompact）は維持。inject_references.py は Edit/Write/MultiEdit/**Read** で発火（issue-scan 等の読み取り経路もカバー）。

## PR161: mark-generated の provenance 化 + フック削減（claude-kit 単独）

「AI がスキルを呼ぶのを減らし、フック注入や reference に寄せる」方針の続き。

- **出自スタンプの正本を `references/provenance.md`(+jp) に一本化**。書式テーブル・version 取得・配置・JP ミラー警告・`.json` スキップ・既存行置換を記載。`common.md` からスタンプ節は撤去（provenance.md へ移管）。
- **mark-generated は薄ラッパーとして存置**（廃止しない）。主経路は注入フックによる provenance.md 配信（Claude が Write/Edit する authoring ファイル）。フォールバックは薄ラッパー呼び出し（フック非発火 = work-kit の `setup-task.py` スクリプト生成物、html-kit debug-fab の `.js`/`.css`/`.html` 非マッチ型）。**判断の決め手**: フック注入は Write/Edit 経路でしか発火しない。スクリプト生成・非マッチ型は薄ラッパー経由が要るため完全削除しない。
- 結果、**work-kit / html-kit は無変更**（薄ラッパーをそのまま呼ぶ）。本 PR は claude-kit 単独で完結。
- injection_rules に `provenance.md` を全 stampable パターン（SKILL.md / rule / CLAUDE.md / prompts / glossary / incidents / `**/*.j2`）の required へ追加。JSON のみのパターン（hooks.json / settings / plugin / marketplace）は `.json` がコメント不可なので provenance を付けない。
- **claude-refactor 薄化**: Step ごとのインライン重複基準表を削除し references 参照へ（407→約160行）。実行ステップも「creator スキルを呼べ」→「直接編集（ガイドは注入される）」へ。
- **j2-stamp-check / jp-mirror-check フック削除**。claude-kit のフックは inject_references + PreCompact のみに。`.j2` 出自は注入で、JP ミラー同期は `*-jp-mirror-sync` ルールで担保。

## PR224: references/ 内部ファイルを .ref-injects/ に集約 + _index.md 追加

ref-inject の内部メカニズムファイルとユーザー authoring の reference 本文が `references/` 直下に
混在していたのを整理。

- **移動**: `references/` 直下の `_index.yaml` / `_index.jp.yaml` / `_injection_rules.yaml` /
  `CLAUDE.md` / `CLAUDE.jp.md` を `references/.ref-injects/` サブディレクトリに移動。
  reference 本文（`*.md`）は `references/` 直下に残す。
- **パス解決変更**: `inject_references.py` の `rules_yaml` / `index_yaml` 参照先を
  `refs_dir` から `refs_dir / ".ref-injects"` に変更。reference 本文の読み込み（`refs_dir / rel_path`）は
  従来どおり `references/` 基準なので不変。
- **_index.md 追加**: 各プラグインの `references/_index.md` に、配下の reference ファイルの
  概要とカテゴリを記した**人間向け日本語インデックス**を新規作成（`.work/notes/_index.md` と同じスタイル）。
  機械可読の `.ref-injects/_index.yaml`（フックが parse）とは別物。
- **適用範囲**: claude-kit / dev-kit / work の各 consumer プラグイン + ref-inject の `templates/references/` 雛形。
  さらに claude-kit の `_injection_rules.yaml` 内 kit 構造ファイルパターンを
  `plugins/*-kit/references/.ref-injects/{...}` に更新、移動先 CLAUDE.md 内のパス参照文も更新。
- **将来 apply するプラグイン**: テンプレート（`templates/references/.ref-injects/` + `templates/references/_index.md`）が
  この構造を持つため、`/ref-inject:apply` で自動的に新構造で展開される。
