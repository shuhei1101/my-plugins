<!-- This file is a Japanese mirror of common-component-first.md. When updating the English original, update this file too. -->

# 共通コンポーネント先読み

> このファイルは `common-component-first.md` の日本語ミラーです(`plugins/dev-kit/references/html/common-component-first.jp.md` に配置)。
> Claude Code には自動読み込まれません。英語版を更新したら同じ変更を反映してください。

任意の画面に UI マークアップ・スタイル・DOM アクセスを追加する前に、**プロジェクトの共有リソースを先に読む**:

1. `static/js/constants.js`(相当) — デザイントークン・ブレイクポイント・デフォルト値
2. `static/js/routes.js`(相当) — 全 URL / ルート定義
3. CSS のコンポーネント層 — すべての `c-*` 定義(例: `static/css/component.css`)
4. JS のコンポーネント層 — すべての共有コンポーネントモジュール(例: `static/js/components/`)

## なぜ

画面が既存のトースト・ダイアログ・ボタン・スケルトンを独自に再実装すると、コードベースが
断片化しデザインが不統一になる。再利用は必須であり、任意ではない。

## どうするか

- 必要なコンポーネントが**存在する**: インポート / 参照する。小さなバリアントが必要なら props / modifier で拡張
- 必要なコンポーネントが**存在しない**が汎用的: 共有層に追加してから使う。インラインに書かない
- 真に画面固有のもの: その画面の `p-*`(Project)層へ。それでも値は `constants.js` / トークン経由

## 禁止事項

- 単発のスケルトン / トースト / ダイアログ / モーダルを画面モジュールにインラインで書く
- 色の 16 進・ピクセル値・URL・魔法文字列を画面コード内にハードコード
- `c-*` ブロックを画面にコピーして「この画面用」と名前変更

## ルールの保守

プロジェクトで新しい共有層を導入する場合(例: `feature/` や `widget/`)は、本ルールの
「先に読むリスト」に追加する。
