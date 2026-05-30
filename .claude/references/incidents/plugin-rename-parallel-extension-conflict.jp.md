<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# プラグインリネームと並行拡張のコンフリクト

**日付**: 2026-05-30
**カテゴリ**: tool-misuse

## 何が起きたか

PR172（`plugins/work-kit/` → `plugins/workspace/` へのリネーム）の作業中、master では PR167 が進行しており、リネーム PR と並行して `plugins/work-kit/skills/config/SKILL.md` などの新スキルファイルが追加されていた。

PR172 ワークツリーで `git merge master` を実行したところ、git が以下のコンフリクトを報告した：

```
CONFLICT (file location): plugins/work-kit/skills/config/SKILL.md added in master
inside a directory that was renamed in HEAD, suggesting it should perhaps be moved to
plugins/workspace/skills/config/SKILL.md.
```

原因：
- PR172 が `git mv` で `plugins/work-kit/` → `plugins/workspace/` にリネームした
- master が独立して `plugins/work-kit/skills/config/` 以下に新ファイルを追加した
- git はリネーム後の新ファイルの配置先を自動解決できない

## 防止策

プラグインリネーム PR に master をマージする際：

1. `CONFLICT (file location)` メッセージで旧プラグインパスを参照しているものを確認する
2. コンフリクトしたファイルを手動で移動する：
   ```bash
   mkdir -p plugins/{新名称}/skills/{スキル名}/
   mv plugins/{旧名称}/skills/{スキル名}/SKILL.md plugins/{新名称}/skills/{スキル名}/SKILL.md
   mv plugins/{旧名称}/skills/{スキル名}/SKILL.jp.md plugins/{新名称}/skills/{スキル名}/SKILL.jp.md
   ```
3. 移動したファイル内の内部参照（`旧名称:` → `新名称:`）を更新する
4. 削除と追加をステージする：
   ```bash
   git rm plugins/{旧名称}/skills/{スキル名}/SKILL.md
   git rm plugins/{旧名称}/skills/{スキル名}/SKILL.jp.md
   git add plugins/{新名称}/skills/{スキル名}/
   ```
5. 新スキル名を参照する glossary エントリも更新する

## コンテキスト

プラグインフォルダをリネームする PR（`git mv plugins/old plugins/new`）と、同じプラグインにファイルを追加する並行 PR が存在する場合に発生する。教訓：プラグインリネームは並行 PR と調整するか、マージ時のロケーションコンフリクトを覚悟してから実施すること。
