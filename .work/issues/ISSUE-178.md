# ISSUE-178: git-guard.py / master-commit-guard.py の正規表現がインシデント #20（false positive）に該当

**作成日**: 2026-06-02

## 問題

`git-guard.py` と `master-commit-guard.py` の正規表現が、コマンド本体だけでなく文字列を含む任意の bash コマンドにマッチする（インシデント #20 の再現）。例えば `echo "git push is needed"` や `grep "git commit" CHANGELOG.md` でガードが誤発火する。

インシデント #20（`git-guard-false-positive-file-content`）: コマンドガードは、マッチ文字列がファイル内容や部分文字列として現れた時に誤検知しうる。部分文字列ではなくコマンド本体にマッチさせる。

```python
# git-guard.py
if not re.search(r"\bgit\s+(push|merge)\b", command):
    return
# master-commit-guard.py
if not re.search(r"\bgit(\s+-C\s+\S+)?\s+commit\b", command):
    return
```

検証結果：
- `echo "git push is needed"` → マッチ（誤発火）
- `grep "git commit" CHANGELOG.md` → マッチ（誤発火）
- `git push origin feature` → マッチ（正常）

## 対応方針

コマンド文字列をセパレータ（`;` `&&` `||` 改行）で分割し、各セグメントの先頭コマンドが `git` かどうかを判定する。引用符内や引数内の文字列はスルーする。

## 対象ファイル

- `plugins/work/hooks/scripts/git-guard.py`: コマンド本体マッチに変更
- `plugins/work/hooks/scripts/master-commit-guard.py`: 同上

## QA

### QA-1: どの案で進めるか

A) セパレータ分割方式（各セグメント先頭コマンドを判定） / B) コマンド開始位置を意識した正規表現 / C) shlex.split 方式

**推奨**: A — 実際の bash 構文に即しており、パイプライン・セミコロン・&& 区切りすべてに対応できる

**回答**: <!-- A / B / C -->

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
