<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# session-kit プラグイン開発ガイド

session-kit は、他プラグイン（py-kit / next-kit）が `/tmp` に置く **注入トークン** の寿命を
管理する。ユーザーのプロンプトごとに現セッションのトークンを削除し（会話ターンごとに
reference を再注入させる）、セッション開始時に古いトークンを掃除する。

**マーカーファイルは持たず**、利用側は session-kit に依存しない: 利用側は自分のトークンを
作って存在チェックするだけで、session-kit が外部から削除する。

---

## 何をするか

| フック | 動作 |
|---|---|
| `UserPromptSubmit` | **現セッションの**注入トークン（`*-references-injection-{session_id}-*`）を削除 |
| `SessionStart` | **TTL 掃除**: 1 日以上前の注入トークンを削除 |

それ以外は **何もしない** — プロンプト注入もブロックも出力もなし。

### なぜ UserPromptSubmit で削除するか（会話ターン単位キャッシュ）

注入トークンは「このルールの reference は注入済み」の印。これを **セッション** 全体で持つと
長すぎる: 長い会話だと注入した案内がコンテキストのずっと上に埋もれ、Claude が忘れてしまう。
`UserPromptSubmit` ごとにセッションのトークンを削除することで、キャッシュを **会話ターン単位**
にする。新しいターンで Claude が再びマッチするファイルを触ったら reference は再注入され、
かつ同一ターン内の繰り返しアクセスは重複注入しない。

`/compact` と `/clear` は個別対応不要: `/compact` 後は次の UserPromptSubmit でトークンが
消えて再注入され、`/clear` は session_id が変わるので新セッションが自然に再注入する。

---

## 注入トークン規約（他プラグインとの共有契約）

| | 値 |
|---|---|
| パス | `/tmp/{plugin}-references-injection-{session_id}-{patternhash}`（`tempfile.gettempdir()` 経由） |
| 意味 | 空ファイル = 「このルールの reference はこのターンで注入済み」 |
| キー | マッチした **injection_rules のパターン単位**（ファイル単位ではない）。同じパターンにマッチする全ファイルで共有 |
| 生成/参照側 | py-kit / next-kit の `inject_references.py`（注入時に作成、トークンがあればそのパターンはスキップ） |
| 寿命管理 | session-kit（`UserPromptSubmit` で削除、`SessionStart` で TTL-GC） |
| 掃除 glob | `*-references-injection-*`（`hooks/session_gc.py` の `_TOKEN_GLOB` 参照） |

**グレースフルフォールバック**: session-kit が未インストールなら、トークンはターンごとに
削除されないだけ（利用側はセッション全体で once-per-pattern 挙動）で、OS が `/tmp` を消すまで
溜まる。session-kit は **任意の companion** であり、利用側は依存してはならない。

TTL は 1 日: それほど長いセッションは無いので、アクティブなセッションのトークンは新しく
消されない。並行セッションも同様に守られる。掃除が早すぎた場合の最悪でも無害な再注入が
走るだけ。

---

## なぜ専用プラグインか（フックロジックの集約ではない）

ここでのクロスプラグイン契約は **ファイル名規約のみ** — session-kit は `/tmp` を glob する
だけで他プラグインのコードを実行せず、利用側も session-kit を呼ばない。これにより
`refs-inject-kit` が却下された `${CLAUDE_PLUGIN_ROOT}` のクロスプラグイン・パス解決問題
（incident `premature-cross-plugin-centralization`）を回避できる。トークン寿命はセッション
単位の関心事なので、管理者を 1 つにする設計が自然。

---

## バージョン

| バージョン | 主な変更 |
|---|---|
| 1.1.0 | トークン削除方式へピボット: UserPromptSubmit で会話ターンごとにセッションの注入トークンを削除（マーカーファイル廃止）、SessionStart で古いトークンを 1 日 TTL で掃除（PR151） |
| 1.0.0 | 初版: PreCompact + SessionStart(clear) のコンテキスト世代マーカー（PR150、置き換え済み） |
