<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# claude-plugin-root-unset-manual-steps

英語オリジナル: `claude-plugin-root-unset-manual-steps.md`

## 何が起きたか

`work:merge` スキル（`disable-model-invocation: true`）の手順を手動実行中、
スキル定義からコマンドをそのままコピーして実行した:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" list-active .work/tasks/index.yaml
```

結果:

```
python: can't open file '/scripts/index-tool.py': [Errno 2] No such file or directory
```

`${CLAUDE_PLUGIN_ROOT}` が空文字列に展開され、パスが `/scripts/index-tool.py` になった。

## 原因

`CLAUDE_PLUGIN_ROOT` は Claude Code のスキルランナーがスキル実行時に注入する環境変数。
`disable-model-invocation: true` のスキルを Bash ツールから手動実行する場合、
このシェル環境には env var が存在しない。

## 防止策

`${CLAUDE_PLUGIN_ROOT}` を参照するスキル手順を実行する前に、`find` でスクリプトを特定する:

```bash
find /path/to/repo -path "*/scripts/index-tool.py" | head -1
```

その後、リテラルパスで置き換えて実行:

```bash
python plugins/work/scripts/index-tool.py list-active .work/tasks/index.yaml
```
