# QA — PR128 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: YAML スキルの所属プラグイン

**決定**: dev-kit に残す。Python 専用コンテンツは py-kit として新規プラグインを作成し分離する。

---

## QA-002: `.work/issues/` の設置先プロジェクト

**決定**: work-kit の setup スキルで `.work/issues/` を作成する（対象プロジェクト汎用）。

---

## QA-003: audit-kit から py-kit/ui-kit の references 参照方法

**決定**: audit-kit は作成しない。issue-scan・issue-create スキルを work-kit に統合する。
参照方法は `${CLAUDE_PLUGIN_ROOT}` 経由で対象プロジェクトにインストールされた py-kit / html-kit の references を読む。

---

## QA-004: dev-kit → py-kit リネームの既存プロジェクト対応

**決定**: dev-kit はリネームしない（現状維持）。Python 専用の py-kit を新規作成する。ui-kit は html-kit にリネームする。

---

## QA-005: Next.js 対応プラグイン

**決定**: next-kit プラグインを将来 PR で作成予定（PR-E として予約）。
現在フロントエンドはバニラ HTML を使用しているが、Next.js への移行計画がある。
