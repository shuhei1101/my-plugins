<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# path-home-cross-env-mismatch

## 何が起きたか

ステータスラインのバグ調査中、`apply-statusline.py` を WSL の Python で実行したが、ユーザーの Claude Code は Windows ネイティブで動いていた。

`apply-statusline.py` は `Path.home() / ".claude" / "settings.json"` に書き込む。実行環境によって書き込み先が変わる:
- WSL Python: `/home/{user}/.claude/settings.json`
- Windows native Python: `C:\Users\{user}\.claude\settings.json`

WSL から実行した結果、WSL 側 settings.json は更新されたが、Windows ネイティブで動く Claude Code が読む `C:\Users\...\settings.json` には何も反映されなかった。**エラーも警告も出ないため、変更が反映されないのに「適用済み」と思い込んでしまった**。

## なぜ起きたか

- `Path.home()` の挙動が実行環境依存であることを意識していなかった
- スクリプト実行のフィードバック（`statusLine applied to ...`）が「Windows 側に適用された」と誤認しやすい出力だった
- ユーザーが WSL 環境であることを早期に確認せず、書き換え先のパスを検証しなかった

## 修正

ユーザーから「WSL 環境や」と教えてもらい、書き換え先を `/home/shuhei2441/.claude/settings.json` に固定して修正した。
SKILL.md / SKILL.jp.md に「実行環境（WSL/Windows）を見極めて、Claude Code と同じ Python 環境からスクリプトを実行すること」という注意事項を追記した。

## 再発防止

`Path.home()` などプラットフォーム依存のパスを使うスクリプトを作る・実行するときは:
1. **実行前**: Claude Code の `Platform` (linux=WSL / win32=Windows) を確認する
2. **書き換え先を出力**: スクリプトは絶対パスで書き換え先を出力し、ユーザーが間違いに気付けるようにする
3. **動作確認**: 書き換え後、Claude Code 側で実際に変更が反映されているか別経路で確認する

クロスプラットフォーム環境（WSL + Windows）で動くスクリプトを作る場合、SKILL.md / README に環境による挙動差を明記すること。
