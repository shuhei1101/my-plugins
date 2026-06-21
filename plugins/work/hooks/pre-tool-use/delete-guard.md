# 削除ガード: ブロック

重要ファイル/ディレクトリへの削除操作はブロックされています。

- `.git` — リポジトリ管理に不可欠。削除するとリポジトリが破損する
- `.claude` — 設定・ルール・プラグインキャッシュが失われる
- `.gitignore` — 消失すると build artifacts や node_modules が tracked 扱いになり大量誤コミットの原因になる
- `.gitattributes` — マージドライバや改行設定が失われる
- lock ファイル（`package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `npm-shrinkwrap.json` / `Cargo.lock` / `Gemfile.lock` / `Pipfile.lock` / `poetry.lock` / `uv.lock` / `composer.lock` / `go.sum`）
  — 依存解決の SoT。削除するとビルド再現性が失われる

このブロックは解除できません。別の方法を検討してください。
