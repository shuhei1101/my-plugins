# SKILL.jp.md — work-kit:setup スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: setup
**トリガー**: ユーザーが `/work-kit:setup` を実行したとき（自動起動なし）

---

## 概要

work-kit のプロンプトファイルをプロジェクトにコピーするスキル。
フック設定（hooks.json）はプラグインインストール時に自動で適用されるため、
このスキルはプロンプトファイルの配置だけを担う。

インストール後の動作:
- `UserPromptSubmit`: `prompts/user-prompt-submit.md` の内容が毎回 Claude に渡される
- `Stop`: `prompts/stop.md` の内容が応答完了時に Claude に渡される

---

## 作業内容

### ステップ1: インストール先を準備する

#### 条件

- 常に — 他の何より先に実行する

#### 処理内容

1. `.claude/hooks/work-kit/prompts/` ディレクトリを作成する

```bash
mkdir -p .claude/hooks/work-kit/prompts
```

→ ステップ2へ進む

#### 出力

- `.claude/hooks/work-kit/prompts/` ディレクトリが存在する

---

### ステップ2: プロンプトファイルをコピーする

#### 条件

- ステップ1が完了していること

#### 入力

- プラグインの `prompts/` ディレクトリ内のファイル
  （SKILL.md では `${CLAUDE_SKILL_DIR}/../../prompts/` として解決される）

#### 処理内容

1. `user-prompt-submit.md` をプロジェクトの `.claude/hooks/work-kit/prompts/` にコピーする
2. `stop.md` をプロジェクトの `.claude/hooks/work-kit/prompts/` にコピーする

→ ステップ3へ進む

#### 出力

- `.claude/hooks/work-kit/prompts/user-prompt-submit.md` コピー済み
- `.claude/hooks/work-kit/prompts/stop.md` コピー済み

---

### ステップ3: インストール確認

#### 条件

- 全ファイルがコピー済みであること

#### 処理内容

1. コピーしたファイルの存在を確認する
2. ユーザーにインストール完了を報告する

#### 補足

##### チェックリスト

- [ ] `.claude/hooks/work-kit/prompts/user-prompt-submit.md` — 存在する
- [ ] `.claude/hooks/work-kit/prompts/stop.md` — 存在する
