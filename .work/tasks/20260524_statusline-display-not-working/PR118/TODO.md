# PR118 — statusline-display-not-working

## 概要

commit 4144128（feat: statusline-ctx-green #PR116）マージ後、ステータスラインが表示されなくなった問題を調査・修正する。

**真因**: PR116 とは無関係。`r5["resets_at"]` のネストされたダブルクォートが `python -c "..."` の外側を切ってしまうバグ（古くから存在）。`rate_limits.resets_at` が入った瞬間に NameError で落ちていた。

### 実施条件

即時実施可

### 関連PR

| PR番号 | 概要 |
|---|---|
| #116 | ctx 50%未満に緑色表示を追加（バグ原因コミット） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260524_statusline-display-not-working/PR118/QA.md` |
| 済 | バグの原因を特定する（apply-statusline.py の動作・settings.json の状態確認） | - `plugins/claude-kit/scripts/apply-statusline.py` |
| 済 | 修正を実施する（resets_at の `.get()` 化 + 緑機能維持） | - `plugins/claude-kit/scripts/apply-statusline.py` |
| 済 | テストして statusline が表示されることを確認する | - `/home/shuhei2441/.claude/settings.json` |
| 済 | SKILL.md / SKILL.jp.md に環境注意事項（WSL/Windows 切り分け）を追記 | - `plugins/claude-kit/skills/statusline-setup/SKILL.md`, `SKILL.jp.md` |
| 済 | plugin.json と marketplace.json のバージョンバンプ（3.22.2） | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/claude-kit/skills/statusline-setup/SKILL.md`: statusline-setup スキルの仕様
- `.work/notes/statusline-display-bug.md`: バグ調査メモ

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| - | - | - |
