# py-kit / next-kit 注入フック修正メモ

## 問題

`inject_references.py` がマッチした reference ファイルの**本文全体**を `decision: block` の reason に注入していた。
複数の Python ファイルを読み込む調査フェーズで、ファイルごとに大量のリファレンス本文が注入され、
コンテキストを大きく圧迫していた。

## 修正内容（PR147）

| 変更 | 内容 |
|---|---|
| テンプレート | Required セクションを `path + description` のみに変更（`{{ ref.body }}` を削除） |
| テンプレート | Summary セクションを削除（冗長） |
| テンプレート | 冒頭文を「編集しようとしています」から中立的な表現に変更 |
| inject_references.py | `_read_ref()` から body 読み込みを削除（未使用コード除去） |
| Read マッチャー | **維持**（issue-scan などの読み取り経路でも reference の案内を受けられるため） |

## 設計方針

- フックは「どの reference を読むべきか」を案内するだけ
- reference の本文は Claude が必要なものを `Read` で自分で読む
- Read マッチャーを残すことで、ファイル調査時にも適切な reference へ誘導できる
- body を注入しないため、Read が複数回発火しても軽い（path + description のみ）
