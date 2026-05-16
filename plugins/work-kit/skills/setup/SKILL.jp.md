# SKILL.jp.md — work-kit:setup スキル（日本語ミラー）

> このファイルは `SKILL.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `SKILL.md` にも反映してください。

---

**スキル名**: setup
**トリガー**: ユーザーが `/work-kit:setup` を実行したとき（自動起動なし）

---

## 概要

work-kit プラグインのフックスクリプトを現在のプロジェクトにインストールし、
`.claude/settings.json` にフック設定を追加するスキル。

インストール完了後の動作:
- `UserPromptSubmit`: プロンプト送信のたびに PR タスク状況を Claude の context に注入
- `Stop`: 未完了タスクがあれば応答完了時にリマインドを context に注入

---

## 作業内容

### ステップ1: インストール先を準備する

#### 条件

- 常に — 他の何より先に実行する

#### 入力

- カレントディレクトリ（プロジェクトルート）

#### 処理内容

1. カレントディレクトリが Git リポジトリであることを確認する
2. `.claude/hooks/work-kit/` ディレクトリを作成する

```bash
mkdir -p .claude/hooks/work-kit
```

→ ステップ2へ進む

#### 出力

- `.claude/hooks/work-kit/` ディレクトリが存在する

#### 補足

##### 条件分岐

- Git リポジトリでない → 中断してユーザーに確認

---

### ステップ2: フックスクリプトをコピーする

#### 条件

- ステップ1が完了していること

#### 入力

- プラグインの `scripts/` ディレクトリ内のスクリプト
  （`[スキルディレクトリ]/../../scripts/` — SKILL.md では `${CLAUDE_SKILL_DIR}` 変数で解決される）

#### 処理内容

1. `user-prompt-submit.py` をプロジェクトの `.claude/hooks/work-kit/` にコピーする
2. `stop.py` をプロジェクトの `.claude/hooks/work-kit/` にコピーする

→ ステップ3へ進む

#### 出力

- `.claude/hooks/work-kit/user-prompt-submit.py` コピー済み
- `.claude/hooks/work-kit/stop.py` コピー済み

---

### ステップ3: settings.json にフック設定を追加する

#### 条件

- ステップ2が完了していること

#### 入力

- `.claude/settings.json`（存在しない場合は `{}` から作成）

#### 処理内容

1. `.claude/settings.json` を読み込む
2. 既存の `hooks` キーとマージする（上書きしない）
3. 以下の設定を追加する:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/work-kit/user-prompt-submit.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/work-kit/stop.py"
          }
        ]
      }
    ]
  }
}
```

4. `.claude/settings.json` を保存する

→ ステップ4へ進む

#### 出力

- `.claude/settings.json` に work-kit フック設定が追加済み

#### 補足

##### 禁止事項

- 既存の `hooks` エントリを削除しない — マージするだけ
- `UserPromptSubmit` / `Stop` キーが既にある場合は配列に追記する

---

### ステップ4: インストール確認

#### 条件

- 全ファイルが作成・更新済みであること

#### 処理内容

1. 作成したファイルの存在を確認する
2. ユーザーにインストール完了を報告する

#### 出力

- インストール完了レポート

#### 補足

##### チェックリスト

- [ ] `.claude/hooks/work-kit/user-prompt-submit.py` — 存在する
- [ ] `.claude/hooks/work-kit/stop.py` — 存在する
- [ ] `.claude/settings.json` — `UserPromptSubmit` / `Stop` フック設定あり

---

## 参考資料

### フック動作の概要

| フックイベント | タイミング | 動作 |
|---|---|---|
| `UserPromptSubmit` | ユーザーのプロンプト送信後、Claude が処理する前 | PR タスク状況を context に注入 |
| `Stop` | Claude が応答を完了したとき | 未完了タスクがあればリマインドを context に注入 |

### 対応表

| ファイルパス | 概要 |
|---|---|
| `.claude/hooks/work-kit/user-prompt-submit.py` | UserPromptSubmit フックスクリプト |
| `.claude/hooks/work-kit/stop.py` | Stop フックスクリプト |
| `.claude/settings.json` | フック設定（hooks キー） |
| `docs/tasks/**/PR{N}.md` | フックスクリプトが参照する PR タスクドキュメント |
