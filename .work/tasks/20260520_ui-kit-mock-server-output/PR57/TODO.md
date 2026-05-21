# PR57 — ui-kit-mock-server-output

## 概要

ui-kit:mock スキルの出力先を「常に `tmp/mocks/`」から「プロジェクト種別に応じた適切な場所」に変更する。
FastAPI などのサーバープロジェクトではサーバーが配信できる場所に HTML を置き、
生成後は空きポートでサーバーを起動してブラウザで即開けるURLをユーザーに通知するルールを追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | SKILL.jp.md を更新（Step 5・6 を改訂） | `plugins/ui-kit/skills/mock/SKILL.jp.md` |
| 済 | SKILL.md を更新（Step 5・6 を改訂） | `plugins/ui-kit/skills/mock/SKILL.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump する | `plugins/ui-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | コミットする | - |

## 参考ドキュメント

- `plugins/ui-kit/skills/mock/SKILL.md`: モックスキル定義
