---
name: conversation-to-claude
description: |
  Analyze the current session's conversation history and automatically create all
  appropriate artifacts (skill, rule, hook, CLAUDE.md, incidents, glossary) for
  persisting the knowledge or workflow discovered. No user confirmation required.
  Trigger when the user says "会話をキャプチャして", "今の作業を保存して", "この手順を残したい",
  "会話からスキル作って", "会話からルール作って",
  or invoked explicitly as `/work:conversation-to-claude`.
---

# conversation-to-claude — 会話履歴からアーティファクトを生成

セッションの会話履歴を解析し、適切な Claude Code アーティファクト種別（skill / rule / hook /
CLAUDE.md / incidents / glossary）をすべて特定して、確認を求めずに自動で実装する。

---

## 概要

実装・調査・設定タスクを終えた後、学んだことを永続化したくなることが多い。繰り返せるワークフロー、
ファイル依存関係、フックのトリガー、プロジェクト規約など。本スキルはその知識に最適な形を判断し、
特定したアーティファクトをすべて自動生成する。

**量より質。** 本スキルの価値は、**まだ発見可能でない**知識を捕まえることにあり、大量のエントリを
生み出すことではない。glossary の各用語・各 incident は Step 2 の重複チェックを通過しなければならない
（CLAUDE.md・ルール・フォルダ構成・既存エントリが提供していない情報を追加するものでなければならない）。
迷ったら**登録しない**。

---

## タスク

### Step 1: 会話履歴を解析する

#### 条件

- 常時 — 最初に実行

#### 処理

1. セッションの会話**全体**を見直し、以下のカテゴリごとに候補を抽出する。
   skill / rule / hook / CLAUDE.md 候補は広く拾う（再利用できるものを取りこぼすより、多めに拾う方がよい）。
   **incidents** と **glossary** については E・F で定義する厳格な採用基準を適用する — この2つは
   量ではなく品質でゲートする。

   **A. 繰り返せるワークフロー候補**（→ skill）

   該当: ユーザーの判断・分岐・対話を伴う複数ステップ（3つ以上）のワークフロー。価値は再利用性
   — 誰かが同じ手順をまた実行するもの。

   - ユーザー対話・分岐を伴う3ステップ以上の手順
   - 他プロジェクトでも再利用する価値のあるパターン
   - ユーザーが繰り返しそうな複数ステップの調査・セットアップフロー

   skill でないもの: 単一アクション、一度きりの修正、ルールや CLAUDE.md に属する情報。

   ---

   **B. ファイル依存・パス構造の知識**（→ rule）

   該当: 2つ以上のファイルが同期している必要があると分かったとき。ルールは Claude が `paths:` に
   マッチするファイルを*読んだ*ときに自動ロードされ、毎回リンク先ファイルを提示する。

   `paths:` の挙動:
   - マッチするファイルを **Claude が読んだ**ときに発火 — シェルコマンド（mv, rm, cp）では発火しない
   - `paths:` には、このドメインで作業するとき Claude が実際に*開く*ファイルを設定する

   ルールに書くもの: 関連ファイルへのリンク、「X を編集したら Y も確認」。短く保つ。
   ルールに書かないもの: 詳細なドキュメント、ステップバイステップの手順。

   - 「ファイル X を編集したら必ず Y も編集する必要がある」
   - 「設定はここ」「ルーティングはここ」というパスの役割の発見
   - セッション中に発見した「常にセットで確認」「同期が必要」というパターン

   ---

   **C. イベント駆動の自動化**（→ hook）

   該当: 特定のイベントで自動的に何かを起こしたいとき — ユーザーのプロンプト不要。

   利用可能なイベント: `PreToolUse` / `PostToolUse` / `Stop` / `SubagentStop` / `SessionStart` / `SessionEnd` / `UserPromptSubmit` / `PreCompact` / `Notification`

   hook でないもの: ユーザーが意識的にトリガーすべきもの — skill を使う。

   - 特定のツール使用の前後・セッション開始時に自動実行するアクション
   - 関連イベントごとに発火すべき検証・通知

   ---

   **D. プロジェクト全体の規約・ガイドライン**（→ CLAUDE.md）

   該当: どのファイルを開いていても、全セッションが知っておくべき規約・禁止事項・構造的知識。
   CLAUDE.md は常時ロード、ルールはファイル読み込み時のみロード。

   CLAUDE.md に向く内容: 禁止事項、命名規約、フォルダ/ディレクトリ構成、設計原則、オンボーディング情報。

   CLAUDE.md に向かないもの: ファイル固有の同期ルール（rule を使う）、手順（skill を使う）、
   イベント自動化（hook を使う）。

   ---

   **E. 学んだ教訓・再発防止**（→ `incidents`）

   incident は**このセッションで実際に起きた、作業プロセス上の具体的なミス**（操作・判断の誤り。
   コードの不具合＝バグではない）を記録して再発を防ぐもの。**以下のすべてを満たす場合のみ**記録する:

   - このセッションで実際に失敗が起きた: コマンド/操作が失敗し正しいやり方が今分かった、ファイルを
     誤って削除/上書きした、当初の TODO で計画されていたタスクを AI が黙って落としてユーザーが再依頼した、
     AI が誤った前提で動いてユーザーが訂正した。
   - その教訓が将来のセッションに**一般化できる**（このブランチのコード固有でない）。
   - 防止策が他所で**まだ捕捉されていない**（Step 2 の重複チェック参照）。

   **記録しない**もの（旧版が抱えていた失敗モード）:
   - **コードのバグそのもの・その修正内容** — 最頻出の誤登録。バグ対応ブランチで直したバグは、
     直したら完了でありコードの不具合であって、セッションの作業プロセスのミスではない。これを書き始めると
     エントリ数が爆発する。「何のバグをどう直したか」はブランチドキュメント / コミットメッセージに残るもの。
   - **「それは既にルール / CLAUDE.md の規約だ」** 正しい挙動が既存ルール・CLAUDE.md・フックで
     強制されている（またはされるべき）なら、それは incident ではない。ルールが*存在すべき*なら、
     incident を記録するのではなくルール（カテゴリ B/D）を作る。
   - PR/ブランチの作業内容そのもの（どの機能を実装し、どのコードを変えたか）。
   - ユーザーがスコープ拡張として新規追加したタスク。
   - プロジェクト内やよく知られたツールのドキュメントに既出の一般的ベストプラクティス。
   - 一般化できる防止策のない、一度きりのうっかりミス。

   ---

   **F. プロジェクト固有の用語**（→ `glossary`）

   glossary の用語は、読み手が誤解しかねないプロジェクト固有の名詞/略語/概念を定義するもの。
   glossary は**常時ロード**されるため、各エントリは全セッションでコンテキストを消費する — 採用基準は高い。
   **以下のすべてを満たす場合のみ**登録する:

   - **プロジェクト固有**である: 造語、内部略語、またはプロジェクト固有の非自明な意味で使われる語。
   - 意味が**名前自体から自明でなく**、定義なしでは読み手が本当に誤解する/理解できない。
   - **繰り返し出る** — 一度きりではなく、繰り返し参照される（される予定の）語。
   - 意味が**まだ発見可能でない**（Step 2 の重複チェック参照）。

   **登録しない**もの（旧版が抱えていた失敗モード）:
   - **「それは既に CLAUDE.md / ルール / スキルの description にある」** それらが真実の源であり、
     glossary への重複記載は純粋な肥大化。源を指す/源に頼る。
   - **「フォルダ/ファイル構成を見れば分かる」** リポジトリを開いたりファイル名を読めば意味が自明
     （例「`skills/` フォルダにはスキルが入っている」）なら登録しない。
   - プロジェクト固有でない一般語・業界標準語（git, PR, commit, hook, lint）。
   - 再利用価値のない一度きりの言及。
   - 該当ファイルを読めば既に自明なことの言い換え。

→ Step 2 へ

#### 出力

- カテゴリごとの候補リスト。skill/rule/hook/CLAUDE.md は広めに。incidents/glossary は上記 E/F の
  基準を通過したエントリのみ。

---

### Step 2: 既存アーティファクトとの重複排除（真実の源チェック）

#### 条件

- Step 1 完了

#### 処理

このステップが**増殖防止ガード**。旧版が生んだ低価値エントリを防ぐのが目的。**すべての**候補に対して
実行し、特に incidents と glossary には積極的に適用する。

1. 各候補について、既にそれをカバーする既存アーティファクトをプロジェクト内で探す:

   | 候補種別 | 探す場所（用語・トピックで検索） |
   |---|---|
   | Skill | `.claude/skills/`、`plugins/*/skills/` — SKILL.md のファイル名と description |
   | Rule | `.claude/rules/` — ファイル名と見出し行 |
   | Hook | `~/.claude/settings.json`、`.claude/settings.json`、`plugins/*/hooks/` |
   | CLAUDE.md 内容 | `CLAUDE.md`、各 `plugins/*/CLAUDE.md` — 関連セクション |
   | incidents | `.claude/rules/incidents.md` + `.claude/references/incidents/` — 同じトピックか？ |
   | glossary | `.claude/rules/glossary.md` — 同じ/近接する用語か？ |

2. **incidents・glossary の全候補に対する必須重複チェック。** 残す前に必ず能動的に検索する:
   - **glossary** → `CLAUDE.md`、各 `plugins/*/CLAUDE.md`、`.claude/rules/`、スキルの description を
     用語とその概念で grep する。意味が既にそこに書かれている、またはフォルダ/ファイル構成から自明なら
     → **破棄**。
   - **incidents** → 既存のルール・CLAUDE.md 規約・フック・incident がその教訓を既に強制/記録して
     いないか確認する。していれば → **破棄**（ルールが*あるべきなのに*ない場合は、代わりにルール候補に
     変換する）。

3. 候補ごとに判断を適用する:
   - **既存にマージ**: 同じドメインを既存アーティファクトがカバー → それを拡張、新規ファイルは作らない。
   - **破棄**: 一度きり・一時的・既出・自明 → スキップ。
   - **新規作成**: カバーする既存アーティファクトがなく、かつそのカテゴリの採用基準を満たす。

4. 判断（新規 / `{path}` にマージ / 破棄）を Step 3 のために記録する。

→ Step 3 へ

#### 出力

- 残った各候補について: 判断（新規 / マージ）と対象パス。破棄候補は除外。

---

### Step 3: 全アーティファクトを実装する

#### 条件

- Step 2 完了

#### 処理

1. Step 2 で何も残らなかった場合:
   - 「今回の会話から永続化すべき知識・手順は見つかりませんでした」と報告して終了。

2. **incidents / glossary** — creator スキルに委譲せず直接処理する:
   - **incidents**: `.claude/rules/incidents.md`（インデックス）に1行サマリを追記し、詳細を
     `.claude/references/incidents/{slug}.md`（+ `.jp.md` ミラー）に書く。
   - **glossary**: `.claude/rules/glossary.md` を読む（なければ作成）。適切な H2 カテゴリ表に用語を追記。
     各定義は1〜2文に保つ。

3. **Skill / Rule / Hook / CLAUDE.md** — 候補が残ったカテゴリごとにサブエージェントを1つ起動する。
   該当する全サブエージェントを Agent ツールの `isolation: "worktree"` で**1メッセージにまとめて**
   （並列）起動する。全完了を待ってから Step 4 へ。

   各サブエージェントは、対応する **claude-kit の creator スキル**に委譲する（install 先に依存せず
   解決するようスラッシュコマンドで起動する）:

   | カテゴリ | creator スキル（起動） | 実装対象 |
   |---|---|---|
   | Skill | `/claude-kit:skill-creator` | 全 skill 候補 |
   | Rule | `/claude-kit:rule-creator` | 全 rule 候補 |
   | Hook | `/claude-kit:hook-creator` | 全 hook 候補 |
   | CLAUDE.md | `/claude-kit:claude-creator` | 全 CLAUDE.md 追記 |

   **サブエージェントプロンプトのテンプレート**（送信前にカテゴリごとに `{…}` を埋める）:

   ```
   You are a subagent responsible for creating [{Category}] artifacts.

   ## Steps
   1. Invoke the creator skill: {creator skill slash command}
   2. Follow its steps to implement all targets below.
      Skip any confirmation prompts — implement automatically.

   ## Targets
   {For each candidate in this category:}
   ### {artifact name or description}
   - Trigger / Domain / Event: {extracted trigger, domain, or event}
   - Context: {workflow steps / file list / hook behavior / guideline text}
   - Step 2 decision: {new | merge into {path}}

   ## Notes
   - If multiple targets exist, implement them one at a time in listed order
   - Follow the Step 2 decision (new / merge) for each target
   ```

   > claude-kit がこのプロジェクトに install されていない場合、サブエージェントは creator スキルを
   > 起動できない。その場合はプロジェクトの既存規約に従ってアーティファクトを直接作成する
   > （claude-kit の ref-inject フックがあれば、対象ファイルの Write/Edit 時に認可ガイドが自動注入される）。

→ Step 4 へ

#### 注意

- creator スキル内の確認プロンプトはスキップする
- glossary は常時ロード — 定義は1〜2文に保つ

---

### Step 4: 出力を検証する

#### 条件

- Step 3 完了

#### 処理

1. 各アーティファクトについて検証する:
   - 期待されるファイルが正しいパスに作成/更新されたか
   - 内容が意図したアーティファクトと一致するか（見出しと主要フィールドをスポットチェック）
   - 期待ディレクトリの外に意図しないファイルが作られていないか
   - **incidents/glossary を Step 2 の重複基準で再チェック** — 見直して CLAUDE.md / ルール /
     フォルダ構成を単に重複しているだけのエントリは削除する。
2. 問題があれば直接修正する（サブエージェントの再起動はしない）。

→ Step 5 へ

---

### Step 5: コミットして報告する

#### 条件

- Step 4 完了

#### 処理

1. 作成・更新した全ファイルを説明的なメッセージでコミットする
2. 作成・更新した全ファイルをユーザーに列挙する

---

## リファレンス

### アーティファクト種別サマリ

| 種別 | 出力先 | 主な用途 |
|---|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` | 複雑で繰り返せるワークフローの自動化 |
| Rule | `.claude/rules/<name>.md` | ファイル依存・パス構造の永続化 |
| Hook | `settings.json` の hooks | ツール前後の自動チェック・通知 |
| CLAUDE.md | `CLAUDE.md` に追記 | プロジェクト規約・ガイドラインの記録 |
| incidents | `.claude/rules/incidents.md`（インデックス — 常時ロード）<br>`.claude/references/incidents/{slug}.md`（詳細 en）<br>`.claude/references/incidents/{slug}.jp.md`（詳細 jp） | 失敗・誤前提の再発防止 |
| glossary | `.claude/rules/glossary.md`（常時ロード） | プロジェクト固有の用語定義 |

### 採用基準クイックリファレンス

- **glossary**: プロジェクト固有 + 意味が非自明 + 繰り返し出る + CLAUDE.md / ルール / スキル description / フォルダ構成に既出でない。
- **incidents**: このセッションで実際にミスが起きた + 教訓が一般化できる + 既存のルール / CLAUDE.md / フック / 既存 incident で既に強制されていない。
- どちらも迷ったら: **破棄**。

採用基準とファイル形式の完全版は work リファレンスにもあり、対象ファイルの編集時に自動注入される:
`references/conversation/グロッサリー.md`（`.claude/rules/glossary.md` 編集時）と
`references/conversation/インシデント.md`（`.claude/rules/incidents.md` / `.claude/references/incidents/**` 編集時）。

### 公式ドキュメント

- Skills: **https://code.claude.com/docs/en/skills**
- Path-scoped rules: **https://code.claude.com/docs/en/memory**
- Hooks: **https://code.claude.com/docs/en/hooks**
