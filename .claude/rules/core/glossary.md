# Glossary

## Plugin System

| 用語 | 説明 |
|---|---|
| incidents | このプロジェクトで再発防止ログを蓄積する固定ルールファイル（`.claude/rules/core/incidents.md`）。インデックス（常時読み込み）と詳細ファイル（`.claude/references/incidents/`）の2層構造。 |
| glossary | このプロジェクトでプロジェクト固有の用語を管理する固定ルールファイル（`.claude/rules/core/glossary.md`）。常時読み込みされるため簡潔に保つ。 |
| conversation-to-claude | セッションの会話履歴を分析し、スキル・ルール・フック・CLAUDE.md・incidents・glossary などのアーティファクトとして知識を永続化するスキル（`/claude-kit:conversation-to-claude`）。 |
| claude-refactor | `.claude/` 配下の rules / skills / CLAUDE.md / hooks を横断的に監査・整理するスキル（`/claude-kit:claude-refactor`）。重複検出・ファイルタイプ移管・フォルダ構成整備を提案し確認後に実行する。 |
| 判定知識 | スキルが提案・選択を行う際に必要な基準・ルールを、外部ファイルを読み込まずにスキル本体の References セクションに自己完結で埋め込んだブロック。トークン効率のために導入（PR68）。 |
| リンクルール | rules の2種類のひとつ（ファイル連携型）。関連ファイル群を `paths:` に束ねて「1つを編集したら他も確認する」連携を強制するルール。 |
| コンテキストルール | rules の2種類のひとつ（読み込みトリガー型）。特定の作業エリアを触ったときに必要な知識・仕様書を自動ロードするルール。 |
| ユースケース指向 | `paths:` 設計の原則。「このルールはいつ読まれたいか」を起点に逆算してトリガーとなるファイルを特定し、そこを `paths:` に設定する考え方。 |
| notes/ | work-kit が管理する `.work/notes/` フォルダ。PR に関連する一時的な設計メモ・検討ノートを置く場所。AI に自動読み込みされないため公式仕様書ではなく「作業中のメモ」として扱う。旧称 `specs/`（PR88 で改名）。 |
| notes-to-claude | `.work/notes/` の一時メモをルール・CLAUDE.md・references に昇格させる work-kit スキル（`/work-kit:notes-to-claude`）。確認フェーズなしで完全自動実行。claude-kit プラグインの creator スキルを内部で使用（PR90 で追加）。 |
| 1行参照パターン | Stop フックの `reason` にファイルの全文を埋め込む代わりに `"Read and follow: /path/to/file.md"` の1行だけを出力するパターン。Claude 自身がファイルを読む方式のため会話セッションへの長文注入を防げる（PR89 で導入）。 |
| pr-handoff | 現在のPRのTODO.mdに記録された「次PR候補」を元に、次のPRをwork-startと同じ流れで予約するスキル（`/work-kit:pr-handoff`）。各PRの背景情報をTODO.mdに記録して引き継ぎ品質を高める（PR91で追加）。 |
| master 適合確認 | merge スキルの Step3。master がブランチ分岐後に進んでいた場合、直接・間接の関連変更を確認しタイブレーク順位に従って自律判断で適合させるステップ（PR92 で追加）。 |
| 間接依存 | merge Step3 での検出対象。この PR が変更したファイルを呼び出している・インポートしている側が master で変更された場合の関係。`git diff --name-only` のファイル直接一致では検出できないため文脈判断が必要。 |
| タイブレーク順位 | merge Step3 で判断が拮抗した場合の優先順位。新しさ → 影響範囲（blast radius）→ PR の目的 → 安全側（master 取り込み）の順（PR92 で定義）。 |
