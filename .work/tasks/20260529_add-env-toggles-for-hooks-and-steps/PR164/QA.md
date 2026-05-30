# QA — PR164 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: #3 INJECTION_DISABLE の波及方法

ref-inject の注入 OFF スイッチは `plugins/ref-inject/templates/hooks/inject_references.py`
（テンプレート本体）に実装する。これを claude-kit / py-kit / next-kit の既存コピーへ
反映する方法をどうするか:

- 案A: テンプレonly 変更 + 各プラグインを `/ref-inject:apply` で再生成
- 案B: この PR 内で 3 プラグインの `inject_references.py` も手編集して同期（kit-hooks-index-sync ルール準拠）

**状態**: 解決済み — テンプレートのみ変更。claude-kit / py-kit / next-kit への反映は次 PR に委ねる。

## QA-002: #7 AITUBER_NOTIFY のスコープ

notify-aituber はこのリポジトリではなくユーザーの `~/.claude/skills/notify-aituber` 配下にある。
この PR の対象に含めるか、別作業（リポジトリ外）として切り離すか。

**状態**: 解決済み — この PR に含める。`~/.claude/settings.json` は git 管理外のため直接変更してよい。

## QA-003: env 変数の命名規則

merge 関連トグル（#5 #6）を `WORK_KIT_MERGE_CONV2CLAUDE` / `WORK_KIT_AUTO_HANDOFF` の
ように `WORK_KIT_` プレフィックスで統一するか、`WORK_KIT_MERGE_*` でさらに名前空間を切るか。
全体の命名一貫性を着手前に確定する。

**状態**: 解決済み — `WORK_KIT_MERGE_` で名前空間を切る。例: `WORK_KIT_MERGE_CONV2CLAUDE` / `WORK_KIT_MERGE_AUTO_HANDOFF`。
