"""プラグイン検出ロジック。"""

import json
from pathlib import Path


def find_plugins(repo_dir: Path) -> list[tuple[str, str, Path]]:
    """リポジトリの plugins/ 配下を走査し、plugin.json を持つプラグインを検出する。

    Returns: [(plugin_name, version, plugin_dir_path), ...]
    """
    plugins = []
    plugins_dir = repo_dir / "plugins"
    if not plugins_dir.exists():
        return plugins

    for plugin_json in plugins_dir.rglob(".claude-plugin/plugin.json"):
        plugin_dir = plugin_json.parent.parent
        try:
            data = json.loads(plugin_json.read_text(encoding="utf-8"))
            name = data.get("name", plugin_dir.name)
            version = data.get("version", "unknown")
        except (json.JSONDecodeError, OSError):
            name = plugin_dir.name
            version = "unknown"
        plugins.append((name, version, plugin_dir))

    return plugins
