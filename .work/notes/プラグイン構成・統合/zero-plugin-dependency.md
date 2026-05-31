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

### 違反件数サマリー

| プラグイン | 違反ファイル | 内容 |
|---|---|---|
| work → claude-kit | `skills/notes-to-claude/SKILL.md`<br>`skills/notes-to-claude/SKILL.jp.md` | Step 3 でclaude-kit スキル群を必須ディスパッチ先として参照。Prerequisite にインストール必須を明記 |

### 許容対象（変更不要）

| プラグイン | 参照先 | 理由 |
|---|---|---|
| claude-kit → ref-inject | `/ref-inject:apply <plugin>` | 許容例外: 静的テンプレ展開 |
| changelogs の記述 | 各種スキル名 | 歴史的参考情報のみ |
| work → work 内 | work スキル間呼び出し | 同プラグイン内依存 |

### 修正方針（ユーザー確認待ち）

`notes-to-claude` スキルを「claude-kit なしでも動作できる」形に変更:
- Prerequisite 削除
- Step 3: クリエータースキル経由 → 直接ファイル作成・編集に変更（Rule の paths: フロントマター・JP ミラー仕様を内包）
- References の "Creator skill summary" セクション削除
- 関連スキル表の `claude-kit:claude-refactor` 行削除
