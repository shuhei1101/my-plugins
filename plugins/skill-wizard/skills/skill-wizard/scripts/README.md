# スクリプト一覧

## create-skill.py
新しいスキルの雛形を一発で作成するPythonスクリプト

### 使い方

```bash
python create-skill.py --skill-name my-skill --target-path /path/to/skills
```

### パラメータ

- `--skill-name`: 作成するスキル名（ケバブケース推奨）
- `--target-path`: スキルを配置するパス

### 動作

1. `{TargetPath}/{SkillName}/` フォルダを作成
2. `SKILL.md` テンプレートを作成
3. `sessions/` フォルダを作成
4. `sessions/.gitignore` を作成

---

## dev-cache-sync.py
**[DEV] 開発・デバッグ用** — 開発中のプラグインをClaudeのキャッシュに反映するスクリプト。
動作確認時に skill-wizard から呼び出される。本番での使用は想定していない。

### 使い方

```bash
# 編集したファイルのパスから自動検出
python dev-cache-sync.py --file-path /path/to/edited/SKILL.md

# プラグインのソースディレクトリを直接指定（複数プラグインの一括同期時など）
python dev-cache-sync.py --source-path /path/to/repo/plugins/skill-wizard

# 確認のみ（コピーしない）
python dev-cache-sync.py --file-path /path/to/SKILL.md --dry-run
```

### パラメータ

- `--file-path`: 編集したファイルのパス（プラグインルートを自動検出）※ `--source-path` と排他
- `--source-path`: プラグインのソースディレクトリを直接指定 ※ `--file-path` と排他
- `--dry-run`: 実際のコピーを行わずに動作確認する

### 動作

1. プラグインルートを特定
   - `--file-path` の場合: `.claude-plugin/plugin.json` を上方向に探索
   - `--source-path` の場合: 指定ディレクトリをそのまま使用
2. プラグイン名 = プラグインルートのディレクトリ名
3. `~/.claude/plugins/installed_plugins.json` からキャッシュパスを取得
4. プラグインルートをキャッシュパスに上書きコピー

### 必要な環境

- Python 3.6以上
- `~/.claude/plugins/installed_plugins.json` にプラグインが登録済みであること
