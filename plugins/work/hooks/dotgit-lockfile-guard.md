# dotgit / lockfile ガード: ブロック

`.git/**` 配下、および主要パッケージマネージャの lock ファイルへの Edit / Write はブロックされています。

- `.git/**` — リポジトリ内部状態。直接編集すると壊れる。Git CLI 経由でのみ操作する
- lock ファイル（`package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `npm-shrinkwrap.json` / `Cargo.lock` / `Gemfile.lock` / `Pipfile.lock` / `poetry.lock` / `uv.lock` / `composer.lock` / `go.sum`）
  — パッケージマネージャ CLI が再生成する前提。手編集すると依存解決の整合性が崩れる

このブロックは解除できません。CLI 経由（`git ...` / `npm install` / `uv sync` 等）で操作してください。
