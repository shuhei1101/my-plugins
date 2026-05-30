# QA — PR143 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: フック実装方式 ✅決定

**背景**: TS の型崩れを検知する方法は複数考えられる。
PostToolUse はリアルタイム検知できるが、毎回 `tsc --noEmit` を走らせると遅い（大規模プロジェクトでは数秒〜数十秒）。pre-commit ならコミット時の最終ガードになる。

**案**:
- A. **PostToolUse(Edit/Write/MultiEdit)** で `*.ts` `*.tsx` 編集後に `tsc --noEmit` を実行（リアルタイム検知、ただし遅い可能性）
- B. **pre-commit フック (lefthook / husky)** でコミット時にのみ実行（軽い、ただし検知が遅い）
- C. **A + B の併用**（リアルタイム + 最終ガード）
- D. **`tsc --noEmit --incremental`** でインクリメンタル実行（遅さ問題の緩和）

**決定**: A + D（PostToolUse(Edit/Write/MultiEdit) で `tsc --noEmit --incremental` を実行）

---

## QA-002: 配置 plugin ✅決定

**背景**: フックをどの plugin に置くか。

**案**:
- A. **claude-kit** に置く（汎用フック群と一緒）
- B. **next-kit** に置く（TS 関連の規約は next-kit にある）
- C. 新規 **`ts-check-kit`** plugin を作る（独立、将来 Vue/Svelte 等の TS プロジェクト共通として再利用可）

**決定**: B（next-kit）。TS 規約は next-kit にまとまっており、新 plugin 作成は早すぎる分離（PR140 の反省）

---

## QA-003: 対象プロジェクトの検出方法 ✅決定

**背景**: フックが発火するプロジェクトをどう判定するか。

**案**:
- A. **`tsconfig.json` の存在**で判定（最も汎用）
- B. **`package.json` に `typescript` 依存があるか**で判定
- C. 編集対象ファイルから `tsconfig.json` を上方向に探索（モノレポ対応）

**決定**: C（編集対象ファイルから上方向に `tsconfig.json` を探索）。モノレポ対応が重要

---

## QA-004: エラー時の挙動 ✅決定

**背景**: `tsc --noEmit` が失敗したときの挙動。

**案**:
- A. **stderr に出力**するだけ（ブロックしない、ログ参照）
- B. **`decision: block`** で次の Edit/Write を止める（強制）
- C. **toast / sonner で通知**（フロント前提）— Claude Code のフックでは不可
- D. **コミット時 (pre-commit) なら失敗で commit を止める**（git 標準）

**決定**: A（stderr 出力のみ）。`decision: block` は連続 Edit 中に割り込み作業フローを壊す。reason にエラーを出して Claude が判断する形

---

## QA-005: incremental ビルド / キャッシュ ✅決定

**背景**: `tsc --noEmit` を毎回 cold start で走らせると遅い。

**案**:
- A. **`--incremental`** で `.tsbuildinfo` キャッシュを利用
- B. **デバウンス**（最後の Edit から N 秒経って初めて実行）
- C. **changed files のみ**チェック（`tsc --noEmit --listFiles` 等で差分判定）— 厳密性が落ちる

**決定**: A（`--incremental`）。TypeScript 標準の仕組みで信頼性が高い。QA-001 の決定と統合

---

## QA-006: ts-go / Biome 等の代替 ✅決定

**背景**: 公式 `tsc` の代替として高速な型チェッカーがある。

**案**:
- A. **`tsc --noEmit`** を採用（公式、確実）
- B. **`@biomejs/biome`** で lint + 型チェック（高速、ただし型推論は tsc ほど厳密でない）
- C. **`ts-go`** (Microsoft TypeScript-Go) を採用（実験的、高速）

**決定**: A（`tsc --noEmit`）。公式ツールで追加セットアップ不要。`ts-go` は実験的すぎ、Biome は型推論が tsc ほど厳密でない
