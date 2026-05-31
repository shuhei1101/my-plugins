# ISSUE-064: vscode-workspace-sync/SKILL.jp.md がコードブロックを省略してリンク参照に差し替えている

**作成日**: 2026-05-31

## 問題

`plugins/work/skills/vscode-workspace-sync/SKILL.jp.md` の Step 3 セクションで、EN オリジナル (`SKILL.md`) が持つ2つの JSON コードブロック（Hook 1 / Hook 2）が完全に省略されており、代わりに以下のような参照文が記載されている:

```
**フック1 — worktree 追加時にワークスペースの folders にパスを追加:**

SKILL.md の Hook 1 JSON 参照

**フック2 — worktree 削除時にワークスペースの folders からパスを削除:**

SKILL.md の Hook 2 JSON 参照
```

EN ファイルには各 Hook の完全な JSON（計 30+ 行のコードブロック）が含まれているが、JP ミラーにはそれがない。コードフェンス数の差異: EN = 4、JP = 0。

JP ミラーは「自己完結した翻訳版」であるべきで、EN ファイルへの参照を要求してはならない。

## 修正案

`SKILL.jp.md` の Step 3 に、`SKILL.md` から Hook 1 / Hook 2 の JSON コードブロックをそのままコピーし、前後の日本語説明文と組み合わせて完結した形にする。コードブロック自体は英語のままで問題ない（JSON は言語非依存）。

## 水平展開

JP ミラーを作成する際に「長いコードブロックは EN を参照」という省略が行われると、JP ミラーが単独で機能しなくなる。他のスキルファイルでも同様の省略がないか確認することを推奨する。
