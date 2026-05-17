# QA — PR47 未決定事項

**運用方針**:
1. 未決定事項が発生 → このファイルに QA-XXX（連番）として追加
2. ユーザーと議論・判断 → 決定
3. 決定したら → 対応する仕様書・ドキュメントに反映する

---

## QA-001: 旧 py-kit / yaml-rule プラグインの扱い

**状態**: 未決定

`dev-kit` に統合後、旧 `plugins/py-kit/` と `plugins/yaml-rule/` をどう扱うか:

- A: 完全に削除する（`marketplace.json` からも除外）
- B: `marketplace.json` からは外すが、ディレクトリは残す
- C: ディレクトリも残し、`marketplace.json` でも別名で残す（移行期間）

**前提**: TODO の現案は A（削除）。

---

## QA-002: `references/` 初期内容のスコープ

**状態**: 未決定

`references/` 配下に置く各ファイルの初期内容:

- `python.md`: 旧 `py-kit/references/python-standards.md` の内容を移植（中身ほぼそのまま）
- `yaml.md`: 旧 `yaml-rule/skills/yaml-rule/SKILL.md` から規約部分を抽出
- `common.md` / `frontend.md` / `backend.md` / `vscode-extension.md`: 雛形のみ（プレースホルダ）で OK か?

**前提**: TODO の現案は「python.md と yaml.md は実内容を入れ、それ以外は雛形のみ」。

---

## QA-003: スキル名の維持

**状態**: 未決定

統合に合わせてスキル名を変更するか:

- A: 現状維持（`py-script`, `py-project`, `py-new-project`, `yaml-rule`）
- B: `dev-kit:` プレフィックスを意識した命名にリネーム

**前提**: TODO の現案は A（現状維持）。プラグイン名が `dev-kit` になることで自動的に `dev-kit:py-script` のように呼ばれるため、スキル単体の名前は変えない。

---

## QA-004: `dev-kit` プラグインの初期バージョン

**状態**: 未決定

新プラグインの `version` を `1.0.0` で開始するか、`py-kit` の `2.0.1` を継承するか。

**前提**: TODO の現案は `1.0.0`（新プラグインとして新規開始）。
