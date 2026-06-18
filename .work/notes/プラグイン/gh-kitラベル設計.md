# gh-kit ラベル設計 — Issue/PR の状態を表すラベル一覧

## 概要

gh-kit プラグインは Issue と PR を GitHub のラベルで状態管理する。
状態遷移はラベルの付け外しで表現し、各スキル/エージェントは特定ラベルの付与・除去を排他制御兼マーカーとして使う。
**「ラベル」が真実のソース** — ローカルに状態ファイルは持たない。

ラベル名は `plugins/gh-kit/scripts/labels.sh` に集約。変更するときはここだけ書き換える。

## ラベル一覧（共通）

| No | ラベル | 意味 | 付与 | 外す |
|---|---|---|---|---|
| 1 | `processing` | 何らかの作業中（排他マーカー） | 各スキルが対象を拾った瞬間 | 完了/失敗時に必ず |
| 2 | `needs-ai-review` | AI レビュー必要。**Issue/PR 作成時に必ず付く** | AI が自動 | AI レビュー完了時 |
| 3 | `needs-user-review` | ユーザーレビュー必要。状況に応じて AI が判断 | AI が自動（判定基準は `templates/ユーザーレビュー要否判定.md`） | ユーザーが手動で外す |
| 4 | `needs-fix` | レビュー結果、修正必要 | AI/ユーザーがレビューで判断 | 修正完了後にレビューしたほうが外す |

## ラベル一覧（Issue 専用）

| No | ラベル | 意味 | 付与 | 外す |
|---|---|---|---|---|
| 1 | `ai-code-scan` | claude code がスキャンして起票（出自タグ） | `code-scanner` | 通常外さない |
| 2 | `type:{refactor,bug,feat,docs,chore,test}` | 種別 | `code-scanner` / ユーザー | 必要に応じて |
| 3 | `priority:{high,medium,low}` | 優先度 | `code-scanner` / ユーザー | 必要に応じて |

## ラベル一覧（PR 専用）

| No | ラベル | 意味 | 付与 | 外す |
|---|---|---|---|---|
| 1 | `wip` | Draft 雛形 PR | `pr-wip-create` | `pr-implement-auto` が実装に入るとき |

## 状態遷移図

### Issue

```mermaid
stateDiagram-v2
  [*] --> Open: gh issue create
  Open --> NeedsAIReview: needs-ai-review 自動付与（作成側が）
  NeedsAIReview --> Processing: /gh-kit:issue-review 取得時
  Processing --> NeedsUserReview: AI レビュー完了 (needs-ai-review 除去・必要なら needs-user-review 付与)
  NeedsUserReview --> Ready: ユーザー回答 → needs-user-review 除去
  Processing --> Ready: AI 判定で needs-user-review 不要だった場合 (即 ready)
  Ready --> PrWipCreating: /gh-kit:pr-wip-create が拾う (processing 付与)
  PrWipCreating --> Closed: PR がマージされて GitHub が自動 close
```

「Ready」= needs-* なし、open、質問にすべて回答済み。`/gh-kit:pr-wip-create` の対象。

### PR

```mermaid
stateDiagram-v2
  [*] --> Draft_wip: /gh-kit:pr-wip-create で wip 付与
  Draft_wip --> Processing: /gh-kit:pr-implement-auto 取得時 (processing 付与・wip 除去)
  Processing --> NeedsAIReview: 実装完了 (processing 除去・needs-ai-review 付与・必要なら needs-user-review・draft 解除)
  NeedsAIReview --> Reviewing: /gh-kit:pr-review-auto 取得時 (processing 付与)
  Reviewing --> Merged: approve → /work:merge → push (processing/needs-ai-review 除去 + needs-user-review なし)
  Reviewing --> NeedsFix: AI レビュー結果 修正必要 (processing 除去・needs-fix 付与)
  Reviewing --> NeedsUserReview_Only: AI OK だがユーザー判断必要 (processing/needs-ai-review 除去、needs-user-review は残す)
  NeedsFix --> Processing: 修正 push → 再 pr-implement-auto or 手動
  NeedsUserReview_Only --> Merged: ユーザーが needs-user-review 除去 → マージ実行
```

「マージ可能」= needs-* がすべて外れた + processing なし + draft でない + CI green。

## ライフサイクル詳細

### Issue 側

1. AI（`code-scanner`）または人間が Issue 作成
2. AI が `needs-ai-review` を自動付与
   - `code-scanner` 起票なら起票時に
   - 人間起票なら `/gh-kit:issue-review` 起動時に「未付与なら付ける」
3. AI が `templates/ユーザーレビュー要否判定.md` に従い `needs-user-review` を付けるか判定して必要なら付与
4. `/gh-kit:issue-review` が `needs-ai-review` 付きを拾う → `processing` 付与
5. AI レビュー実施（実装方針案・QA todo・分割提案）
6. 完了 → `processing` 除去、`needs-ai-review` 除去、コメント投稿
7. ユーザーが QA todo にチェックを入れる
8. ユーザーが内容に満足したら `needs-user-review` を手動で外す（不要なら最初から付いてない）
9. **次工程に進める条件**: open + needs-* なし + processing なし + 質問の todo がすべて埋まっている
10. `/gh-kit:pr-wip-create` の対象になる

### PR 側

1. `/gh-kit:pr-wip-create` が Issue から Draft PR を作成し `wip` 付与
2. `/gh-kit:pr-implement-auto` が `wip` を拾う → `processing` 付与、`wip` 除去
3. 実装完了 → `processing` 除去、`needs-ai-review` を必ず付与、`needs-user-review` を必要に応じて付与、`gh pr ready` で draft 解除
4. `/gh-kit:pr-review-auto` が `needs-ai-review` を拾う → `processing` 付与
5. AI レビュー実施
   - 合格 → `processing` / `needs-ai-review` 除去
     - `needs-user-review` がなければ即マージ
     - `needs-user-review` があれば残す（ユーザー待ち）
   - 修正必要 → `processing` 除去、`needs-fix` 付与
6. ユーザーが `needs-user-review` を手動で外す
7. **マージ可能条件**: open + needs-* なし + processing なし + draft でない + CI green

`needs-fix` 解消フロー: 修正 push 後にユーザーまたは AI が `needs-fix` を外し、再度 `needs-ai-review` を付ければレビューフェーズに戻る。

## 排他制御

`processing` がついた Issue/PR は **他セッションが触らない**。各スキルは取得時に必ず:

```bash
gh {issue|pr} edit {N} --add-label "$LABEL_PROCESSING" --remove-label "$LABEL_<前段>"
```

完了/失敗時に必ず:

```bash
gh {issue|pr} edit {N} --remove-label "$LABEL_PROCESSING" [--add-label "$LABEL_<次段>"]
```

## 検討事項（残課題）

| No | 論点 | 現状の方針 |
|---|---|---|
| 1 | 失敗系（旧 `implement-failed` 等）の扱い | タグでは管理せず、PR にコメントで失敗理由を残す。再着手は `needs-fix` 付与 + 修正 push 経由 |
| 2 | コンフリクト時の扱い（旧 `conflict-needs-human`） | `needs-user-review` + `needs-fix` の組み合わせで表現。コメントで diff を残す |
| 3 | `needs-fix` を AI が解消するスキルを設けるか | 当面は手動。需要が出たら別スキルを検討 |
| 4 | `needs-user-review` の自動付与判定の精度 | `templates/ユーザーレビュー要否判定.md` を運用しながら磨く。疑わしきは付ける側に倒す |

## 参考リンク

- `plugins/gh-kit/scripts/labels.sh`: ラベル名定義（変更時はここだけ）
- `plugins/gh-kit/templates/ユーザーレビュー要否判定.md`: `needs-user-review` の判定基準
- `plugins/gh-kit/CLAUDE.md`: 同梱ドキュメント
- `plugins/gh-kit/skills/*/SKILL.md` / `plugins/gh-kit/agents/*.md`: 各スキル・エージェントのラベル操作
- [gh issue edit reference](https://cli.github.com/manual/gh_issue_edit)
- [gh pr edit reference](https://cli.github.com/manual/gh_pr_edit)
