# reload-pluginsの自セッション遅延実行

> ブランチ: `fix/reload-self-deferred`

## 概要

`reload_plugins.py` は起動中の全 tmux セッションに `/reload-plugins` を送信するが、マージを実行した自セッションはターン処理中のため入力を取りこぼす。
自セッション宛は即時送信せず保留トークンを書き、Stop フック（ターン終了時）でバックグラウンド遅延送信する方式に変更する。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `reload_plugins.py` で自セッションを検出し、保留トークン（`tokens/work/reload-pending/`）を書く |
| 2 | 済 | Stop フック `reload_deferred.py` を新規作成（保留トークン消費 → 遅延 send-keys） |
| 3 | 済 | `hooks.json` に Stop エントリを追加 |
| 4 | 済 | work プラグインのバージョンバンプ（1.3 → 1.4） |
| 5 | 済 | `.work/notes/` の関連ノートを更新する |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 |
|---|---|---|---|
| 1 | `tools/reload_plugins.py` | 編集 | 自セッション検出 + 保留トークン書き込み |
| 2 | `plugins/work/hooks/reload_deferred.py` | 新規 | Stop フック: 保留トークンがあれば遅延 send-keys |
| 3 | `plugins/work/hooks/hooks.json` | 編集 | Stop エントリ追加 |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | 自セッション検出が tmux 内で正しく動く | `_own_session()` が `plg-1` を返すことを確認 | OK |
| 2 | reload_deferred が保留トークンを消費して遅延送信する | ダミーセッション wttest でトークン消費と send-keys 到達を確認 | OK |
| 3 | 保留トークンがないとき何もしない | 出力なし exit 0 を確認 | OK |
