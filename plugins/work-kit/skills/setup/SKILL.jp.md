# SKILL.jp.md — work-kit:setup スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: setup
**トリガー**: ユーザーが `/work-kit:setup` を実行したとき（自動起動なし）

---

## 概要

work-kit プラグインのフックスクリプトをプロジェクトにコピーする。
フック設定（hooks.json）はプラグインインストール時に自動で適用されるため、
このスキルはスクリプトファイルの配置だけを担う。

---

## 作業内容

### ステップ1: インストール先を準備する

#### 条件

- 常に — 他の何より先に実行する

#### 処理内容

1. `.claude/hooks/work-kit/` ディレクトリを作成する

```bash
mkdir -p .claude/hooks/work-kit
```

→ ステップ2へ進む

#### 出力

- `.claude/hooks/work-kit/` ディレクトリが存在する

---

### ステップ2: フックスクリプトをコピーする

#### 条件

- ステップ1が完了していること

#### 入力

- プラグインの `scripts/` ディレクトリ内のスクリプト
  （SKILL.md では `${CLAUDE_SKILL_DIR}/../../scripts/` として解決される）

#### 処理内容

1. `user-prompt-submit.py` をプロジェクトの `.claude/hooks/work-kit/` にコピーする
2. `stop.py` をプロジェクトの `.claude/hooks/work-kit/` にコピーする

→ ステップ3へ進む

#### 出力

- `.claude/hooks/work-kit/user-prompt-submit.py` コピー済み
- `.claude/hooks/work-kit/stop.py` コピー済み

---

### ステップ3: インストール確認

#### 条件

- 全ファイルがコピー済みであること

#### 処理内容

1. コピーしたファイルの存在を確認する
2. ユーザーにインストール完了を報告する

#### 補足

##### チェックリスト

- [ ] `.claude/hooks/work-kit/user-prompt-submit.py` — 存在する
- [ ] `.claude/hooks/work-kit/stop.py` — 存在する
