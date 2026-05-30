# フック直接差し戻し方式の選択理由 — 設計判断メモ

## 背景

PR89 / PR104 で「Stop フックの reason に全文を埋め込むとユーザーに見えて鬱陶しい」という incident を受け、すべてのフックを `"Read and follow: /path"` の1行参照方式に変更した。

## 問題

複数の Stop フックが同時発火する場合に "Read and follow:" 方式が信頼できない：

1. notify-aituber (直接指示) と work-kit (間接参照) が同時にブロック
2. Claude が notify-aituber の直接指示を優先して実行
3. Claude が再 Stop → `stop_hook_active=true` → 両フックがスキップ
4. work-kit の stop.md 指示が永遠に実行されない

## 判断

直接コンテンツ埋め込み方式に戻す。reason テキストが長くなっても、確実に実行されることを優先する。

- Stop フック: `p.read_text('utf-8')` を reason に埋め込む
- UserPromptSubmit フック: `q.read_bytes()` を stdout に直接出力
- PreToolUse フック: `p.read_text('utf-8')` を reason に埋め込む

## 影響

`Stop hook error: {full content}` が UI に表示されるようになるが、機能的には正しく動作する。

## PR115 残作業 (PR119)

PR115 では `claude-kit/hooks/hooks.json` の修正が漏れていた。
以下が未修正：
- UserPromptSubmit × 5（skill-creator-dispatch, rule-creator-dispatch, hook-creator-dispatch, claude-creator-dispatch, plugin-creator-dispatch）
- PostToolUse × 1（jp-mirror-check）

UserPromptSubmit フックの変更パターン：
- Before: `sys.stdout.buffer.write(('Read and follow: '+str(q)+'\\n').encode())`
- After: `sys.stdout.buffer.write(q.read_text('utf-8').encode())`

PostToolUse フックの変更パターン：
- Before: `sys.stdout.buffer.write(('Read and follow: '+sys.argv[1]+'\\n').encode())`
- After: `sys.stdout.buffer.write(pathlib.Path(sys.argv[1]).read_text('utf-8').encode())`
