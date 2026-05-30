<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# マージスキル ↔ 仕様書ステップ番号同期

`.work/specs/work-kit-merge-flow.md` はマージスキルのアーカイブフローをステップ番号で参照している。
`SKILL.md` でステップを追加・削除した場合、同じコミットで仕様書のステップ番号参照も更新すること。
英語原文: `references/work-merge-skill-sync.md`

---

## ファイルの依存関係

| 変更 | 確認・更新が必要なファイル |
|---|---|
| `plugins/work/skills/merge/SKILL.md` のステップ追加・削除 | `.work/specs/work-kit-merge-flow.md` のステップ番号参照 |
| `plugins/work/skills/merge/SKILL.jp.md` の更新 | `SKILL.md` も同じコミットで更新（JP ミラー） |
| `.work/specs/work-kit-merge-flow.md` のステップ番号変更 | `SKILL.md` の実際のステップと一致しているか確認 |

## 背景

PR92 でステップを挿入した際、仕様書が「Step 4〜6」と記載したまま「Step 5〜7」にずれていた。
この不一致を再発させないためにこの同期ルールを追加した。

## コミット前チェックリスト

- [ ] `.work/specs/work-kit-merge-flow.md` のステップ番号が `SKILL.md` の実際のステップと一致している
- [ ] `SKILL.md` と `SKILL.jp.md` が同じコミットで更新されている
