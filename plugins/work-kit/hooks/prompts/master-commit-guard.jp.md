master/main ブランチへの直接コミットが検出されました。

**`/work-kit:work-start` を実行してワークツリーを作成し、そこでコミットしてください。**

正しいフロー:
1. `/work-kit:work-start` を実行して PR ブランチとワークツリーを作成する
2. ワークツリー内でコミットする（`../repo-wt-PR{N}/` 内）
3. `/work-kit:merge` で master にマージする

どうしても master に直接コミットする必要がある場合:
1. ユーザーに明示的な許可を得る
2. ユーザーが許可したら、ワンタイム許可トークンを作成する:
   ```
   python -c "import pathlib,tempfile; pathlib.Path(tempfile.gettempdir(),'work-kit-master-commit-guard-allowed').touch()"
   ```
3. その後、コミットを再試行する
