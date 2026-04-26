# PR1: assets/ → examples/ リネーム & 内容を具体例に書き直し

## 概要

全プラグインの `assets/` フォルダを `examples/` にリネームし、ファイル内容もプレースホルダー形式のテンプレートから「具体的な記載例」形式に書き直す。

公式 Claude Code ドキュメントに合わせて `examples/` に統一することで、AI が few-shot 的に参照しやすい構成にする。

## 変更対象プラグイン

- `py-wizard/assets/` → `examples/`（2ファイル）
- `skill-wizard/assets/` → `examples/`（8ファイル）
- `wiki-wizard/assets/` → `examples/`（5ファイル）

## 作業内容

- [ ] git worktree 作成（ブランチ: `1/assets-to-examples`）
- [ ] py-wizard: assets/ → examples/ リネーム + 内容を具体例に書き直し
- [ ] skill-wizard: assets/ → examples/ リネーム + 内容を具体例に書き直し
- [ ] wiki-wizard: assets/ → examples/ リネーム + 内容を具体例に書き直し
- [ ] SKILL.md / references/ 内の `assets/` 参照を `examples/` に一括置換
- [ ] skill-wizard の file_organization.md の説明文も更新（assets/ の説明を examples/ に変更）

## テスト観点

- 全 SKILL.md と references/ 内に `assets/` への参照が残っていないこと
- `examples/` フォルダが各スキルに存在し、ファイルが揃っていること
