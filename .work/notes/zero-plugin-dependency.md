# プラグイン間依存ゼロ — 棚卸しノート

PR210 で原則セクションを追加。本ノートは棚卸し作業（PR213）の記録用。

## 原則の要約

全プラグインは独立した配布単位として設計する。他プラグインのスキル・コマンド・スクリプトパスへの依存は極力ゼロにする。

### 許容される例外

- 同プラグイン内のスキル同士の呼び出し
- `ref-inject:apply` による静的テンプレ展開（配布先プラグインに閉じる）
- `claude-kit` の references injection 機構（他プラグインが opt-in で取り込む形）

### 禁止される依存

- skill A の手順内で `/other-plugin:skill-B` を呼ぶ
- hook が他プラグインのスクリプトパスを直接参照する
- reference が他プラグインのコマンドを「実行してから戻れ」と指示する

## 違反検出コマンド

```bash
# 他プラグインスキル呼び出し
grep -rn "/[a-z-]\+:[a-z-]\+" plugins/*/skills/ plugins/*/references/

# hook の他プラグインパス参照
grep -rn "CLAUDE_PLUGIN_ROOT.*\.\." plugins/*/hooks/
```

## 棚卸し結果（PR213 で記録）

作業中に更新する。
