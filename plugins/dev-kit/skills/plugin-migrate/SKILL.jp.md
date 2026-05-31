---
name: plugin-migrate
description: |
  プロジェクト内の dev-kit 生成物（静的テンプレと dev-kit 規約に従って作られたコード・設定ファイル）が
  現在インストール済みの dev-kit バージョンの規約を満たしているかを検査・修正する。
  静的テンプレの再コピーと、既存プロジェクトファイルの規約逸脱の発見・修正が対象。
  手動起動のみ — `/dev-kit:plugin-migrate` を使う。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# dev-kit:plugin-migrate — dev-kit 生成物を現行規約に揃える

## 何をするか

dev-kit がプロジェクトに関与した成果物を 2 種類に分けて扱う:

| 種別 | 内容 | 処理 |
|---|---|---|
| 静的テンプレ | html-implement が `.claude/rules/` に配布したルールファイル、html-debug-fab が配布した `uidev.css` / `uidev.js` | プラグイン本体から最新版を再コピー |
| 規約遵守ファイル | dev-kit 規約に従って作られた Python / HTML-CSS-JS / Next.js のソースコード | 現行リファレンスと照合し、逸脱があれば修正 |

静的テンプレの再コピーは自動。規約の検査・修正は Claude が現行リファレンスを参照して判断する（injection hook が対象ファイルを `Read` する際に自動注入される）。

どの言語の規約を検査するかは `settings.json` の env 変数（`DEV_KIT_PYTHON` / `DEV_KIT_HTML` / `DEV_KIT_NEXT`）で決まる。

このスキルはどの他プラグインにも依存しない。コミット・マージはユーザーの責務。

---

## 静的テンプレ一覧（ステップ1 で再コピーする対象）

| ソース (`${CLAUDE_PLUGIN_ROOT}/`) | 配布先 |
|---|---|
| `skills/html-debug-fab/templates/uidev.css` | プロジェクトの静的アセットディレクトリ |
|  | `uidev.js` も同ディレクトリ |
|  | `CLAUDE.md` も同ディレクトリ |
|  | `CLAUDE.jp.md` も同ディレクトリ |

---

## タスク

### ステップ1: html-debug-fab のウィジェットを再コピーする

#### 条件

- プロジェクトに `uidev.css` が存在する（html-debug-fab 導入済みと判定）

#### 処理

1. `find . -name 'uidev.css' -not -path '*/node_modules/*' -not -path '*/.git/*'` で検索
2. 見つからなければ未導入としてステップ2 へスキップ
3. 1 箇所のみ → そのディレクトリを配布先として確定
4. 複数 → ユーザーに確認
5. `${CLAUDE_PLUGIN_ROOT}/skills/html-debug-fab/templates/` から `uidev.css` / `uidev.js` / `CLAUDE.md` / `CLAUDE.jp.md` を上書きコピー（`example.html` は除く）
6. 更新したファイル名を報告

→ ステップ2 へ

---

### ステップ2: Python ソースファイルの規約検査（DEV_KIT_PYTHON が有効な場合）

#### 条件

- `settings.json` の env で `DEV_KIT_PYTHON` が truthy

#### 処理

1. プロジェクト内の Python ファイルを列挙する
   ```bash
   find . -name "*.py" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*"
   ```
2. ファイルを `Read` する（injection hook が Python リファレンスを自動注入する）
3. 現行リファレンスの規約と照合し、逸脱箇所を特定する
   - 例: 型ヒント欠如、ロガー実装が規約外、設定ファイルの構造が規約外
4. 逸脱が見つかったファイルごとに内容と修正方針を提示し、ユーザーの確認を得てから修正する
5. ファイル数が多い場合はバッチ処理（例: 10 ファイルずつ）

→ ステップ3 へ

#### 注意

injection hook が `Read` 時に自動注入した Python リファレンス群（`references/python/` 配下）が規約判断の根拠。リファレンスに明記されていない事項は逸脱として扱わない。

---

### ステップ3: HTML/CSS/JS ソースファイルの規約検査（DEV_KIT_HTML が有効な場合）

#### 条件

- `settings.json` の env で `DEV_KIT_HTML` が truthy

#### 処理

1. HTML / CSS / JS ファイルを列挙する
   ```bash
   find . \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -not -path "*/node_modules/*" -not -path "*/.git/*"
   ```
2. ファイルを `Read` する（HTML リファレンスが自動注入される）
3. 現行リファレンスの規約（FLOCSS、デザイントークン、DebugFAB 使い方 など）と照合し、逸脱を特定
4. 逸脱ファイルごとに提示・確認・修正

→ ステップ4 へ

---

### ステップ4: TypeScript/TSX ソースファイルの規約検査（DEV_KIT_NEXT が有効な場合）

#### 条件

- `settings.json` の env で `DEV_KIT_NEXT` が truthy

#### 処理

1. TS / TSX ファイルを列挙する
   ```bash
   find . \( -name "*.ts" -o -name "*.tsx" \) -not -path "*/node_modules/*" -not -path "*/.git/*"
   ```
2. ファイルを `Read` する（Next.js リファレンスが自動注入される）
3. 現行リファレンスの規約（ファイル配置、Server Actions、auth、DB ヘルパー 等）と照合
4. 逸脱ファイルごとに提示・確認・修正

→ ステップ5 へ

---

### ステップ5: 完了報告

#### 処理

1. 再コピーした静的テンプレファイル一覧を表示
2. 規約検査で修正したファイルと修正内容の一覧を表示
3. 差分を `git diff` でユーザーに確認させる
4. 提案コミットメッセージを提示し、コミットはユーザーに委ねる
   - 提案例: `chore: sync dev-kit generated artifacts to v{N}`
   - バージョンは `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` から取得

→ 完了

#### 注意

##### 禁止事項

- master / main への直接コミット
- ユーザー確認なしでの修正（規約検査の修正はすべてユーザーが承認する）
