# aituber-notify (Claude Code plugin)

Claude Code の `Stop` hook で AITuber 本体 (`http://localhost:8080`) の `/api/notify/completion` を叩き、琴葉茜に作業完了を音声で報告させる plugin。

## 仕組み

1. Claude Code セッション終了 → Stop hook 発火 → `scripts/notify.ps1` 実行
2. `notify.ps1` が hook payload から `transcript_path` を取得
3. transcript JSONL を解析:
   - `ai-title` エントリ → `summary`（Claude がセッションに付けたタイトル）
   - `file-history-snapshot` の最初の `timestamp` → `duration_sec`（所要時間）
   - `transcript_path` のフォルダ名 → `project`（プロジェクト名）
4. `curl POST http://localhost:8080/api/notify/completion`
5. AITuber 未起動 / 接続不能時は **silent fail（exit 0）**— Claude Code を妨げない

## インストール

### 1. marketplace を追加（初回のみ）

```bash
/plugin marketplace add ./my-plugins
```

### 2. プラグインをインストール

```bash
/plugin install aituber-notify@my-plugins
```

スコープ選択: **User**（全プロジェクトで有効にする場合）または **Local**（このプロジェクトのみ）

### 3. AITuber を起動

```bash
python src/aituber/main.py  # port 8080
```

### 4. 動作確認

```bash
# hooks.json に書いたコマンドを手動テスト
echo '{"transcript_path": null}' | powershell -ExecutionPolicy Bypass -File my-plugins/aituber-notify/scripts/notify.ps1
```

AITuber が起動していれば茜が話す。未起動でも exit 0 で終了する。

## 構成

```
aituber-notify/
  plugin.json           # Claude Code plugin manifest
  hooks/
    hooks.json          # Stop hook 設定
  scripts/
    notify.ps1          # 通知スクリプト本体 (PowerShell 7+)
  README.md             # このファイル
```

## 関連ドキュメント

- `aituber/wiki/作業完了通知設計.md` §7 — 本 plugin の設計ドキュメント
- `aituber/src/aituber/server/routes/notify.py` — 受け口エンドポイント (PR214)
- `aituber/docs/PR/PR275.md` — 実装 PR ドキュメント
