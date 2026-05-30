# env トグル実装メモ — PR164

## 概要

常時発火するフック/ステップを env var で opt-out できる仕組みを全 7 件実装した。

## 実装した env トグル一覧

| env 変数 | 実装箇所 | デフォルト | 無効化値 |
|---|---|---|---|
| `WORK_KIT_PR_ENFORCEMENT` | `user-prompt-submit.py` 先頭 | 有効 | `false`/`0`/`no`/`off` |
| `WORK_KIT_STOP_REMINDER` | `hooks.json` Stop インライン python | 有効 | `false`/`0`/`no`/`off` |
| `WORK_KIT_MERGE_CONV2CLAUDE` | merge SKILL.md Step 4 Condition | 有効 | `false`/`0`/`no`/`off` |
| `WORK_KIT_MERGE_AUTO_HANDOFF` | merge SKILL.md Step 12 Condition | 有効 | `false`/`0`/`no`/`off` |
| `NEXT_KIT_TS_CHECK` | `ts_check.py` main() 先頭 | 有効 | `false`/`0`/`no`/`off` |
| `{PREFIX}_INJECTION_DISABLE` | `inject_references.py` テンプレート | 有効（注入ON） | `true`/`1`/`yes`/`on` |
| `AITUBER_NOTIFY` | `~/.claude/settings.json` Stop フック | 有効 | `false`/`0`/`no`/`off` |

## QA で決定した事項

- **QA-001**: `{PREFIX}_INJECTION_DISABLE` の 3 プラグインへの波及は次 PR に委ねる（テンプレートのみ変更）
- **QA-002**: `AITUBER_NOTIFY` はリポジトリ外（`~/.claude/settings.json`）を直接変更してよい
- **QA-003**: merge 関連 env 変数は `WORK_KIT_MERGE_` で名前空間を切る

## 設計メモ

- `{PREFIX}_INJECTION_DISABLE` のみ「truthy で無効化」の逆極性。理由: 注入は有効がデフォルトで、積極的に「切る」意図を持つ変数名にしたため。
- 他は全て「falsy で無効化」の統一パターン（PR163 の WORK_KIT_USE_WORKTREE と同じ）。
- `AITUBER_NOTIFY` のフックは python inline なので、`os` の import を追加してチェックを先頭に挿入した。

## バージョンバンプ

- work-kit: 2.37.0 → 2.38.0
- next-kit: 3.7.0 → 3.8.0
- ref-inject: 1.2.0 → 1.3.0

---

# PR173 — WORK_KIT_MERGE_PROPOSAL トグル追加

## 概要

merge スキルがマージを提案するかどうかを env var でオフにできるようにする。

## 追加する env トグル

| env 変数 | 実装箇所 | デフォルト | 無効化値 |
|---|---|---|---|
| `WORK_KIT_MERGE_PROPOSAL` | merge SKILL.md (TBD: どのステップか調査) | 有効（提案あり） | `false`/`0`/`no`/`off` |

## 設計メモ

- PR164 の `WORK_KIT_MERGE_` 名前空間に追加
- `work-kit:config` スキルの選択肢にも追加する（PR167 で追加されたスキル）
