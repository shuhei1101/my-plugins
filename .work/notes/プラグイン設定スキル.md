# プラグイン設定スキル — 設計メモ (PR167)

## 概要

PR164 で追加された env トグル群を、ユーザーが簡単に ON/OFF できるスキルを作成する。

## UX フロー（案）

1. `/plugin-config` を呼び出す
2. 現在の env 変数の状態を読み取り（settings.json の env ブロックを参照）
3. AskUserQuestion で各トグルの ON/OFF を選択肢で提示
4. 選択に基づき settings.json の env ブロックを更新

## 実装上の注意

- settings.json はユーザースコープ（`~/.claude/settings.json`）かプロジェクトスコープ（`.claude/settings.json`）かを選択させる
- env 未設定 = デフォルト有効のため、「ON（デフォルト）」の場合は env キーを削除する設計にする
- `INJECTION_DISABLE` のみ逆極性（truthy で無効化）— 表示ラベルを「注入を無効にする」にする

## 実装済み（PR167）

- `plugins/work-kit/skills/config/SKILL.md` — スキル定義（`plugin-config` → `config` にリネーム）
- `plugins/work-kit/skills/config/SKILL.jp.md` — JP ミラー
- work-kit v2.38.0 → v2.39.0 バンプ

## UX フロー（最終設計）

1. 現在の設定状態をテキストで一覧表示
2. ループ開始: `AskUserQuestion` #1 → どの env 変数を設定するか（4 オプション + その他）
   - options 1-3: よく使う work-kit 変数（現在の状態を `[ON/OFF]` でラベルに表示）
   - option 4: 完了（ループ終了）
   - その他: MERGE_CONV2CLAUDE / MERGE_AUTO_HANDOFF / NEXT_KIT_TS_CHECK / AITUBER_NOTIFY を手入力
3. `AskUserQuestion` #2 → 2 つの質問を 1 回で：値（デフォルト/OFF） + スコープ（プロジェクト/ユーザー）
4. 変更を適用して Step 2 に戻る
5. 完了選択時: 全変更のサマリーを表示

## 実装済み（PR204）

PR174 完了を受けて、逆極性の `{PREFIX}_INJECTION_DISABLE` 変数を work:config 管理対象に追加。

追加した管理変数:
- `CLAUDE_KIT_INJECTION_DISABLE` — claude-kit の全参照注入を無効化（truthy で無効）
- `DEV_KIT_INJECTION_DISABLE` — dev-kit の全参照注入を無効化（truthy で無効）

### 逆極性変数の設計

Step 1（状態判定）: truthy な値（"true"/"1"/"yes"/"on"）→ OFF（注入無効）。キー不在 or falsy → ON（注入有効）。

Step 3（値選択）: 逆極性変数には専用 options を表示。
- "デフォルトに戻す（キー削除 = 注入 ON）"
- "無効にする（"true" に設定 = 注入 OFF）"

Step 4（適用）: "無効にする" → `"true"` を設定。"デフォルトに戻す" → キー削除。

Notes の除外文言を削除。

work プラグインバージョン: v2.46.2 → v2.47.0（MINOR バンプ）

## 参照

- `.work/notes/env-toggles-for-hooks-and-steps.md` — PR164 の env トグル実装メモ
