<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# glob パターンに `**/` 前置忘れ（PR140）

## 何が起きたか

「`tools/` 配下の Python ファイルには `python-script.md` を引き込む」という rule を追加するとき、AI は以下のように書いた:

```yaml
- pattern: "tools/**/*.py"
  required: [scripts/python-script.md]
```

ユーザーが即指摘：**「**/tools/ ってしなくていいの？」**

`tools/**/*.py` パターンは **プロジェクトルート直下の** `tools/foo.py` / `tools/sub/bar.py` にしかマッチしない。モノレポ構造の `packages/foo/tools/bar.py` や `apps/web/tools/script.py` には **マッチしない**。AI は py-kit がマルチパッケージリポジトリに適用される可能性を考慮していなかった。

`**/tools/**/*.py` に修正（任意の深さでマッチ）。

## 根本原因

「慣習的なフォルダ名（tools, scripts, tests, gui 等）」のパスパターンを書く時、AI はルート相対思考でデフォルトを書いてしまった。しかし:

- 多くの実プロジェクトはモノレポ（複数パッケージルート）
- 非モノレポでもヘルパーフォルダはネストする（例: `backend/services/api/tools/`）
- PR140 は py-kit 向け — py-kit はリポレイアウトに意見を持たない。フラット / ネスト両対応が必須

## 教訓

**glob rules の「フォルダ名」パターンは、デフォルトで `**/` を前置する。**

| パターン | マッチ範囲 | 使うべき場合 |
|---|---|---|
| `tools/**/*.py` | ルート直下の `tools/` のみ | ネストされた `tools/` を意図的に除外したい時 |
| `**/tools/**/*.py` | 任意の深さの `tools/` | デフォルト — フラットでもモノレポでも動く |
| `src/tools/**/*.py` | `src/tools/` のみ | 特定の場所だけを対象にしたい時 |

適用対象: `tools/`, `scripts/`, `tests/`, `gui/`, `benchmarks/`, `perf/` など慣習的フォルダ名すべて。ルート固定パターンは **プロジェクトルートに必ずある** ファイル（`.env`, `pyproject.toml`, `tsconfig.json` 等）にだけ使う。

## 関連

- PR140 修正: コミット f1fd5ac
- 参考: `plugins/py-kit/references/injection_rules.yaml` — ほとんどのフォルダ名パターンが `**/` を使用
