<!-- This file is a Japanese mirror of git-guard-false-positive-file-content.md. When updating the English original, update this file too. -->
# git-guard フックがコマンド文字列テキストに誤反応

**日付**: 2026-05-30
**カテゴリ**: tool-misuse

## 何が起きたか

git-guard フック（`PreToolUse(Bash)`）はBashコマンド文字列全体を検索する。引数・ファイル内容・サマリーテキストなど、「git push」「git merge」という文字列がどこに出現しても発動する。

**ケースA — シェルヒアドキュメント**（2026-05-30）:
```bash
cat > plugins/work/.claude-plugin/plugin.json << 'EOF'
{
  "description": "...guards git push/merge confirmation..."
}
EOF
```
ファイル本文がコマンド文字列に含まれるため、リテラル "git merge" がブロックを引き起こした。

**ケースB — Pythonコマンド引数**（2026-05-30）:
```bash
python index-tool.py add ... --summary "git merge master/main は許可..."
python -c "..." "git-guardフックを修正し、git merge master/mainは許可..." "session-id"
```
`--summary` や位置引数の値に "git merge" がテキストとして含まれるだけでガードが発動する（実際のgitコマンドではなくても）。

## 回避策

1. **リフレーズ**: 引数やファイル内容で "git push" / "git merge" の文字列を避ける（例: "マージ"、"ギットマージ"、"force-operations"）。
2. **Pythonファイル書き込み**: ヒアドキュメントの代わりにPython APIでファイルを書く。
3. **WORK_GUARD=false**: 偽陽性が避けられない場合は環境変数でガードを一時的に無効化する。

## コンテキスト

git-guard の正規表現（`r"\bgit\s+(push|merge)\b"`）はBashコマンド文字列全体（引数や埋め込みコンテンツを含む）を検索する。コマンドとしての "git merge" と、テキストとして議論している "git merge" を区別できない。
