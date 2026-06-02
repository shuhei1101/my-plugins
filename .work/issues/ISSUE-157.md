# ISSUE-157: claude-kit:plugin-config SKILL.md（英語ファイル）の Notes セクションとステップ見出しに日本語が混入

**作成日**: 2026-06-02

## 問題

`plugins/claude-kit/skills/plugin-config/SKILL.md`（英語ファイルが source of truth）の以下の箇所が日本語のままになっている。

### 問題 1 — `## Notes` セクション（ファイル末尾）

3 行すべてが日本語：

```
- `settings.json` が存在しない場合は `{"env": {}}` として新規作成する
- `${CLAUDE_KIT_INJECTION_DISABLE}` は逆極性のキルスイッチのため、このスキルでは管理しない（`プラグイン設定.md` 参照）
- TTL には整数値のみ設定すること
```

### 問題 2 — ステップ見出し・条件行

```
### Step 2: Select variable to configure （ループ先頭）
- Step 1 complete（ループ時はここから再開）
```

ユーザー向け出力文字列（UI プロンプトや表ヘッダ）が日本語である点は意図的だが、スキル自身の操作手順・注意事項が日本語のままでは英語ファイルの role（source of truth）を果たせない。また JP ミラーの TTL ノートは「TTL に数値以外の文字列を設定しないこと — 整数値のみ有効」と微妙に異なる表現になっており、EN/JP 間で微妙な不整合がある。

## 対応方針

`## Notes` セクションの日本語行を英語に翻訳する。ステップ見出し・条件の括弧付き日本語注釈を英語に直す。SKILL.jp.md の TTL ノートとも表現を揃える。

## 対象ファイル

- `plugins/claude-kit/skills/plugin-config/SKILL.md`: `## Notes` セクション（末尾3行）、Step 2 見出しの `（ループ先頭）`、Step 2 条件の `（ループ時はここから再開）` を英語化

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
