# aituber — ドキュメント Wiki

プロジェクト全体のドキュメントナビゲーションハブ。すべてのドキュメントへのリンクを一元管理する。

**作成日**: 2026-04-26
**最終更新**: 2026-04-26

---

## 🎯 プロジェクト管理・意思決定

- **[Issues.md](Issues.md)** — 未決定事項・検討中の Issue 集（ISSUE-XXX 番号で管理）
- **[イシュー履歴.md](イシュー履歴.md)** — 決定済みイシューの履歴（追記型ログ、決定経緯の追跡用）

---

## 📡 配信モード仕様

- **[共通仕様.md](共通仕様.md)** — 全モード共通の決定済み仕様
- **[YouTube配信モード.md](YouTube配信モード.md)** — YouTube Live Chat 配信モード固有の仕様 ✅
- **[ゲーム実況モード.md](ゲーム実況モード.md)** — ゲーム実況変換モード固有の仕様 ✅
- **[個人チャットモード.md](個人チャットモード.md)** — 個人おしゃべりモード固有の仕様

---

## 🤖 AI・システム設計

- **[AI構成.md](AI構成.md)** — LLM プロバイダ・タスク設計・統一 JSON 構造
- **[LLM エージェント設計.md](LLM エージェント設計.md)** — エージェント構成とロール定義
- **[配信フロー設計.md](配信フロー設計.md)** — 配信処理フロー全体図

---

## 🔌 API 仕様

- **[YouTube ライブチャット API.md](YouTube ライブチャット API.md)** — YouTube Data API v3 の Live Chat 仕様
- **[OBS WebSocket API.md](OBS WebSocket API.md)** — OBS WebSocket v5 連携仕様
- **[VTube Studio API.md](VTube Studio API.md)** — VTube Studio API 連携仕様
- **[AI Voice API.md](AI Voice API.md)** — 音声合成 API まとめ

---

## 📚 参考資料

- **[Claude Code CLI 仕様.md](Claude Code CLI 仕様.md)** — Claude Code CLI 統合パターン

---

**更新ルール**:
- 新規ドキュメント作成時 → このファイルの対応セクションにリンク追加
- ドキュメント削除時 → このファイルの該当リンク削除
- ドキュメント名変更時 → このファイルのリンクも同時に更新
