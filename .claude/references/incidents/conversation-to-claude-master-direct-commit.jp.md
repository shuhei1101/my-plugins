# conversation-to-claude が PR ブランチではなく master 直接コミットになっていた

## 発生状況

`work-kit:merge` スキルの Step 3 で `claude-kit:conversation-to-claude` を呼び出していたが、
このとき cwd は **master ブランチのメインリポジトリ**だった。

`conversation-to-claude` は `.claude/rules/` や `.claude/references/` にファイルを書き、
最後に `git commit` するが、cwd が master なので**コミットも master 直接行き**になっていた。

その後 PR ブランチを `--no-ff` でマージしても、glossary や incidents の追記は
別コミット（master 直接）として残り、PR の作業内容として一体化しなかった。

## 影響

- master の git log に `docs: PR{N} — ... を glossary に追加` のようなコミットが
  PR マージコミットとは別に乱立
- PR 単位で revert したくても glossary / incidents 部分が残る
- 「PR の作業内容」と「セッション知識」が論理的に同じ単位なのに別コミットになる

## 修正内容

PR93 で `work-kit:merge` Step 4（旧 Step 3）を変更:

```bash
# 修正前: master の cwd で実行
/claude-kit:conversation-to-claude

# 修正後: ワークツリーに cd してから実行
cd ../$(basename $(pwd))-wt-PR{N}
/claude-kit:conversation-to-claude
# 必要ならワークツリーで commit
git -C ../$(basename $(pwd))-wt-PR{N} add .claude/
git -C ../$(basename $(pwd))-wt-PR{N} commit -m "docs: conversation-to-claude artifacts #PR{N}"
cd -
```

これにより `.claude/` 配下の生成物が PR ブランチに含まれ、`--no-ff` マージコミットに同梱される。

## 教訓

**他のスキルにファイル書き込みを委譲する場合、呼び出し元はターゲットの cwd を明示的に制御すること。**

特に `git commit` を含むスキルは、誰のブランチにコミットされるかが cwd 依存になる。
master ブランチで作業すべきでないファイル変更を委譲する際は、必ずワークツリー（または該当ブランチ）に
`cd` してから呼び出す。
