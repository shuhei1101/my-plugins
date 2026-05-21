# Glossary

## Plugin System

| 用語 | 説明 |
|---|---|
| incidents | このプロジェクトで再発防止ログを蓄積する固定ルールファイル（`.claude/rules/incidents.md`）。インデックス（常時読み込み）と詳細ファイル（`.claude/references/incidents/`）の2層構造。 |
| glossary | このプロジェクトでプロジェクト固有の用語を管理する固定ルールファイル（`.claude/rules/glossary.md`）。常時読み込みされるため簡潔に保つ。 |
| conversation-to-claude | セッションの会話履歴を分析し、スキル・ルール・フック・CLAUDE.md・incidents・glossary などのアーティファクトとして知識を永続化するスキル（`/claude-kit:conversation-to-claude`）。 |
