# issue-resolve Step1をindex.yaml優先に変更

> ブランチ: `fix/issue-resolve-step1-index-first`

## 概要

### 実施条件

即時実施可

### 背景・目的

`work:issue-resolve` の Step 1 では `ISSUE-*.md` を全 glob してから `_index.yaml` でステータスを
照合していた。しかし `_index.yaml` にはすでに `status` フィールドが存在するため、
先に `_index.yaml` を読んで `not_started` エントリに絞り、そのイシューファイルだけを読む方が
自然で効率的。

---

## 作業内容

| 済 | タスク |
|---|---|
| 済 | `SKILL.md` Step 1 プロセスを `_index.yaml` 優先に変更 |
| 済 | `SKILL.jp.md` を同期（JP ミラー） |
| 済 | QA を記録する |
| 済 | ノートを更新する |

---

## 変更内容

| No | ファイル | 変更内容 |
|---|---|---|
| 1 | `plugins/work/skills/issue-resolve/SKILL.md` | Step 1: glob 先行 → `_index.yaml` 先行に変更 |
| 2 | 〃 | `SKILL.jp.md` | 〃（JP ミラー同期） |

---

## テスト

| No | 内容 | 結果 |
|---|---|---|
| 1 | Step 1 の記述が `_index.yaml` 優先になっているか読んで確認 | |

---

## QA

（なし）

---

## 参考ドキュメント

- [issue-resolve スキル設計メモ](../../notes/スキル設計/issue-resolveスキル.md)

---

## 関連ブランチ

（なし）

## 次ブランチ候補

（なし）
