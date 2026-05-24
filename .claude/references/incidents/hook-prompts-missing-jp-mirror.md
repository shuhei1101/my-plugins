# hook-prompts-missing-jp-mirror

## 何が起きたか

PR104 で dev-kit プラグインのフック用プロンプトファイル（`hooks/prompts/python-skill-dispatch.md`、`yaml-skill-dispatch.md`）を作成したが、JP ミラー（`*.jp.md`）を同時に作らなかった。
ユーザーから「プロンプトを作るときは必ず日本語ミラーも作れ」と指摘を受け、追加コミットが発生した。

## 原因

- `SKILL.md` の JP ミラーについては `skill-jp-mirror-sync.md` ルールが存在しており習慣化していた
- `hooks/prompts/` 配下のプロンプトファイルについては対応ルールが存在せず、ミラー作成が抜け落ちた

## 修正

- `python-skill-dispatch.jp.md` / `yaml-skill-dispatch.jp.md` を追加コミット
- `hook-prompts-jp-mirror-sync.md` ルールを新規作成して自動的に気づける仕組みを整備

## 教訓

**フック用プロンプトファイル（`hooks/prompts/*.md`）を作成・編集するときは、必ず同じコミットで `*.jp.md` の JP ミラーも作成する。**

`skill-jp-mirror-sync.md` と同様のリンクルールとして `hook-prompts-jp-mirror-sync.md` を設け、ファイル連携を強制する。
