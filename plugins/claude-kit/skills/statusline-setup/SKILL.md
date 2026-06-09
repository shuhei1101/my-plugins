---
name: claude-kit:statusline-setup
description: |
  ユーザーが「ステータスラインを設定して」「statusline-setup を実行して」「ステータスラインをセットアップして」と言ったとき。
  または `/statusline-setup` で明示的に呼ばれたとき。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# statusline-setup — ステータスライン設定を適用する

`~/.claude/settings.json` の `statusLine` キーを定義済みの設定値に書き換える。

---

## 概要

Claude Code のステータスラインには、モデル名・コンテキスト使用率・レート制限状況をカラー付きで表示する Python コマンドを設定できる。
このスキルは `apply-statusline.py` スクリプトを実行するだけで、以下の表示設定を適用する。

**表示例**:
```
my-plugins/ | Claude Sonnet 4.6 | ctx 23% (47k/200k)
5h 12% (~14:30) | 7d 8% (~05/20)
```

**適用される設定内容**:
- 行1: `ワークスペース名/ | モデル名（色付き）| ctx XX%（50%未満で緑、50%以上で黄色、70%以上で赤）`
- 行2: `5h XX%（5時間レート） | 7d XX%（7日レート）`（使用率に応じて色変化）
- モデル色: opus → 赤、sonnet → 黄色

---

## タスク

### ステップ1: スクリプトを実行する

#### 条件

- 常に実行

#### 処理

以下のコマンドを実行する:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/apply-statusline.py"
```

→ ステップ2へ進む

#### 出力

- `~/.claude/settings.json` の `statusLine` キーが更新される

#### 注意事項

##### 実行環境の注意（重要）

スクリプトは `Path.home() / ".claude" / "settings.json"` に書き込む。実際のパスは呼び出す Python によって変わる:

| 実行環境 | 書き込み先 settings.json |
|---|---|
| WSL の Python | `/home/{ユーザー}/.claude/settings.json` |
| Windows ネイティブの Python | `C:\Users\{ユーザー}\.claude\settings.json` |

Claude Code は自身の実行環境に対応するパスから設定を読み込む。**Claude Code と同じ Python 環境からスクリプトを実行すること** — そうしないと Claude Code が読まない settings.json を書き換えてしまい、変更が反映されない（しかもエラーは出ない）。

実行前に環境を確認する:
- Claude Code の `Platform` が `linux`（WSL）→ WSL の `python` で実行
- Claude Code が Windows ネイティブ → Windows の `python`（PowerShell / cmd）で実行

##### 条件分岐

- スクリプトがエラーを返した場合 → エラーメッセージをユーザーに報告して終了

---

### ステップ2: 結果を報告する

#### 条件

- ステップ1 完了

#### 処理

1. 適用完了をユーザーに伝える
2. Claude Code を再起動しないと反映されない場合があることを案内する

#### 出力

- 完了メッセージ
