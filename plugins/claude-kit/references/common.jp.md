<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Claude 設定 共通ガイド

すべての creator スキルと `claude-refactor` のための共有リファレンス。
英語原本: `references/common.md`

種別ごとの詳細は、各専用リファレンスを参照:
- ルール: `references/rules.md`
- スキル: `references/skills.md`
- フック: `references/hooks.md`
- CLAUDE.md: `references/claude-md.md`

---

## ファイル種別の概要

| ファイル種別 | 読み込まれるタイミング | 何を書くか |
|---|---|---|
| `CLAUDE.md`（ルート） | セッション開始のたび — 常時 | プロジェクト全体の規約とワークフロー。**できる限り薄く保つ** |
| `CLAUDE.md`（サブフォルダ） | Claude がそのフォルダにアクセスしたとき | フォルダの説明とローカル規約（co-location を優先） |
| `.claude/rules/<name>.md` | `paths:` にマッチするファイルが読まれたとき | 複数パスを跨ぐリンクと更新漏れ防止 |
| `.claude/skills/<name>/SKILL.md` | 呼び出されたとき | 複数ステップのワークフローや手順 |
| `.claude/hooks/` + `settings.json` | 特定イベント時（自動） | 自動チェック・通知・プロンプト注入 |
| `.claude/references/<name>.md` | オンデマンド、Claude が必要としたとき | 毎セッションでは不要な詳細説明や参照資料 |

---

## ファイル種別の判定基準

| 内容の性質 | 最適なファイル種別 | 理由 |
|---|---|---|
| 複数の異なるフォルダを跨ぐファイル同期リンク | **rule** | 対象ファイルが編集されたときのみパスマッチで自動ロード |
| 単一フォルダ内のファイル一覧やローカル規約 | rule またはサブフォルダ CLAUDE.md | 可視性なら rule、co-location なら CLAUDE.md |
| プロジェクト全体で常に必要な短いワークフローや制約 | **CLAUDE.md（ルート）** | セッション開始時に常時ロード |
| ユーザー確認や分岐を伴う複数ステップのワークフロー | **skill** | オンデマンド呼び出し。コンテキストを汚さない |
| イベント起因で繰り返す自動チェックや通知 | **hook** | イベントで自動発火し、Claude のコンテキストに注入 |
| 1〜2 行の単純な指示や注意 | CLAUDE.md または rule | skill にするほど複雑ではない |
| ときどきしか必要としない参照資料や詳細説明 | `.claude/references/` | CLAUDE.md にはパスのみ記載し、オンデマンドでロード |

---

## 成果物の増殖防止ガード

**常時ロードされるコンテキストは、毎セッションや毎ファイル読み込み時にコンテキストウィンドウを消費する。**

- `CLAUDE.md`（ルート）は**毎**セッション開始時にロードされる
- 広い `paths:` パターンを持つルールは、マッチするファイルを開く**たびに**自動ロードされる

これらを増やすと、関連タスクだけでなくすべての作業でトークンを消費する。新しい成果物を作る前に、以下のチェックを適用すること:

### 新規成果物 vs 既存への統合 — 判定基準

| 問い | YES なら → |
|---|---|
| 既存のルールやスキルが既にこのドメインをカバーしているか？ | そこに統合する — 新規ファイルを作らない |
| その内容は毎セッション必要か、それとも特定タスク時のみか？ | ときどきだけなら → CLAUDE.md ではなく `.claude/references/` を使う |
| そのルールの `paths:` はプロジェクトのほぼ全ファイルにマッチするか？ | パターンを絞るか、CLAUDE.md に移す |
| これは一度きりの観察や一時的なメモか？ | 永続化しない |

### 増殖防止チェックリスト

- [ ] まず既存の成果物がこの内容を吸収できるか確認したか？
- [ ] CLAUDE.md への追加: これは本当に毎セッション必要か？
- [ ] ルール: `paths:` は可能な限り狭いか？
- [ ] `.claude/references/` に属すべき詳細専用の内容を CLAUDE.md に書いていないか？

---

## JP/EN ミラールール

すべてのファイルには対応する JP ミラーが必要:

| 英語ファイル（Claude が読む） | JP ミラー（人間の参照専用） |
|---|---|
| `.claude/rules/<name>.md` | `.claude/rules-jp/<name>.md` |
| `.claude/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.jp.md` |
| `CLAUDE.md`（任意のフォルダ） | 同じフォルダの `CLAUDE.jp.md` |
| `.claude/references/<name>.md` | `.claude/references/<name>.jp.md` |

**ワークフロー — まず JP ミラーを書き、次に英語原本を書く。** `.jp.md` を日本語で執筆し、
それから英語版を作る。このリポジトリでは英語原本が Claude が実際にロードするファイルなので、
両者が決して乖離してはならない。すべての JP ミラーは警告コメント
`<!-- This file is a Japanese mirror. ... -->` で始める必要がある（`provenance.md` 参照）。
フロントマターへの配置ルール: `dev-kit/references/markdown-editing.md` を参照。

> このリポジトリには `jp-mirror-translator` エージェント（`subagent_type: "claude-kit:jp-mirror-translator"`）が同梱されている:
> `.md` パスを渡すとその `.jp.md` を生成/更新し、`.jp.md` パスを渡すと英語原本を更新する。
> 両側を執筆する際に便利だが、手作業で書くことも同様に有効。
