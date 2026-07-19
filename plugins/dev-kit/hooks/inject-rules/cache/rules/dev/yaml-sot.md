# Yaml SoTルール

## 概要

- 新規ドメインのデータ管理は YAML を SoT として持ち、`index.yaml` + `settings.yaml` の 2 段構成を使う ことを必須化する。
- frontend / backend が同じ YAML を見て同じ識別子で実装できることと、Claude Code がデータの全貌を 1 箇所で把握できる
  - 散らばらない ことが目的。

## 必須化する 2 段構成

| ファイル                  | 役割                                                | git        | 編集経路              |
| ------------------------- | --------------------------------------------------- | ---------- | --------------------- |
| `**/index.yaml`           | キー本体 — 環境非依存 / 構造定義 / 一覧性が要るもの | committed  | 手編集                |
| `**/settings.yaml`        | 付随メタデータ — 画面から更新する / 環境別 / 個人差 | gitignored | UI または手編集       |
| `**/settings.yaml.sample` | `settings.yaml` の committed template               | committed  | 手編集 (新キー追加時) |

### どっちに書くかの判断

- 配信者が画面ポチポチで変える → `settings.yaml`
- ファイル追加と同時に増える本質的なキー → `index.yaml`
- git で全員揃ってほしい値 → `index.yaml` または `settings.yaml.sample`

「画面更新もなく環境依存もない」単独 YAML (例: `config/banned_words.yaml`) は 2 段にせず単独 YAML で OK。
2 段が必須になるのは「画面から更新」or「環境別」が発生するとき。

## frontend / backend は同じ YAML を読む

- 物理 ID と論理名 を YAML 1 箇所で定義し、Python / JS の両方が `/api/dev/catalog/...` 経由で同じ値を取る
- コード内ハードコード禁止 — YAML に未登録のキーが必要になったら YAML を先に更新する
- 表記が乖離する事故を構造的に潰すのが目的

## worktree-safe な runtime YAML

`settings.yaml` 等、実行時に UI / API から書き込まれる YAML は、どの worktree から書いても main repo の同一ファイル に着地させる。
worktree 削除でユーザーデータが消える事故 を防ぐため。

以下例では (`main_repo_root()` ヘルパ) を採用:

```python
from aituber.core.paths import main_repo_root
path = main_repo_root() / "config" / "settings.yaml"
```