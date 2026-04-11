# ファイル配置ガイドライン

スキル内のファイルは以下の3つのディレクトリに分類して配置する:

## ディレクトリの役割

### `scripts/`
**実行可能なコード（決定的・反復的なタスク用）**

- Pythonスクリプト、Shell スクリプトなど、実行可能なファイル
- 繰り返し使われる定型処理（データ変換、検証、レポート生成など）
- LLMが毎回書くよりもbundleした方が効率的なコード

**配置すべきファイルの例:**
- データ処理スクリプト（JSON パース、CSV変換など）
- バリデーションスクリプト
- レポート生成スクリプト
- テスト実行スクリプト

**配置すべき場面:**
- テストケース実行時に、サブエージェントが同じようなヘルパースクリプトを繰り返し書いている
- 複数のテストケースで共通の処理が見られる
- 決まった入力から決まった出力を生成する処理

**例:** `scripts/generate_report.py`, `scripts/validate_yaml.py`

---

### `references/`
**必要に応じてコンテキストに読み込むドキュメント**

- LLMが参照する説明文書やガイド
- テンプレート、サンプルコード、スキーマ定義
- 大きなドキュメント（>300行）には目次を含める
- SKILL.md本体から「いつ読むべきか」を明確に参照する

**配置すべきファイルの例:**
- ワークフローガイド、設計ドキュメント
- JSONスキーマ定義
- ステップテンプレート
- 技術仕様書、API ドキュメント
- フレームワークごとのガイド（aws.md, gcp.md など）

**配置すべき場面:**
- SKILL.mdが500行を超えそうなとき
- 複数のドメイン/フレームワークをサポートする場合
- 詳細な手順や技術仕様を別ファイルで管理したい場合

**例:** `references/workflow_guide.md`, `references/schemas.md`, `references/phases/01_main.md`

---

### `assets/`
**出力に使用するファイル（テンプレート、アイコン、フォントなど）**

- 最終成果物として使用されるファイル
- スキルの実行結果に含まれるリソース
- ユーザーに提供するテンプレート
- スキル内部で使用するテンプレート（memoryファイル、セッション記録など）

**配置すべきファイルの例:**
- HTMLテンプレート
- CSSファイル
- 画像、アイコン、フォント
- 文書テンプレート（Markdown、LaTeXなど）
- 設定ファイルのテンプレート
- memoryファイルのテンプレート
- チェックリストテンプレート

**配置すべき場面:**
- ユーザーに提供する成果物の雛形がある
- UIコンポーネントやスタイルシートを含む
- 固定のフォーマットで出力を生成する
- スキル実行中に生成する内部ファイルの形式を定義したい

**skill-wizardでの使用例:**
- `assets/improvement_checklist_template.md` - スキル改善時のチェックリスト
- `assets/session_template.md` - セッション履歴の記録形式
- `assets/step_template.md` - ステップ構造の記述形式
- `assets/memory_skill_creation_template.md` - スキル作成時のmemoryテンプレート
- `assets/memory_skill_edit_template.md` - スキル編集時のmemoryテンプレート
- `assets/memory_test_run_template.md` - テスト実行時のmemoryテンプレート
- `assets/memory_decision_template.md` - 重要な決定事項のmemoryテンプレート

**一般的な例:** `assets/eval_review.html`, `assets/template.md`, `assets/icon.png`

---

## 判断基準のまとめ

| 特徴               | scripts/                 | references/ | assets/                 |
| ------------------ | ------------------------ | ----------- | ----------------------- |
| **実行される**     | ✓                       | ✗          | ✗                      |
| **AIが読む**       | △（必要に応じて）        | ✓          | △（テンプレートとして） |
| **出力に含まれる** | ✗（実行結果は含まれる） | ✗          | ✓                      |
| **典型的な拡張子** | .py, .sh, .js            | .md, .json  | .html, .css, .png       |

---

## スキル構造の例

```
example-skill/
├── SKILL.md                    # メインの説明（<500行推奨）
├── scripts/                    # 実行可能コード
│   ├── validate_input.py
│   └── generate_report.py
├── references/                 # 参照ドキュメント
│   ├── workflow_guide.md
│   ├── schemas.md
│   └── api_docs.md
└── assets/                     # 出力リソース
    ├── template.html
    └── icon.png
```

**skill-wizardの実際の構造:**

```
skill-wizard/
├── SKILL.md                                        # メインインデックス（100行以下）
├── assets/                                         # テンプレート集
│   ├── improvement_checklist_template.md           # 改善チェックリスト
│   ├── session_template.md                         # セッション履歴形式
│   ├── step_template.md                            # ステップ構造形式
│   ├── memory_skill_creation_template.md           # スキル作成memory
│   ├── memory_skill_edit_template.md               # スキル編集memory
│   ├── memory_test_run_template.md                 # テスト実行memory
│   └── memory_decision_template.md                 # 決定事項memory
├── references/                                     # 参照ドキュメント
│   ├── workflow_guide.md                           # ワークフロー原則
│   ├── design_philosophy.md                        # 設計思想
│   ├── file_organization.md                        # ファイル配置ガイド
│   ├── test_cases.md                               # テストケース定義
│   ├── bonus_random_ideas.md                       # ランダム案生成
│   └── phases/                                     # フェーズ別定義
│       ├── 00_prep.md                              # フェーズ1: 準備
│       ├── 01_main.md                              # フェーズ2: 設計
│       ├── 02_post.md                              # フェーズ3: 完成
│       ├── 03_edit.md                              # フェーズ4: 編集
│       └── 04_test.md                              # フェーズ5: テスト
└── scripts/                                        # スクリプト集
    ├── run_eval.py                                 # eval実行
    ├── generate_report.py                          # レポート生成
    ├── improve_description.py                      # description最適化
    └── ...
```

### スキルのmemory保存先について

memoryファイルはスキル配下ではなく、`~/.claude/skill-memory/{スキル名}/` に保存する。
pluginはインストール/アンインストールされるため、スキル配下に保存するとデータが失われる。

**保存先:** `~/.claude/skill-memory/{スキル名}/`（ディレクトリが存在しない場合は自動作成）

**ディレクトリ構造:**
用途に応じてサブフォルダを作成する:
- `history/` — セッション履歴（作成・編集・テスト等の記録）
- 必要に応じて他のフォルダを追加（例: `config/` でユーザー設定など）

```
~/.claude/skill-memory/{スキル名}/
├── history/                    # セッション履歴
│   ├── {YYYYMMDDHHMMSS}_skill_creation.md
│   └── ...
└── {その他必要なフォルダ}/
```

**ファイル命名規則（history/）:**
- `{YYYYMMDDHHMMSS}_{type}.md` 形式（例: `20260402143052_skill_creation.md`）
- 日時は秒単位まで含め、同日の複数セッションでも衝突を回避

**テンプレート:**
- `assets/memory_*_template.md` にテンプレートを配置
- 各ステップでこれらのテンプレートを参照して一貫性を保つ

---

## Progressive Disclosure（段階的な情報開示）

スキルは3層のロード方式を採用:

1. **メタデータ** (name + description) - 常にコンテキスト内（100単語程度）
2. **SKILL.md本体** - スキル起動時にコンテキスト内（<500行推奨）
3. **Bundledリソース** - 必要に応じて（制限なし、scriptsは読み込まずに実行可能）

**重要:**
- SKILL.mdは500行未満を目標にする
- この制限に近づいたら、階層を追加し、次に参照すべき場所を明確に示す
- 大きなreferenceファイル（>300行）には目次を含める
