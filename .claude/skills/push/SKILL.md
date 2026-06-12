---
name: push
description: pushする。スキルを実行すると自動でpush処理が実行される。
---

## pushを実行する
```!
python .claude/hooks/post-merge-upgrade.py
```
- master へのマージ後に push + marketplace upgrade + reload-plugins を実行。
