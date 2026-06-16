# .gitignore / .gitattributes の Edit/Write 禁止

> ブランチ: `feat/gitignore-edit-guard`

## 概要

`.gitignore` と `.gitattributes` への Edit / Write 経路をブロックする。
既存の `delete-guard.py` は Bash `rm` / `rmdir` を防ぐが、Edit ツールで
全行を消したり Write ツールで空ファイルを上書きする経路は通る。これを
`dotgit-lockfile-guard.py` の対象パスに追加して塞ぐ。

`.gitignore` が消えると tracked にすべきでないファイル (実行時 YAML、
ローカル設定、ビルド成果物) が一気に working tree に湧くため、Claude 由来の
事故を恒久ブロックしたい。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | - | 未解決事項を `## QA` に記録する |
| 2 | - | `dotgit-lockfile-guard.py` のパス判定に `.gitignore` / `.gitattributes` を追加 |
| 3 | - | `dotgit-lockfile-guard.md` のメッセージ本文に追記 |
| 4 | - | 手動テスト (Edit/Write 対象でブロック、他は通過) |
| 5 | - | `.work/notes/hooks/dotgit-lockfile-guard.md` を更新 |
| 6 | - | `plugin.json` / `marketplace.json` の version bump |

## 仕様

ブロック対象 (basename 完全一致) を追加:

| No | ファイル名 | 既存 (delete-guard rm) | 今回追加 (dotgit-lockfile-guard Edit/Write) |
|---|---|---|---|
| 1 | `.gitignore` | ✅ | ✅ |
| 2 | `.gitattributes` | ✅ | ✅ |

判定方法は既存ロックファイルと同じく `basename(file_path) == "..."` の完全一致。
`.gitignore.bak` や `foo.gitignore` は対象外（衝突防止）。

ブロック方針: 永久ブロック（ワンタイムトークンなし、既存ロックファイルと同方針）。

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/hooks/dotgit-lockfile-guard.py` | 編集 | `_DOTFILE_NAMES` (新) を追加し `_is_dotfile_path()` で判定 | basename 完全一致 |
| 2 | `plugins/work/hooks/dotgit-lockfile-guard.md` | 編集 | ブロック対象に `.gitignore` / `.gitattributes` を明記 | |
| 3 | `plugins/work/.claude-plugin/plugin.json` | 編集 | version bump | |
| 4 | `.claude-plugin/marketplace.json` | 編集 | work エントリの version bump | |
| 5 | `.work/notes/hooks/dotgit-lockfile-guard.md` | 編集 | 適用範囲表に 2 行追加 | |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `.gitignore` への Edit で deny 出力 | (未実施) | - |
| 2 | `.gitignore` への Write で deny 出力 | (未実施) | - |
| 3 | `.gitattributes` への Edit で deny 出力 | (未実施) | - |
| 4 | `.gitignore.bak` (派生名) は通過 | (未実施) | - |
| 5 | `foo/.gitignore` (サブディレクトリ) も deny | (未実施) | - |
| 6 | `.git/HEAD` 既存ガードに影響なし | (未実施) | - |
| 7 | 通常ファイル (`foo.py`) は通過 | (未実施) | - |

## 参考リンク

- `plugins/work/hooks/dotgit-lockfile-guard.py`: 拡張対象の Edit/Write ガード
- `plugins/work/hooks/delete-guard.py`: 既に `.gitignore` を Bash `rm` 経路でカバー (今回拡張不要)
- `.work/notes/hooks/dotgit-lockfile-guard.md`: 既存ガード仕様ノート
