<!-- This file is a Japanese mirror of CLAUDE.md. When updating the English original, update this file too. -->
# ref-inject プラグイン開発ガイド

`ref-inject` は**プラグインにリファレンス自動注入の仕組みを付与する**プラグイン。`dev-kit` /
`claude-kit` で使われている `*-kit` 形式の、編集対象パスを `_injection_rules.yaml` と照合して
関連リファレンスを注入する `PreToolUse` フックを付ける。対象プラグインは新規でも既存でもよく、
`/ref-inject:apply` は**注入部分だけ**を提供する。

共通ランタイムの共有はしない（そのやり方は却下済み —
`premature-cross-plugin-centralization` 参照）。代わりに `templates/` から**独立したファイル**を
コピーし、インシデントログが「コピペの方が安い」と認めたやり方を自動化する。

**生成スクリプトは持たない。** `/ref-inject:apply` は Claude が各テンプレートを読んで出力先
ファイルを自分で書き、その過程でプレースホルダを置換する。こうすることで構造がコンテキストに
残り、プラグインごとに調整しやすい。

### 責務範囲（このプラグインが所有しないもの）

`apply` スキルは**注入の仕組みだけ**に責務を絞る。プラグインレベルの関心事は `plugin-creator`
の領分でここには含まない:

- 対象プラグインの `plugin.json` を作成・編集しない
- 対象プラグインのルート `CLAUDE.md` を作成・所有しない
- `marketplace.json` を触らない

---

## 構成

```
ref-inject/
├── .claude-plugin/plugin.json
├── CLAUDE.md / CLAUDE.jp.md
├── skills/apply/SKILL.md (+ .jp.md)           # /ref-inject:apply — Claude がテンプレを読んで対象プラグインへ書く
├── skills/plugin-migrate/SKILL.md (+ .jp.md)  # /ref-inject:plugin-migrate — 全 consumer の注入ファイルを更新
├── skills/setup-wizard/SKILL.md (+ .jp.md)    # /ref-inject:setup-wizard — 初回オンボーディング（ユースケース紹介）
├── hooks/hooks.json                            # SessionStart フック: setup_done フラグ確認
└── hooks/scripts/setup_check.py               # .claude/ref-inject.local.md を読み、未設定時に setup-wizard を促す
    ├── hooks/
    │   ├── scripts/
    │   │   ├── inject_references.py      # PreToolUse: パス照合 → リファレンス注入（再利用される注入スクリプト）
    │   │   └── _common.py                # フックスクリプトの共通ヘルパー（stdin・env truthy・once-per-session・block 理由出力）
    │   ├── hooks.json
    │   └── templates/injection.md.j2 (+ .jp.md.j2)
    └── references/
        ├── _index.yaml (+ _index.jp.yaml)
        ├── _injection_rules.yaml
        ├── CLAUDE.md (+ CLAUDE.jp.md)
        └── example/はじめに.md
```

`plugin.json` / ルート `CLAUDE.md` のテンプレートは無い — それらはプラグインレベル
（`plugin-creator` の所有）であり、注入の仕組みの一部ではない。

---

## プレースホルダ

`apply` スキルが、各テキストテンプレートを書き出す際に Claude に置換させる
（対象プラグインのディレクトリ名から導出）:

| プレースホルダ | 置換内容 | 例 |
|---|---|---|
| `__PLUGIN_NAME__` | プラグイン名（kebab） | `vue-kit` |
| `__ENV_PREFIX__` | 名前を大文字化、英数以外を `_` | `VUE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `vue-kit-references-injection` |
| `__DEFAULT_TTL__` | デフォルト TTL 秒 | `3600` |

パスはテンプレートをそのまま反映 — 移動なし。

---

## 注入設計（フックに組み込み済み）

- `required` は（本セッション初回のみ）**本文全量**注入 / `optional` は**パス + description のみ**
- トークン: `~/.claude/tokens/{plugin}/{session_id}.yaml`。`patterns` と `references` の 2 名前空間を持つ**二層** YAML マップで、各エントリに `expires_at`（epoch、= 注入時刻 + TTL）。`now < expires_at` の間はスキップ、`now >= expires_at` で再注入。期限が注入時に確定するため、TTL の env var を変えても既存エントリには遡及しない。
  - **`patterns`**: そのパターンのリファレンス集合を再注入するかの判定（期限内のパターンは丸ごとスキップ）
  - **`references`**: `required` リファレンスの**本文**を注入するかの判定。本セッションに（どのパターン経由であれ）既に注入済み（期限内）なら**パスのみ**表示する。これで複数パターンに紐づくリファレンスの本文二重注入を防ぐ
- TTL: デフォルト `3600` 秒、`settings.json` の `env` → `{PREFIX}_INJECTION_TTL` で上書き（両層共通）
- クリーンアップ: 発火のたびに全 `{session_id}.yaml` を走査し両名前空間の期限切れエントリを削除、空ファイルは削除（旧 single-tier schema のトップレベルキーも除去）
- 言語: `{PREFIX}_INJECTION_LANG=jp` で description/テンプレートを日本語に切替

`PreCompact` フックは持たない: `/compact` 後は注入済み本文がコンテキストから消えるが、
トークンは TTL 経過後に再注入されるだけ。compact 専用のリフレッシュフックは無駄と判断（PR156）。

リファレンス層キャッシュ（PR160）は当初の single-tier（パターンのみ）トークン（PR156/157）を
拡張したもの。同一リファレンスが複数パターンに紐づくケースを解決し、別パターンにマッチする
ファイルを編集しても共有ドキュメント本文を再注入しなくなった。この仕組み全体は旧方式（パターン
単位の空ファイルトークン PR150/151、ポインタのみ注入 PR147）を置き換える。TTL トークンが
再注入を throttle するため `required` の本文注入を復活させた。

---

## 使い方

対象プラグイン（新規でも既存でも）に `/ref-inject:apply` を実行する。その後 `references/` を
実際の doc で埋め、`_injection_rules.yaml` で紐付ける。

全 consumer の**仕組み**を変えるときは、ここの `templates/` を編集し、変更後のテンプレを各
consumer の `hooks/` に再適用する（references はそのまま。`ref-inject` 由来なのはフック・
テンプレートファイルのみ）。

---

## 関連プラグイン

| プラグイン | 関係 |
|---|---|
| `dev-kit` / `claude-kit` | リファレンス注入の consumer。ref-inject テンプレートを採用済み |
| `claude-kit` | `plugin-creator`（プラグインレベルのファイルを所有）と共通フックポリシーの出所 |

---

## Changelog

| バージョン | 日付 | 概要 |
|---|---|---|
| 1.8.0 | 2026-05-31 | `ref-inject:setup-wizard` スキルと `SessionStart` フック（`setup_check.py`）を追加。`plugin-migrate` の Step 5 に setup-wizard 実装確認を追加 |
| 1.6.0 | 2026-05-30 | `ref-inject:plugin-migrate` スキルを追加 — consumer を列挙し注入フックファイルを現行テンプレートに更新する; references/ は変更しない (PR185) |
| 1.5.0 | — | 二層 TTL トークン（パターン層 + リファレンス層）導入 — 複数パターンで共有されるリファレンスの二重注入を防止 (PR160) |
