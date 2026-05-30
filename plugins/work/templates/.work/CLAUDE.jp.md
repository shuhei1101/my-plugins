<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
> このファイルは `CLAUDE.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `CLAUDE.md` にも反映してください。

# .work/ — workspace タスク管理ディレクトリ

workspace プラグインが管理するタスク・PR ライフサイクルの作業場所。
Claude はここのファイルを読み書きして作業状態を追跡する。

---

## ディレクトリ構成

| パス | 役割 |
|---|---|
| `tasks/index.yaml` | PR 索引（`completed: false` = 進行中）。`last_id` フィールドで次の PR 番号を管理する |
| `tasks/index.archive.yaml` | アーカイブ済み（`completed: true`）の PR エントリ。`trim-index.py` で自動生成される |
| `tasks/{YYMMDD}_{title}/{branch-hyphenated}.md` | PR ごとに 1 つの Markdown ファイル — TODO・QA・変更内容まで全て 1 ドキュメントに統合 |
| `notes/{トピック名}.md` | 作業中の議事録・検討メモ（一時的、AI 自動読み込みなし） |

### tasks/

`tasks/index.yaml` が PR の一元管理場所。進行中の PR は `completed: false`、マージ済みは `completed: true`。
`last_id` フィールドが次の PR 番号の基準値。マージのたびに `trim-index.py` が完了済みエントリを `index.archive.yaml` へ移動し、`index.yaml` をアクティブな PR のみに保つ。
作業開始時は必ず index.yaml を読んで進行中の PR を確認する。

タスクごとにフォルダ（`{YYMMDD}_{title}/`）を切り、その中に **PR ごとに 1 つの Markdown ファイル** を置く。ファイル名は PR のブランチ名のスラッシュをハイフンに置換したもの（例: `PR168/refactor/refactor-task-doc-structure` → `PR168-refactor-refactor-task-doc-structure.md`）。

PR ドキュメントは「この PR が何をするか」の唯一の正本。実装開始前に作成し、作業を通じて常に最新に保つ。以下のセクションを含む:

- `## 概要` — 目的・背景（`### 実施条件` を含む）
- `## 作業内容` — 作業チェックリスト（完了した行は `完了` 列を `済` にする。マージ前に全行が `済` であることを確認する）
- `## 変更内容` — 追加・編集した実装ファイルの一覧（テストを除く）
- `## テスト` — 実装に伴って追加・編集したテストファイル
- `## QA` — この PR スコープの未解決事項（マージ前に解決し、決定内容は該当する仕様・ドキュメントに反映する）
- `## 参考ドキュメント` — 関連ノート・仕様へのリンク
- `## 関連イシュー` — この PR が解決する `.work/issues/` のエントリ（merge で自動クローズ）
- `## 関連PR` — 先行・後続・分割兄弟の PR
- `## 次PR候補` — `/work-kit:pr-handoff` で予約する後続 PR

### notes/

**立ち位置**: 議事録・検討メモレベルの一時的な作業ノート。Claude Code には**自動読み込みされない**ため、公式ドキュメントとして扱わない。

フラット構造（**サブフォルダ禁止**）。1 ノート 1 トピック。重複禁止（リンクで代替）。

**ライフサイクル**:
1. PR の検討・設計段階で自由にメモを書く（書き捨て OK）
2. 作業完了後、内容が有益なら `/work:notes-to-claude` で恒久的な知識に昇格させる
   - 再利用したい手順・依存関係 → ルール (`.claude/rules/`)
   - 全セッションで必要な規約・禁止事項 → `CLAUDE.md`
   - 詳細な参考資料 → `.claude/references/`
3. 昇格済みのノートは削除してよい

昇格しない内容（一時的な比較表・調査メモ・ボツ案など）は放置してかまわない。

---

## 規約

- `## 作業内容` テーブルで完了した行は `完了` 列を `済` にする
- notes を恒久知識に昇格させる場合は `/work:notes-to-claude` を使う
- 疑問点・未確定事項は PR ドキュメントの `## QA` セクションに追記する
- マージ前に作業内容テーブルの全行が `済` であることを確認する

---

## workspace スキル

| スキル | 用途 |
|---|---|
| `/work:setup` | `.work/` を初期化する（初回のみ） |
| `/work:start` | 新規タスクフォルダ・PR ドキュメント・index.yaml エントリを作成する |
| `/work:merge` | 作業内容チェック・マージ・index.yaml 更新・クリーンアップを実行する |
| `/work:pr-handoff` | PR ドキュメントの `## 次PR候補` を元に次の PR を work-start と同じ流れで予約し、背景情報を新 PR に記録する |
| `/work:notes-to-claude` | `notes/` の内容をルール・CLAUDE.md・references に昇格させる |
| `/work:plugin-update` | プロジェクトに既に存在するプラグイン生成物（`.work/` テンプレやその他プラグインの静的ファイル）を、現在インストール済みのプラグインバージョンに合わせて更新する |
