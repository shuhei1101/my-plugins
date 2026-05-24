<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# hook-pattern-change-missed-plugin

## 何が起きたか

PR115 でフックの `"Read and follow: /path"` パターンを直接コンテンツ埋め込みに一括変更した。
work-kit / dev-kit / ui-kit の hooks.json は修正したが、**claude-kit/hooks.json が完全に見落とされた**。

残存していた未修正箇所：
- `UserPromptSubmit` × 5（skill-creator-dispatch, rule-creator-dispatch, hook-creator-dispatch, claude-creator-dispatch, plugin-creator-dispatch）
- `PostToolUse` × 1（jp-mirror-check）

## なぜ起きたか

PR115 では Stop フックの修正を起点に作業を進め、同じ hooks.json 内の他フックタイプ（UserPromptSubmit, PostToolUse）まで修正対象を広げた。
しかし claude-kit の hooks.json は Stop フックを持たないため「Stop フックのあるプラグイン」として認識されず、修正リストから漏れた。

## 修正

PR119 で `grep -r "Read and follow" --include="*.json" .` を実行して残存を確認し、claude-kit/hooks.json を修正した。

## 再発防止

フックパターンの横断変更を行う場合は、実装前に以下を実行して全プラグインの対象箇所を網羅的に確認すること：

```bash
grep -r "対象パターン" --include="*.json" .
```

修正後も同じコマンドで残存がないことを確認してからコミットする。
