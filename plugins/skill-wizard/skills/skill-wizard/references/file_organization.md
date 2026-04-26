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

### `examples/`
**具体的な記載例・サンプル出力**

- AIが Few-shot 的に参照するための具体的なサンプル
- 実際のユースケースに基づいたリアルな記載例
- スキル実行時にAIが出力形式の参考にするファイル
- プレースホルダーなし・空白なしの完成形サンプル

**配置すべきファイルの例:**
- memoryファイルの記載例（実際のスキル名・日時・内容を含む）
- セッション履歴の記載例
- ステップ記述の記載例
- チェックリストの記載例

**配置すべき場面:**
- AIに「このような形式で出力してほしい」という具体例を示したい
- テンプレートよりも完成形のサンプルの方が参照しやすい場面
- Few-shot learning 的にAIの出力品質を高めたい場面

**skill-wizardでの使用例:**
- `examples/improvement_checklist_example.md` - スキル改善時のチェックリスト具体例
- `examples/session_example.md` - セッション管理の具体例
- `examples/step_example.md` - ステップ構造の記述具体例
- `examples/memory_skill_creation_example.md` - スキル作成時のmemory具体例
- `examples/memory_skill_edit_example.md` - スキル編集時のmemory具体例
- `examples/memory_test_run_example.md` - テスト実行時のmemory具体例
- `examples/memory_decision_example.md` - 重要な決定事項のmemory具体例

**一般的な例:** `examples/eval_review.html`, `examples/sample_output.md`

---

## 判断基準のまとめ

| 特徴               | scripts/                 | references/ | examples/                 |
| ------------------ | ------------------------ | ----------- | ------------------------- |
| **実行される**     | ✓                       | ✗          | ✗                        |
| **AIが読む**       | △（必要に応じて）        | ✓          | ✓（Few-shot参照として）   |
| **出力に含まれる** | ✗（実行結果は含まれる） | ✗          | △（出力形式の参考に使う） |
| **典型的な拡張子** | .py, .sh, .js            | .md, .json  | .md, .html                |

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
└── examples/                   # 具体的な記載例・サンプル出力
    ├── sample_output.md
    └── session_example.md
```

**skill-wizardの実際の構造:**

```
skill-wizard/
├── SKILL.md                                        # メインインデックス（100行以下）
├── examples/                                       # 具体的な記載例集
│   ├── improvement_checklist_example.md            # 改善チェックリスト具体例
│   ├── session_example.md                          # セッション管理具体例
│   ├── step_example.md                             # ステップ構造具体例
│   ├── memory_skill_creation_example.md            # スキル作成memory具体例
│   ├── memory_skill_edit_example.md                # スキル編集memory具体例
│   ├── memory_test_run_example.md                  # テスト実行memory具体例
│   └── memory_decision_example.md                  # 決定事項memory具体例
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

**具体的な記載例:**
- `examples/memory_*_example.md` に具体例を配置
- 各ステップでこれらの例を Few-shot 参照として活用し一貫性を保つ

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
