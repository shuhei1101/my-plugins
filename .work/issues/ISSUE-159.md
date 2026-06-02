# ISSUE-159: apply-statusline.py の Path.home() がモジュールレベルで定数化されており cross-env リスクが不透明

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/claude-kit/scripts/apply-statusline.py` の 9 行目で `SETTINGS_PATH = Path.home() / ".claude" / "settings.json"` がモジュールレベルの定数として宣言されている。

インシデント #22 (`path-home-cross-env-mismatch`) が示すように、`Path.home()` は Claude Code が動作する Python 環境に依存する。WSL Python と Windows ネイティブ Python では `home()` が返すパスが異なるため、誤った環境で実行すると別の `settings.json` を書き換え、変更が無音で無効になる。

SKILL.md (`statusline-setup/SKILL.md`) には環境確認の警告注記があるが、スクリプト本体には実行時チェックも警告出力もなく、`SETTINGS_PATH` が定数のためデバッグが難しい。

## 対応方針

`SETTINGS_PATH` をモジュール定数から `main()` 内ローカル変数に移動し、実行時に `Path.home()` を呼ぶ。あわせて、設定ファイルパスを stderr に表示し、どの環境のファイルを書き換えているかを実行時に確認できるようにする。

## 対象ファイル

- `plugins/claude-kit/scripts/apply-statusline.py`: `SETTINGS_PATH` を `main()` 内に移動し、適用前にパスを stderr 出力する

