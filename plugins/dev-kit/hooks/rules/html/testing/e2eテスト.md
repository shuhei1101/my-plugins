---
paths:
  - "**/frontend/tests/e2e/**/*.spec.{ts,js}"
  - "**/playwright.config.{ts,js}"
---

# E2E テスト（playwright）

FastAPI を 1 プロセス起動し、同一オリジンで画面を叩く。Next.js 時代の別フロントプロセス・rewrite proxy は無い。

- スペックは `frontend/tests/e2e/{name}.spec.ts`。`import { test, expect } from "@playwright/test"`。
- 外部 I/O（LLM / TTS / OBS 等）は `AITUBER_E2E_MOCK_LLM=1` でモックする（`playwright.config.js` の webServer env）。実課金・非決定性に依存させない。
- ロケータは role / text / label ベースを優先。画面の `id` で参照するのは実装と対応が明確な範囲に留め、`data-testid` は最後の手段。
- 待ちは `expect(locator).toBeVisible()` 等で行う。`sleep` をハードコードしない。
- 実 FastAPI とファイル永続を共有するため直列実行（`workers: 1`・`fullyParallel: false`）。
- 検証対象は「画面が組み上がる・共通シェルが付く・主要操作とバリデーション」。ユニットで足りることは持ち込まない。
- メイン dev server 稼働中に走らせるときは worktree から別ポート（既定 8190・`E2E_PORT`）で起動する。設定詳細は `playwright.config.js`（worktree の src を PYTHONPATH に、メインリポジトリの venv / settings を参照）。
