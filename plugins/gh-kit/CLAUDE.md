# gh-kit ワークフロー設計

## モニター一覧（パイプライン順）

| #   | モニター名       | 起動スキル              | 監視ラベル              | 完了時の次ラベル                                   | 入力       | 必須/任意                     |
| --- | ---------------- | ----------------------- | ----------------------- | -------------------------------------------------- | ---------- | ----------------------------- |
| 1   | issue-triage     | gh-kit:issue-triage     | 確認:issue-triage       | 確認:issue-spec                                    | Issue 番号 | 必須                          |
| 2   | issue-spec       | gh-kit:issue-spec       | 確認:issue-spec         | 確認:issue-poc / issue-ui / issue-arch / issue-doc | Issue 番号 | 必須                          |
| 3   | issue-poc        | gh-kit:issue-poc        | 確認:issue-poc          | 確認:issue-arch                                    | Issue 番号 | 任意                          |
| 4   | issue-ui         | gh-kit:issue-ui         | 確認:issue-ui           | 確認:issue-arch                                    | Issue 番号 | 任意                          |
| 5   | issue-arch       | gh-kit:issue-arch       | 確認:issue-arch         | 確認:issue-detail                                  | Issue 番号 | 実装系で必須                  |
| 6   | issue-detail     | gh-kit:issue-detail     | 確認:issue-detail       | （ユーザー手動）確認:pr-plan                       | Issue 番号 | 実装系で必須                  |
| 7   | issue-doc        | gh-kit:issue-doc        | 確認:issue-doc          | （ユーザー手動）確認:pr-plan                       | Issue 番号 | ドキュメント/ハーネス系で必須 |
| 8   | pr-plan          | gh-kit:pr-plan          | 確認:pr-plan            | 確認:pr-test                                       | Issue 番号 | 必須                          |
| 9   | pr-test          | gh-kit:pr-test          | 確認:pr-test            | 確認:pr-impl                                       | PR 番号    | 必須                          |
| 10  | pr-impl          | gh-kit:pr-impl          | 確認:pr-impl            | 確認:pr-impl-review                                | PR 番号    | 必須                          |
| 11  | pr-impl-review   | gh-kit:pr-impl-review   | 確認:pr-impl-review     | 確認:pr-doc-plan（合格時）/ 確認:pr-impl（差し戻し時） | PR 番号    | 必須                          |
| 12  | pr-doc-plan      | gh-kit:pr-doc-plan      | 確認:pr-doc-plan        | 確認:pr-doc（影響あり）/ 確認:pr-merge（影響なし） | PR 番号    | 必須（影響リスト確認のみ）    |
| 13  | pr-doc           | gh-kit:pr-doc           | 確認:pr-doc             | 確認:pr-doc-review                                 | PR 番号    | ドキュメント影響あり時のみ    |
| 14  | pr-doc-review    | gh-kit:pr-doc-review    | 確認:pr-doc-review      | （ユーザー手動）確認:pr-merge（合格時）/ 確認:pr-doc（差し戻し時） | PR 番号    | ドキュメント影響あり時のみ    |
| 15  | pr-merge         | gh-kit:pr-merge         | 確認:pr-merge           | 完了                                               | PR 番号    | 必須                          |

---

## 設計レベルとモニターの対応

| 設計レベル            | 担当モニター | 決めること                                       |
| --------------------- | ------------ | ------------------------------------------------ |
| 管理                  | issue-triage | タイトル・概要・背景・type/priority・分割判断    |
| SS（システム要件）    | issue-spec   | 機能要件・非機能要件・受入条件・後続モニター判定 |
| PoC                   | issue-poc    | 外部ライブラリの動作検証                         |
| UI                    | issue-ui     | 画面構成・モック・画面遷移                       |
| SA（システム方式）    | issue-arch   | コンポーネント分割・採用ライブラリ・データフロー |
| DD（詳細設計）        | issue-detail | クラス・メソッドシグネチャ・データモデル         |
| ドキュメント/ハーネス | issue-doc    | CLAUDE.md・Rules・Wiki ページの構造・更新方針    |
| 実装計画              | pr-plan        | worktree + Draft PR + テスト計画                 |
| テスト                | pr-test        | テストコード作成（Red 状態）                     |
| 実装                  | pr-impl        | 実装 → Green 化                                  |
| 実装レビュー          | pr-impl-review | コード品質チェック                               |
| ドキュメント計画      | pr-doc-plan    | 実装結果を踏まえた詳細なドキュメント修正計画     |
| ドキュメント実装      | pr-doc         | Wiki / CLAUDE.md / Rules の実コミット            |
| ドキュメントレビュー  | pr-doc-review  | ドキュメント差分のレビュー                       |
| マージ                | pr-merge       | マージ + コンフリクト解消 + worktree 削除        |

---

## issue本文の担当セクション



## issue本文の担当セクション
---
## wikiページの担当セクション

| 分類             | ページ名                           | 概要                                           | 担当モニター              |
| ---------------- | ---------------------------------- | ---------------------------------------------- | ------------------------- |
| コード設計図     | クラス図_{モジュール名}.md         | クラス構成と関係（Mermaid classDiagram）       | issue-arch / issue-detail |
| コード設計図     | シーケンス図_{機能名}.md           | 処理の呼び出し順（Mermaid sequenceDiagram）    | issue-arch / issue-detail |
| コード設計図     | 状態遷移図_{コンポーネント名}.md   | 状態を持つ要素の遷移（Mermaid stateDiagram）   | issue-detail              |
| コード設計図     | ER図.md                            | DB スキーマ（Mermaid erDiagram）               | issue-arch / issue-detail |
| コード設計図     | 画面遷移図_{機能名}.md             | UI 画面間の遷移                                | issue-ui                  |
| コード設計図     | アーキテクチャ図.md                | システム全体構成（C4 / Mermaid）               | issue-arch                |
| コード設計図     | データフロー図_{機能名}.md         | データの流れ                                   | issue-arch                |
| プロジェクト管理 | ラベル定義一覧.md                  | constants.sh のラベルと運用ルール              | issue-doc                 |
| プロジェクト管理 | ディレクトリ構成図.md              | プラグイン全体のフォルダ階層                   | issue-doc                 |
| プロジェクト管理 | 命名規則.md                        | ファイル名・関数名・ラベル名の命名規則         | issue-doc                 |
| 運用・規約       | コーディング規約_Python.md         | Python のコーディング規約                      | issue-doc                 |
| 運用・規約       | コーディング規約_Bash.md           | Bash のコーディング規約                        | issue-doc                 |
| 運用・規約       | コミットメッセージ規約.md          | コミットメッセージのフォーマット               | issue-doc                 |
| 運用・規約       | イシュードキュメント.md            | Issue 本文テンプレート                         | issue-doc                 |
| 運用・規約       | PRドキュメント.md                  | PR 本文テンプレート                            | issue-doc                 |
| 運用・規約       | セットアップ手順.md                | プラグインインストール手順                     | issue-doc                 |
| Claude ハーネス  | スキル一覧.md                      | プラグイン内の全 SKILL.md の一覧と役割         | issue-doc                 |
| Claude ハーネス  | カスタムサブエージェント一覧.md    | agents/*.md の一覧と役割                       | issue-doc                 |
| Claude ハーネス  | フック一覧.md                      | session-start / PreToolUse などの設定一覧      | issue-doc                 |
| Claude ハーネス  | 動的注入対応表.md                  | 編集対象パス → 注入される Wiki ページの対応    | issue-doc                 |
| Claude ハーネス  | プラグイン構成.md                  | hooks / skills / agents / scripts の役割と関係 | issue-doc                 |
| 共通テンプレート | テンプレート_ライブラリ選定論点.md | 1論点1コメント用テンプレート                   | issue-arch                |
| 共通テンプレート | テンプレート_設計レビュー論点.md   | 1論点1コメント用テンプレート                   | issue-arch / issue-detail |
| 共通テンプレート | ghコマンドまとめ.md                | スキルから参照する gh CLI コマンド集           | issue-doc                 |

## 設計原則

### モニター vs カスタムサブエージェントの判断軸

**ユーザーとのやり取りが発生するなら「モニター」、発生しないなら「カスタムサブエージェント」**

| 場面                                             | 採用             | 理由                                               |
| ------------------------------------------------ | ---------------- | -------------------------------------------------- |
| ユーザーへ質問してコメント返信を待つ             | モニター         | スキルが長時間待機せず、ラベル付け替えで再開できる |
| 複数の観点・候補を並列に深堀りして結果を統合する | サブエージェント | 内部処理で完結、Agent ツールで並列起動できる       |

### 領域別の処理（フロント/バック/DB）

`issue-arch` の領域別検討は**カスタムサブエージェントで並列処理**する。
モニター数を爆発させないため、領域分割はモニターではなくサブエージェントで行う。

---

## モニター詳細

### 1. issue-triage

**モニター条件**:
- Issue に `確認:issue-triage` ラベルが付与された
- Assignee にユーザが設定されていない

起票直後の Issue を整える。**「分かっていることだけを整理する」**フェーズで、仕様・実装方針の決定は後の issue-spec 以降に任せる。

- 本文の整文・整形（入力の誤字脱字・改行整理・文言修正）を行う
- 本文に欠けているセクションがあれば、**ユーザーが書いた情報の範囲内で**テンプレートに沿って埋める
- 内容を表すタイトルに更新する
- `type:*` ラベル・優先度ラベルを付与する
- **現状調査**: Issue が言及する領域のコードベース・既存実装・関連ファイルを Read で確認する
- Issue のスコープが大きすぎる場合は子 Issue の分割を提案し、ユーザーの合意が得られれば親 Issue はクローズする

**禁止事項**:
- モデルが持っている知識で**仕様や実装方針を推測して書き加えない**（ハルシネーション防止）
- 「こうあるべき」「こうした方がいい」は spec / arch / detail で決めるので、ここでは書かない
- 調査せずに想像で書いた内容は後続フェーズのコンテキストを汚染するので絶対 NG

**ラベル更新**:
- Issue: 除去 `確認:issue-triage` / 付与 `確認:issue-spec`
- PR: なし

- Assignee にユーザが設定されていない

要件で曖昧な点をユーザーに確認する。

- Issue 本文・コードベースを読んで、要件が確定していない箇所を抽出
- 1 質問 = 1 コメントで投稿する
- `assignee=ユーザー` を付けて待機状態にする
- ユーザーが回答した後は、ユーザー自身が `確認:issue-design` ラベルを手動付与する

ラベル更新:
- Issue
  - 除去: `確認:issue-clarifier`
  - 付与: なし（assignee=ユーザーで待機）
- PR
  - なし

### 3. issue-design

モニター条件:
- Issue に `確認:issue-design` ラベルが付与された
- Assignee にユーザが設定されていない

実装の論点を洗い出し、3 案比較 + 推奨を Issue にコメントする。

- カスタムサブエージェント（design-points-finder / design-reviewer / library-finder / library-researcher）を並列起動して各論点を深堀り
- 1 コメント = 1 論点で投稿する（ライブラリ選定論点・設計論点いずれも）
- `assignee=ユーザー` を付けて待機状態にする
- ユーザーが各論点を確認した後は、ユーザー自身が `確認:pr-planner` ラベルを手動付与する

ラベル更新:
- Issue
  - 除去: `確認:issue-design`
  - 付与: なし（assignee=ユーザーで待機）
- PR
  - なし

### 4. pr-plan

モニター条件:
- Issue に `確認:pr-planner` ラベルが付与された
- Assignee にユーザが設定されていない

Issue の決定事項をもとに Draft PR を作成する。

- worktree を作成し、PR 本文テンプレートに沿った空コミットを push
- `gh pr create --draft` で Draft PR を作成
- 完了時に `確認:pr-plan-reviewer` ラベルを付与

ラベル更新:
- Issue
  - 除去: `確認:pr-planner`
  - 付与: なし
- PR
  - 付与: `確認:pr-plan-reviewer`

### 5. pr-plan-review

モニター条件:
- PR に `確認:pr-plan-reviewer` ラベルが付与された
- Assignee にユーザが設定されていない

Draft PR のプランが Issue の決定事項と整合しているかをチェックする。

- Issue で決まったメソッドシグネチャ・採用ライブラリ・設計方針と PR 本文を照合
- 整合していれば `確認:pr-implementer` ラベルに付け替える
- 整合していなければ修正コメントを投稿し、`assignee=ユーザー` で差し戻し

ラベル更新:
- Issue
  - なし
- PR
  - 除去: `確認:pr-plan-reviewer`
  - 付与: `確認:pr-implementer`（合格時）/ なし（差し戻し時、assignee=ユーザーで待機）

### 6. pr-implement

モニター条件:
- PR に `確認:pr-implementer` ラベルが付与された
- Assignee にユーザが設定されていない

Draft PR の中身を実装する。

- worktree に復帰し、fetch/reset で最新化
- Issue で決定した方針に沿って実装し、テスト実行・コミット・push
- `gh pr ready` で Draft を解除
- 完了時に `確認:pr-test-creator` ラベルに付け替える

ラベル更新:
- Issue
  - なし
- PR
  - 除去: `確認:pr-implementer`
  - 付与: `確認:pr-test-creator`

### 7. pr-test-create

モニター条件:
- PR に `確認:pr-test-creator` ラベルが付与された
- Assignee にユーザが設定されていない

実装に対するテストを追加する。

- 既存テストの規約に沿って新規テストを追加
- テスト実行・コミット・push
- 完了時に `確認:pr-reviewer` ラベルに付け替える

ラベル更新:
- Issue
  - なし
- PR
  - 除去: `確認:pr-test-creator`
  - 付与: `確認:pr-reviewer`

### 8. pr-review

モニター条件:
- PR に `確認:pr-reviewer` ラベルが付与された
- Assignee にユーザが設定されていない

PR のコード品質をレビューする。

- バグ・パフォーマンス・可読性・保守性の観点で diff をレビュー
- 指摘があればインラインコメントで投稿
- 問題なければ `assignee=ユーザー` で待機状態にする
- ユーザーが承認後、ユーザー自身が `確認:pr-merger` ラベルを手動付与する

ラベル更新:
- Issue
  - なし
- PR
  - 除去: `確認:pr-reviewer`
  - 付与: なし（assignee=ユーザーで待機）

### 9. pr-merge

モニター条件:
- PR に `確認:pr-merger` ラベルが付与された
- Assignee にユーザが設定されていない

PR を base ブランチへマージする。

- `gh pr merge --squash --delete-branch` で squash マージ + リモートブランチ削除
- ローカルの worktree を削除

ラベル更新:
- Issue
  - なし（マージで自動クローズ）
- PR
  - 除去: `確認:pr-merger`（マージで PR 自体がクローズ）

---

## コメント返信ルール（共通）

Wiki に `コメント返信ルール.md` を作り、constants.sh に `GH_KIT_REFERENCE_COMMENT_REPLY` を追加し、各モニターのスキル冒頭で `read_urls.py` で動的注入する。

### ルール内容

ユーザーが「ここはこうした方がいい」とコメントしてきたら:

1. **本文側を上書き更新する**（該当セクションを最新内容に置換）
2. AI の応答コメントは**短く** — 「本文の `## XXX` セクションを更新しました」程度
3. **詳細をコメントに書かない**。本文に書く

### 本文更新の方針

- 元の記述は**消してよい**（コメント履歴に議論の経緯は残るため）
- 本文は常に「最新の確定版」に保つ
- 部分書き換えは難しいので、各モニター担当セクションを丸ごと置換する

### 例

| ユーザーコメント | AI の対応 | AI の応答コメント |
| ---------------- | --------- | ----------------- |
| 「ライブラリは LangChain ではなく Anthropic SDK にして」 | 本文の「採用ライブラリ」セクションを更新 | 「採用ライブラリを Anthropic SDK に変更し、本文に反映しました」 |
| 「分割案 B でお願い」 | 本文の「設計方針」セクションを更新 + 子 Issue を作成 | 「分割案 B を採用しました。子 Issue を #45, #46 で作成」 |

---

## 本文構造ルール（Issue/PR 共通）

本文はテンプレート構造にして、各モニターが担当セクションだけ上書きする。

### Issue 本文テンプレート例

```markdown
## 概要
（issue-triage が記入）

## 背景
（issue-triage が記入）

## 明確化された要件
（issue-clarify が記入）

## 設計決定事項

### 採用ライブラリ
（issue-design が記入）

### メソッドシグネチャ
（issue-design が記入）

### 実装方針
（issue-design が記入）
```

| 役割 | 場所 |
| ---- | ---- |
| 議論の経緯（論点・質問・回答） | コメント履歴 |
| 確定した内容（最新版のみ） | 本文 |

---

## 記憶喪失問題への対応

各モニターはシェルから毎ターン起動されるので前ターンの記憶を持たない。ただし以下のルールで十分機能する:

- AI 投稿には必ずプレフィックス（例: `🤖 Generated by issue-design`）をつける
- 新ターンのモニターはプレフィックスまたは著者ログインで「AI コメント vs ユーザーコメント」を判別
- 「前回の自分」という意識は不要。**AI 一般として読み返せばよい**

---

## 運用ルール: assignee による状態管理

各モニターは「**監視ラベル付き AND assignee に自分自身が入っていない**」Issue/PR を拾う。
assignee がボールの所在を示す。

| アクター | アクション | assignee 操作 |
| -------- | ---------- | ------------- |
| AI | コメントしてボールを渡す | `=ユーザー` を付ける |
| ユーザー | コメント等で返信 | **自分自身を外す**（モニターが再度拾えるように） |

スキル側は「最後のコメント著者が AI なら初回、ユーザーなら返信ターン」で分岐する。

---

## カスタムサブエージェント一覧

| サブエージェント     | 呼び元モニター | 入力                    | 出力                           |
| -------------------- | -------------- | ----------------------- | ------------------------------ |
| design-points-finder | issue-design   | Issue + 関連コード      | 設計論点リスト（タイトルだけ） |
| design-reviewer      | issue-design   | 1論点 + 関連コード      | 3案比較 + 推奨                 |
| library-finder       | issue-design   | 処理目的 + 既存スタック | ライブラリ候補3〜5個           |
| library-researcher   | issue-design   | 1ライブラリ             | 観点別スコア + コード例        |
