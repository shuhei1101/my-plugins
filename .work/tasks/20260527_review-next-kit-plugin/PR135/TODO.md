# PR135 — review-next-kit-plugin

## 概要

next-kit プラグイン全体を Claude Code の一般的なベストプラクティス知識で評価し、改善提案を **質問形式で大量に QA.md に書き出す**。ユーザーが一個ずつ判断し、採用したものを実装する。

**評価観点（例）**:
- ライブラリ選定（Mantine / react-hook-form / Zod / TanStack Query / Drizzle）の妥当性。代替案・トレードオフ
- フォルダ構造の保守性（`[id]/view/` `[id]/edit/` sibling、`_components/` `_hooks/` プレフィックス）
- ファイル分割粒度（API ルートの route/client/service/db/query 5分割、フォームの form.ts + useXxxForm + useXxx{Action}）
- ドキュメント分類（`conventions/` vs `patterns/` の境界）
- 抜けている観点（パフォーマンス、SEO、a11y、テスト戦略、CI/CD、デプロイ戦略、画像最適化、フォント、SSR vs CSR の使い分け など）
- 命名規則の一貫性
- 型定義の場所
- エラー処理の階層
- セキュリティ考慮事項

**流れ**:
1. AI が next-kit の references を全て読み、評価
2. 改善提案を質問形式で QA.md に大量に書く（「Mantine をやめて shadcn/ui にしませんか?」「[id]/page.tsx の redirect は middleware で実装してはどうですか?」等）
3. ユーザーが一個ずつ「採用 / 不採用 / 後回し」を判断
4. 採用されたものを当 PR で実装

**背景（PR132 からの引き継ぎ）**:
- PR132 で next-kit プラグインが完成したが、設計は ユーザー自身の経験ベース（quest-pay プロジェクト）から抽出したもので、外部のベストプラクティスとの照合は未実施
- 「自分が考えたやり方で、特に何かに習ってやってるわけじゃないから、評価しておきたい」とのユーザー意向

### 実施条件

即時実施可（PR132 がマージ済みで next-kit が一通り整備済みであること）

### 関連PR

| PR番号 | 概要 |
|---|---|
| #132 | next-kit プラグイン新規作成（評価対象） |

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | next-kit の全 references を読み、ベストプラクティスと照合する | `plugins/next-kit/references/**` |
| 済 | 観点抜けがあれば洗い出す（パフォーマンス、a11y、SEO、テスト戦略、CI/CD、画像最適化など） | (調査) |
| 済 | 改善提案を質問形式で QA.md に大量に書き出す（QA-001〜QA-072、計 72 件） | `.work/tasks/.../PR135/QA.md` |
| 済 | ユーザーに採否を確認し、QA に判断を記録する | (ユーザー対話) |
| 済 | Next.js 16 最新ドキュメント確認（middleware→proxy、Cache Components、async Request API 等） | (調査) |
| 済 | quest-pay の参考実装（route.ts/service.ts/db.ts/query.ts、drizzle/schema.ts）を確認 | (調査) |
| 済 | 既存 references を shadcn/ui + Next.js 16 ベースに全面書き換え | `plugins/next-kit/references/{frontend,backend,shared}/**` |
| 済 | 新規 references を追加（server-actions, proxy, auth, caching, security, testing/, devtools/, devops/, streaming, seo, assets, pwa, autosave, route-files, server-vs-client, webhooks, jobs, realtime, rate-limit, idempotency） | `plugins/next-kit/references/**` |
| 済 | CLAUDE.md インデックスを新構成で再生成 | `plugins/next-kit/references/CLAUDE.md` |
| 済 | SKILL.md（implement）を新構成に合わせて更新 | `plugins/next-kit/skills/implement/SKILL.md` |
| 済 | JP ミラーを同期する（46 ファイル） | `plugins/next-kit/references/**/*.jp.md`, `plugins/next-kit/skills/**/*.jp.md` |
| 済 | plugin.json / marketplace.json を MAJOR バンプ（1.2.0 → 2.0.0、破壊的変更） | `plugins/next-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | QA-073: references をユースケース＝ファイル単位で全面再分割（46 → 70+） | `plugins/next-kit/references/**` |
| 済 | 旧 references を全削除し、新構成で書き直し | 同上 |
| 済 | 比較・選定・トレードオフ系を完全削除 | 同上 |
| 済 | CLAUDE.md と SKILL.md を新分割マップで再生成 | `plugins/next-kit/references/CLAUDE.md`, `plugins/next-kit/skills/implement/SKILL.md` |
| 済 | JP ミラーを再生成 | `plugins/next-kit/**/*.jp.md` |
| 済 | plugin.json / marketplace.json を 2.0.0 → 3.0.0 にバンプ（再構成のため） | 同上 |
| 済 | PR140 (py-kit) の実装に合わせて hooks/ と index.yaml + injection_rules.yaml を導入 | `plugins/next-kit/hooks/**`, `plugins/next-kit/references/index.yaml`, `injection_rules.yaml` |
| 済 | `hooks/inject_references.py` + `templates/injection.{md,jp.md}.j2` + `hooks.json` を実装（env: `NEXT_KIT_INJECTION_LANG`） | `plugins/next-kit/hooks/` |
| 済 | `references/index.yaml` + `index.jp.yaml` を 91 ファイル分作成 | `plugins/next-kit/references/index.yaml`, `index.jp.yaml` |
| 済 | `references/injection_rules.yaml` で全ファイルパターンマッピングを作成 | `plugins/next-kit/references/injection_rules.yaml` |
| 済 | `references/CLAUDE.md(jp)` を「index.yaml を読め」スタイルに簡素化 | `plugins/next-kit/references/CLAUDE.md(.jp).md` |
| 済 | plugin.json / marketplace.json を 3.0.0 → 3.1.0 にバンプ（フック追加） | `plugins/next-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | my-plugins ルール作成: kit 間の hooks / index 構造同期ルール（py-kit ↔ next-kit、将来 X-kit） | `.claude/rules/feature/kit-hooks-index-sync.md` (+ jp) |

## 参考ドキュメント

- `plugins/next-kit/references/`: 評価対象の規約集
- `.work/notes/AIイシュー自動発見システム構想.md`: 設計背景

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| references の自動フック読み込み機構 | 特定フォルダ/ファイル名（例: `*.view.tsx`, `app/api/**/proxy.ts` 等）の編集時に対応する references を Claude に自動読み込みさせる UserPromptSubmit/PreToolUse フックを構築 | PR135 マージ後 |
| TypeScript リントの自動実行フック | コミット前 / PostToolUse で `tsc --noEmit` を走らせて型崩れを検知（QA-046 の補強） | 即時実施可 |
| next-kit プラグインのテンプレート生成スキル | `references/**` を読み込んで初期プロジェクトを scaffold するスキル | references が安定後 |
| AI イシュー自動発見システム構想の更新 | 当 PR の references 改訂を `.work/notes/AIイシュー自動発見システム構想.md` に反映 | PR135 マージ後 |
