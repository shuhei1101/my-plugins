<!-- This file is a Japanese mirror of askuserquestion.md — human reference only. Do NOT load this file directly. Edit the JP mirror first, then apply changes to the English source. -->

# AskUserQuestion 使用ガイド

スキル内から `AskUserQuestion` ツールを呼び出す際の制約と正しい使い方。

English source: `references/common/askuserquestion.md`

---

## 使用するタイミング

`AskUserQuestion` を呼び出してよいのは、**スキル定義またはユーザーが明示的に指示した場合のみ**。

タスクの途中で確認・質問が必要になった場合は、**通常のテキストとして質問を書いてターンを終了する** — `AskUserQuestion` を呼んではいけない。

**理由**: `AskUserQuestion` は Stop フックを発火させない。スキル外で呼ぶと stop-hook 通知システムがバイパスされる。

---

## 質問数

| 項目 | 制約 |
|---|---|
| 最小 | 1 質問 |
| 最大 | 4 質問（1 回の呼び出しで） |

---

## options の制約

| 項目 | 制約 |
|---|---|
| 最小 | 2 個 |
| 最大 | 4 個 |
| "Other" | UI が自動で末尾に付与する — 手動で追加してはいけない |

---

## フィールド詳細

### `question`

質問文全体。疑問符で終わること。

### `header`

チップ/タグとして表示される短いラベル。**最大 12 文字**。例: `"認証方式"`、`"ライブラリ"`、`"アプローチ"`。

### `options[].label`

ユーザーが見て選ぶ選択肢のテキスト（1〜5 語）。特定の選択肢を推奨する場合は、それをリストの先頭に置き、ラベル末尾に `"（推奨）"` を付ける。

### `options[].description`

その選択肢の説明 — トレードオフ、影響範囲、選んだ場合に何が起きるか。

### `multiSelect`

`true` にすると複数選択可。**選択肢が排他的でない場合**に使う。
質問文もそれに合わせる（例: 「有効にする機能を選んでください」）。

**制約**: `preview` は single-select（`multiSelect: false`）のみ対応。

---

## preview フィールド

視覚的に比較させたい場合に `options[].preview` を使う。
適したコンテンツ: ASCII モックアップ、コードスニペット、ダイアグラム、設定例。

単純な好み質問（ラベルと description で十分な場合）には使わないこと。

```yaml
options:
  - label: "クラス構造"
    description: "状態を持つ処理に向く。"
    preview: |
      ```python
      class Processor:
          def __init__(self, cfg):
              self.cfg = cfg

          def run(self):
              ...
      ```
  - label: "関数構造"
    description: "シンプルなパイプラインに向く。"
    preview: |
      ```python
      def process(cfg):
          ...
      ```
```

いずれかの選択肢に `preview` がある場合、UI は左に選択肢リスト・右にプレビューの 2 カラムレイアウトに切り替わる。
コンテンツは Markdown としてモノスペースボックスでレンダリングされる。改行を含む複数行テキストも有効。

---

## アンチパターン

| # | アンチパターン | 正しい方法 |
|---|---|---|
| 1 | options を 5 個以上並べる | 複数の質問に分割するか、プレーンテキストの番号付きリストを使う |
| 2 | "Other" を手動で追加する | 不要 — UI が自動で付与する |
| 3 | `multiSelect: true` に `preview` を付ける | `preview` は single-select のみ使用可 |
| 4 | スキル外で `AskUserQuestion` を呼ぶ | プレーンテキストで質問を書いてターンを終了する |
