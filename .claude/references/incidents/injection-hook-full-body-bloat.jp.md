<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# 自動注入フックが reference 本文全体を注入しコンテキストを圧迫

## 何が起きたか

py-kit / next-kit の references 自動注入フック（`inject_references.py`、PreToolUse）が、
マッチした reference ファイルの**本文全体**を `decision: block` の reason に展開していた。
フックは `Read` でも発火するため、`injection_rules.yaml` のパターンにマッチするファイル
操作のたびに大きな reference 本文が Claude のコンテキストへ流し込まれた。調査フェーズで
複数の `.py` を読むと、ファイルごとに繰り返し注入されコンテキストを激しく圧迫した。

## 診断の経緯

ソースファイル閲覧中にコンテキストが膨らむことにユーザーが気づき、フックの見直しを依頼。
調査の結果、Jinja2 テンプレートが Required セクションで `{{ ref.body }}` を展開していた。

## 最初の誤った対応

AI は当初、発火を止めるため `hooks.json` から **`Read` マッチャーを削除**することを提案した。
ユーザーが訂正: `Read` マッチャーは意図的なもの（`issue-scan` など読み取り経路でも reference
の案内を受けられるようにするため）。問題はトリガーではなく**注入内容の量**だった。

## 修正（PR147）

1. **ポインタのみ**（path + description）を注入し、本文は注入しない。本文は Claude が
   必要に応じて `Read` で自分で読む。
2. `inject_references.py` の `_read_ref()` から本文読み込みを削除し、4 つのテンプレートから
   `{{ ref.body }}` を削除。冗長な Summary セクションも削除。
3. `Read` マッチャーは維持。

## 第2の教訓: `${CLAUDE_PLUGIN_ROOT}` は注入テキスト内で展開されない

ポインタ方式に切り替えたことでパス解決のバグが露呈した。テンプレートは当初
`references/{{ ref.path }}`（相対パス）を出力していたが、これは**編集対象プロジェクト**の
cwd 基準で解決されるため（プラグインキャッシュではない）、Claude が `Read` できなかった。

`${CLAUDE_PLUGIN_ROOT}` は **hooks.json の中でのみ**展開される（`claude-kit/references/hooks.md`
参照）。フックが print する reason テキスト内では展開されない。したがってフックスクリプト
自身が**絶対パス**を生成して出す必要がある（`(refs_dir / rel_path).as_posix()`）。これは
1行参照パターン（フックの reason/stdout に絶対パスを書く）と同じ考え方。

## まとめ

- 自動注入フックは**本文全体ではなくポインタ**を注入すべき。本文はマッチする操作のたびに
  コンテキストコストを増大させる。
- フックが Claude にプラグインファイルの `Read` を促すときは**絶対パス**を出す。
  `${CLAUDE_PLUGIN_ROOT}` は hooks.json の args 内のみで、注入テキストでは使えない。
- 注入フックがコンテキストを圧迫したら、**トリガー**を削除する前に**注入内容**を減らす。
  トリガーは他の利用者（issue-scan）に使われている可能性がある。
