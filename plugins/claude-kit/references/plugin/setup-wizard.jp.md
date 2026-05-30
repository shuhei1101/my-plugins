<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# setup-wizard スキル オーサリングガイド

新規プラグイン作成時に**必須**となる `setup-wizard` スキルの設計ガイド。
ユーザーがプラグインを初めて使うときの初期セットアップと、ユースケース別の入口を提供する。
英語原本: `references/plugin/setup-wizard.md`

`plugin-migrate`（バージョン追従）と対になる「初期セットアップ」の規約。`common.md` と
`skills.md` も併読すること。

---

## なぜ必須か

- 各プラグインの env トグル・初期設定は CLAUDE.md に分散しており、ユーザーが能動的に読まないと気づけない
- インストール直後の「最初の一歩」フローがないと、せっかくの機能が使われない
- 初期セットアップ完了状態を **per-plugin で** 持つことで、横断的な依存を作らず各プラグインが自律する

---

## 標準仕様

| 項目 | 規約 |
|---|---|
| 名前 | `setup-wizard`（kebab-case 固定 — `<plugin>-setup-wizard` ではない） |
| トリガー | 手動（明示的に `/<plugin>:setup-wizard`） + SessionStart フックによる自動誘導（フラグ未設定時のみ） |
| 最初の動作 | `.claude/{plugin}.local.md` の `setup_done` を読み、既に true なら「再セットアップしますか？」と確認して終了/続行を分岐 |
| スコープ | このプラグイン自身の env / オンボーディングのみ。他プラグインの設定には絶対に触らない |
| 完了マーク | `.claude/{plugin}.local.md` の YAML frontmatter に `setup_done: true` を書き込む |

### setup-wizard と config の関係

`setup-wizard` は env 設定を **自プラグインの `config` スキル**に委譲する。各プラグインが
env トグルを持つ場合、`config` スキルの実装も必須（→ 後述「関連必須スキル」）。

---

## SessionStart フックの構成

各プラグインが自分の SessionStart フックを持ち、`setup_done` が false（または未定義）なら
「`/<plugin>:setup-wizard` を起動するよう」プロンプトを注入する。

### hooks.json 例

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/setup_check.py"
          }
        ]
      }
    ]
  }
}
```

### スクリプト要件

- `.claude/{plugin}.local.md` を読み、YAML frontmatter の `setup_done` を確認
- 真値なら何も出力せず正常終了
- 偽値・未定義なら「`/<plugin>:setup-wizard` を起動してセットアップしてください」というメッセージを stdout に出して `decision: block` で注入

---

## フラグスキーマ

`.claude/{plugin-name}.local.md`（既存の `plugin-settings` の仕組みを利用）:

```markdown
---
setup_done: true
---

# {plugin-name} の設定メモ

（ユーザー自由記述）
```

**version 情報は持たせない**。バージョン追従は規約で人間に守らせる方針:
プラグインを更新するときは、合わせて `setup-wizard` の内容も最新化する。
本リファレンス自体に「プラグイン更新時 setup-wizard も更新」を明記してあるため、
`plugin-migrate` 実装側のチェックリストにも入れること。

---

## setup-wizard の標準フロー

各ステップで `AskUserQuestion` を使う。**`AskUserQuestion` の options は 2〜4 個まで**
（公式 schema 上限。"Other" は自動付与される）。

### Step 1 — 既セットアップ判定

`.claude/{plugin}.local.md` を読み:

- `setup_done: true` → 「再セットアップしますか？（[再実行] / [中止]）」で確認
- false / 未定義 → そのまま続行

### Step 2 — env / 初期設定

`AskUserQuestion` で次のいずれかを選ばせる:

| ラベル | 動作 |
|---|---|
| すべて設定する | 自プラグインの `config` スキルを起動して全 env を対話設定 |
| 必須のみ | プラグインが必須と定義した env だけを設定（任意項目はスキップ） |
| スキップ | env 設定を行わず次へ。後で `/<plugin>:config` で個別設定可能と案内 |

### Step 3 — ユースケース紹介

`AskUserQuestion` で「最初に試したいユースケース」を 2〜4 件提示。
選んだユースケースのみ要点を 3〜5 行で紹介し、詳細は CLAUDE.md の該当セクションへリンク。

> **目次役に徹する**: 使い方の本文は CLAUDE.md に書き、setup-wizard はそこへ誘導するだけ。
> 重複管理を避けるため、setup-wizard 内で長文の使い方を書かない。

### Step 4 — 完了処理

`.claude/{plugin}.local.md` の frontmatter に `setup_done: true` を書き込み、再セットアップは
`/<plugin>:setup-wizard` を明示的に呼べばよいと案内して終了。

---

## 関連必須スキル

`setup-wizard` は単独では完結しない。env を持つプラグインでは下記スキルも合わせて実装する:

| スキル | 役割 |
|---|---|
| `config` | env 変数を `AskUserQuestion` で個別編集する単機能スキル。`setup-wizard` から委譲される |
| `plugin-migrate` | バージョン追従。詳細は本リファレンスの「Required skills」セクション |

env を持たないプラグインなら `config` は不要だが、`setup-wizard` のユースケース紹介
ステップは依然として価値があるため必須は維持する。

---

## skeleton（コピー用）

```markdown
---
name: setup-wizard
description: |
  `SessionStart` 時（フックが `setup_done` 未設定を検知したとき）、または
  ユーザーが `/<plugin>:setup-wizard` を明示的に呼んだときにトリガー。
  env 設定とユースケース紹介を経てプラグインをセットアップ済みとしてマークする。
---

# <plugin>:setup-wizard — 初回オンボーディング

このスキルは <plugin> の初回オンボーディング用。AskUserQuestion を内部で使用する
（このスキル内では AskUserQuestion 利用を許可）。

## 作業内容

### ステップ 1: 既セットアップ判定
{`.claude/<plugin>.local.md` を読み、`setup_done` の値で分岐}

### ステップ 2: env 設定（config スキルに委譲）
{AskUserQuestion で「すべて設定 / 必須のみ / スキップ」を提示し、選択に応じて `config` を起動}

### ステップ 3: ユースケース紹介
{AskUserQuestion で「最初に試したいユースケース」を 2〜4 件提示し、選んだものを要約 + CLAUDE.md へリンク}

### ステップ 4: 完了マーク
{`.claude/<plugin>.local.md` の frontmatter に `setup_done: true` を書き込む}
```

JP ミラー `SKILL.jp.md` も同時に作成すること（`common.md` の JP/EN ミラー規約参照）。

---

## チェックリスト

- [ ] `skills/setup-wizard/SKILL.md` と `SKILL.jp.md` を作成した
- [ ] `hooks/hooks.json` に `SessionStart` フックを追加し、`hooks/scripts/setup_check.py` を実装した
- [ ] env を持つプラグインなら `skills/config/SKILL.md` (+ `.jp.md`) も合わせて実装した
- [ ] プラグインの `CLAUDE.md` に「初回起動時のセットアップフロー」を 1 行記載した
- [ ] バージョンを bump し、changelog に "setup-wizard を追加" と記録した
