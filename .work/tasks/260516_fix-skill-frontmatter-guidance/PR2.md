# PR2 — fix-skill-frontmatter-guidance

## 仕様参照

<!-- 関連仕様書なし -->

## TODO

- [x] `claude-kit/references/file-types.jp.md` の `disable-model-invocation` 説明を「基本使わない」に更新
- [x] `claude-kit/references/file-types.md`（英語本体）を同期
- [x] `claude-kit/skills/skill-creator/SKILL.jp.md` のフロントマター説明を `name` + `description` のみに変更
- [x] `claude-kit/skills/skill-creator/SKILL.md`（英語本体）を同期
- [x] `work-kit/skills/merge/SKILL.md` から `allowed-tools` を削除
- [x] `work-kit/skills/work-start/SKILL.md` から `allowed-tools` を削除
- [x] `work-kit/skills/setup/SKILL.md` から `allowed-tools` と `disable-model-invocation` を削除
- [x] work-kit バージョンバンプ（plugin.json + marketplace.json）
- [x] `file-types.jp.md` / `file-types.md`: disable-model-invocation に「人間のみが実行すべきスキルには使う」を追記
- [x] `skill-creator/SKILL.jp.md` / `SKILL.md`: 同様に例外ケースを追記
- [x] `work-kit/skills/merge/SKILL.md`: `disable-model-invocation: true` を復活
- [x] work-kit バージョンバンプ（2.3.3 → 2.3.4）

## 変更ファイル

- `plugins/claude-kit/references/file-types.jp.md`: disable-model-invocation を基本不使用に変更
- `plugins/claude-kit/references/file-types.md`: 同上（英語本体）
- `plugins/claude-kit/skills/skill-creator/SKILL.jp.md`: フロントマター案内を name+description のみに更新
- `plugins/claude-kit/skills/skill-creator/SKILL.md`: 同上（英語本体）
- `plugins/work-kit/skills/merge/SKILL.md`: allowed-tools 削除
- `plugins/work-kit/skills/work-start/SKILL.md`: allowed-tools 削除
- `plugins/work-kit/skills/setup/SKILL.md`: allowed-tools + disable-model-invocation 削除
- `plugins/work-kit/.claude-plugin/plugin.json`: 2.3.3
- `.claude-plugin/marketplace.json`: work-kit 2.3.3

## QA

なし
