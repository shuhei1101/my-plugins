---
paths:
  - "plugins/*-kit/hooks/scripts/inject_references.py"
  - "plugins/*-kit/hooks/scripts/_common.py"
  - "plugins/*-kit/hooks/hooks.json"
  - "plugins/*-kit/hooks/templates/injection.md.j2"
  - "plugins/*-kit/hooks/templates/injection.jp.md.j2"
  - "plugins/*-kit/references/index.yaml"
  - "plugins/*-kit/references/index.jp.yaml"
  - "plugins/*-kit/references/injection_rules.yaml"
  - "plugins/*-kit/references/CLAUDE.md"
  - "plugins/*-kit/references/CLAUDE.jp.md"
---

> ⚠️ **Japanese mirror** — Claude には読み込まれない。このファイルを更新したら必ず英語原本 `.claude/rules/feature/kit-hooks-index-sync.md` も同じコミットで更新する。

## 概要

`dev-kit` と `claude-kit`（および将来追加される `*-kit`）は **同じ references 自動注入構造** を共有する:

- `hooks/scripts/inject_references.py` — PreToolUse(Edit/Write/MultiEdit) フックスクリプト
- `hooks/scripts/_common.py` — フックスクリプトの共通ヘルパー（stdin 読み・env truthy 判定・once-per-session トークン・block 理由出力等）。各 plugin 内に閉じる（プラグイン間共通化はしない）
- `hooks/hooks.json` — フック登録
- `hooks/templates/injection.md.j2` + `injection.jp.md.j2` — Jinja2 テンプレ
- `references/index.yaml` + `index.jp.yaml` — reference 一覧 + description
- `references/injection_rules.yaml` — pattern → required/optional マッピング
- `references/CLAUDE.md` + `CLAUDE.jp.md` — 「index.yaml を読め」スタイルのインデックス

これらの **構造（フォーマット・パース仕様・テンプレ変数・YAML スキーマ）** は plugin 間で完全に揃っている前提でフックが動く。
**片方の plugin で構造を変えたら、他の plugin も同じコミットで変える** — そうでないと片方だけ動いて片方は古い、という分裂状態になる。

共通化（共通スクリプト化）は試みたが、各 plugin が独立して install されることや `${CLAUDE_PLUGIN_ROOT}` の参照位置が plugin ごとに異なるため断念。ルールで「同コミットで両方を変える」ことを強制する形にした。

---

## 関連ファイル

| File path | Role |
|---|---|
| `plugins/*-kit/hooks/scripts/inject_references.py` | フック本体（plugin ごとに env var 名・ログ tag だけ違うほぼ同一のコード） |
| `plugins/*-kit/hooks/scripts/_common.py` | フックスクリプト共通ヘルパー（各 plugin に同一形式の関数群、ENV_PREFIX のみ違う） |
| `plugins/*-kit/hooks/hooks.json` | PreToolUse 登録（plugin ごとに同一形式） |
| `plugins/*-kit/hooks/templates/injection.md.j2` | 注入テンプレ英語版（plugin ごとに plugin 名表記だけ違う） |
| `plugins/*-kit/hooks/templates/injection.jp.md.j2` | 注入テンプレ日本語版 |
| `plugins/*-kit/references/index.yaml` | reference 一覧 (英語)。`references:` 配列で path + description |
| `plugins/*-kit/references/index.jp.yaml` | reference 一覧 (日本語ミラー)、人間用 |
| `plugins/*-kit/references/injection_rules.yaml` | pattern → required / optional マッピング |
| `plugins/*-kit/references/CLAUDE.md` | 「index.yaml と injection_rules.yaml を読め」式のインデックス |
| `plugins/*-kit/references/CLAUDE.jp.md` | 上記の日本語ミラー |
| `.claude/rules/feature/kit-hooks-index-sync.md` | このルール |

---

## 編集時に確認すること

`*-kit` の上記いずれかを編集したとき、**他の `*-kit` すべて** で以下を確認する:

- [ ] `inject_references.py` の関数 / 変数 / env var 規約（プラグインごとに `{PLUGIN}_INJECTION_LANG` を使う）が揃っているか
- [ ] `hooks.json` の matcher / command 構造が揃っているか
- [ ] テンプレの変数名（`file_path`, `required`, `optional`、`ref.path`, `ref.description`, `ref.body`）と Jinja2 制御構文が揃っているか
- [ ] `index.yaml` の YAML スキーマ（`references:` 配列、各エントリの `path`、`description` キー名）が揃っているか
- [ ] `index.jp.yaml` も同様にスキーマが揃っているか
- [ ] `injection_rules.yaml` の YAML スキーマ（`rules:` 配列、各 rule の `pattern`、`required`、`optional` キー名）が揃っているか
- [ ] `references/CLAUDE.md` (+ jp) の管理セクション（reading manually / reading automatically / SKILL から利用 / メンテナンス / cross-kit sync）が揃っているか
- [ ] **新規 `*-kit` 追加時**: このルールの `paths:` は `plugins/*-kit/...` のグロブで自動的に拾われるため変更不要だが、Overview に新 kit を明記する

**変更が plugin の構造ではなく中身（reference エントリ追加、新 pattern 追加など）の場合**:
そのときは plugin 内で完結する（他 kit を変える必要はない）。
ただし、ファイル構成自体は変えていなくても **キー名・型・命名規約・コメントスタイル** を変えたら構造変更扱い。

---

## やってはいけない

- 片方の plugin の `inject_references.py` だけ大きく変更してもう片方を放置（フックが壊れたり挙動が分裂したりする）
- `injection_rules.yaml` のキー名を一方だけリネームする（パーサーが対応できない）
- `index.yaml` のキー名を変える（`path` → `file` 等）
- Jinja2 テンプレの変数名を変えてもう片方を放置
- 「自分の kit だけ便利機能を追加」して構造を分裂させる（必要なら両方に同時に入れる、無理なら共通化策を再検討）

---

## Rule Maintenance

このドメイン内のファイル操作を行うとき:

- **新 kit 追加**（例: `vue-kit`、`django-kit`） → `paths:` のグロブ `plugins/*-kit/...` が自動マッチするため `paths:` 変更は不要。代わりに **概要セクションに新 kit を明記**
- **新ファイルをこの構造に追加** → `paths:` と「関連ファイル」表に追加し、各 kit に同じファイルが揃っているかチェックリストを追加
- **ファイル削除・リネーム** → `paths:` と「関連ファイル」表を更新
- **構造方針自体が変わる**（例: index.yaml と injection_rules.yaml を統合する等） → 概要セクションを書き直し
