<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python テスト規約 — py-kit（日本語ミラー）

> このファイルは `python-testing.md` の日本語ミラーです。Claude Code には読み込まれません。

Python プロジェクトのロガー設定とテストポリシー。

---

## ロガー仕様

全プロジェクトに `{package_name}/logger.py` を作成し、`setup_logger()` 関数を実装する：

- `constants.py` に `LOG_DIR = PROJECT_ROOT / "log"` を定義する
- `setup_logger()` で `LOG_DIR.mkdir(parents=True, exist_ok=True)` を呼ぶ
- ログファイル名：`LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — 実行毎に新規ファイル
- `StreamHandler(sys.stdout)` と `FileHandler(..., encoding="utf-8")` の両方をアタッチする
- フォーマット：`[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- ハンドラー重複ガード：`if logger.handlers: return logger`
- サブモジュール：`get_logger(__name__)`

`main.py` / `__main__.py` のエントリ直後に `setup_logger()` を呼ぶ。

---

## テストポリシー

| テスト種別 | ポリシー |
|---|---|
| ユニットテスト（個別メソッド・関数） | 書かない — AI 支援開発ではメンテナンスコストが価値を上回る |
| モジュール統合テスト | モジュールが非自明な形で相互作用する場合に書く |
| ユースケーステスト | ユースケース毎に書く。外部 I/O 境界のみモックする |
| E2E テスト | CLI エントリーポイントと HTTP API エンドポイントに書く |

pytest を使う。`tests/` でソースフォルダ構造をミラーリングする。再利用可能なモックは `tests/mocks/` に置く。

ソースファイルとテストファイルはリンクしている — ソースファイルを変更したら対応するテストを必ず確認・更新する。

### テスト構成

```
tests/
├── mocks/
│   ├── mock_env.py       # 環境変数モックヘルパー
│   └── mock_externals.py # 外部 API / DB クライアントのスタブ
├── conftest.py           # 共有 pytest フィクスチャ
└── {feature}/
    └── test_{feature}.py
```

テストは外部 I/O 境界（DB・API・ファイルシステム）のみモックする — 個別メソッドのユニットテストは書かない。
