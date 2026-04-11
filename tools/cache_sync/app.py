"""cache_sync GUI アプリケーション。"""

import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

from cache_sync import config
from cache_sync.scanner import find_plugins


class CacheSyncApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cache Sync — プラグインキャッシュ同期")
        self.root.geometry("720x560")
        self.root.minsize(600, 480)

        self.plugins: list[tuple[str, str, Path]] = []
        self.check_vars: list[tk.BooleanVar] = []

        self._build_ui()
        self._load_plugins()

    # ── UI ──────────────────────────────────────────────────

    def _build_ui(self):
        # --- リポジトリディレクトリ ---
        repo_frame = ttk.LabelFrame(self.root, text="プラグインリポジトリ", padding=8)
        repo_frame.pack(fill=tk.X, padx=10, pady=(10, 4))

        repo_row = ttk.Frame(repo_frame)
        repo_row.pack(fill=tk.X)

        self.repo_var = tk.StringVar(value=config.REPO_DIR)
        self.repo_entry = ttk.Entry(repo_row, textvariable=self.repo_var, font=("Consolas", 9))
        self.repo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(repo_row, text="参照...", command=self._browse_repo).pack(side=tk.LEFT)

        # --- キャッシュディレクトリ ---
        cache_frame = ttk.LabelFrame(self.root, text="キャッシュディレクトリ", padding=8)
        cache_frame.pack(fill=tk.X, padx=10, pady=4)

        cache_row = ttk.Frame(cache_frame)
        cache_row.pack(fill=tk.X)

        self.cache_var = tk.StringVar(value=config.CACHE_DIR)
        self.cache_entry = ttk.Entry(cache_row, textvariable=self.cache_var, font=("Consolas", 9))
        self.cache_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(cache_row, text="参照...", command=self._browse_cache).pack(side=tk.LEFT)

        # --- 検出プラグイン一覧 ---
        plugin_frame = ttk.LabelFrame(self.root, text="検出プラグイン一覧", padding=8)
        plugin_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        btn_row = ttk.Frame(plugin_frame)
        btn_row.pack(fill=tk.X, pady=(0, 4))
        ttk.Button(btn_row, text="全選択", command=lambda: self._set_all(True)).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(btn_row, text="全解除", command=lambda: self._set_all(False)).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="再読込", command=self._load_plugins).pack(side=tk.RIGHT)

        canvas_frame = ttk.Frame(plugin_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0, height=120)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.plugin_inner = ttk.Frame(self.canvas)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.plugin_inner, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _update_scroll(_event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            if self.plugin_inner.winfo_reqheight() <= self.canvas.winfo_height():
                self.canvas.yview_moveto(0)

        self.plugin_inner.bind("<Configure>", _update_scroll)
        self.canvas.bind("<Configure>", lambda e: (
            self.canvas.itemconfig(self.canvas_window, width=e.width),
            _update_scroll(),
        ))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # --- 更新ボタン ---
        sync_btn_frame = ttk.Frame(self.root)
        sync_btn_frame.pack(fill=tk.X, padx=10, pady=4)
        tk.Button(
            sync_btn_frame, text=">> キャッシュに反映", command=self._do_sync,
            bg="#4a90d9", fg="white", activebackground="#3a7bc8", activeforeground="white",
            font=("", 10, "bold"), relief=tk.FLAT, cursor="hand2", pady=4,
        ).pack(fill=tk.X)

        # --- ログ ---
        log_frame = ttk.LabelFrame(self.root, text="ログ", padding=4)
        log_frame.pack(fill=tk.X, padx=10, pady=(4, 10))

        self.log_text = tk.Text(log_frame, height=6, state=tk.DISABLED, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.X)

    # ── ディレクトリ選択 ────────────────────────────────────

    def _browse_repo(self):
        d = filedialog.askdirectory(title="プラグインリポジトリを選択")
        if d:
            self.repo_var.set(d)
            config.save_env(REPO_DIR=d)
            self._log(f"[repo] {d}")
            self._load_plugins()

    def _browse_cache(self):
        d = filedialog.askdirectory(title="キャッシュディレクトリを選択")
        if d:
            self.cache_var.set(d)
            config.save_env(CACHE_DIR=d)
            self._log(f"[cache] {d}")

    # ── プラグイン読み込み ──────────────────────────────────

    def _load_plugins(self):
        for w in self.plugin_inner.winfo_children():
            w.destroy()

        self.plugins = []
        self.check_vars = []

        repo_dir = self.repo_var.get().strip()
        if not repo_dir:
            ttk.Label(self.plugin_inner, text="リポジトリが未設定です。").pack(anchor=tk.W)
            return

        self._log(f"[reload] scanning... {repo_dir}")
        found = find_plugins(Path(repo_dir))
        self.plugins = found
        self._log(f"[reload] {len(found)} plugins found")

        if not found:
            ttk.Label(self.plugin_inner, text="プラグインが見つかりません。").pack(anchor=tk.W)
            return

        header = ttk.Frame(self.plugin_inner)
        header.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(header, text="", width=3).pack(side=tk.LEFT)
        ttk.Label(header, text="プラグイン名", width=24, font=("", 9, "bold")).pack(side=tk.LEFT)
        ttk.Label(header, text="バージョン", width=12, font=("", 9, "bold")).pack(side=tk.LEFT)
        ttk.Label(header, text="パス", font=("", 9, "bold")).pack(side=tk.LEFT)

        ttk.Separator(self.plugin_inner, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=2)

        for name, version, path in self.plugins:
            var = tk.BooleanVar(value=True)
            self.check_vars.append(var)

            row = ttk.Frame(self.plugin_inner)
            row.pack(fill=tk.X, pady=1)
            ttk.Checkbutton(row, variable=var).pack(side=tk.LEFT)
            ttk.Label(row, text=name, width=24).pack(side=tk.LEFT)
            ttk.Label(row, text=version, width=12, foreground="gray").pack(side=tk.LEFT)
            ttk.Label(row, text=str(path), foreground="gray").pack(side=tk.LEFT)

    # ── アクション ──────────────────────────────────────────

    def _set_all(self, val: bool):
        for v in self.check_vars:
            v.set(val)
        self._log(f"[select] {'all' if val else 'none'}")

    def _log(self, msg: str):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _log_clear(self):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _selected_plugins(self) -> list[tuple[str, str, Path]]:
        return [
            p for p, v in zip(self.plugins, self.check_vars) if v.get()
        ]

    def _do_sync(self):
        self._log_clear()
        selected = self._selected_plugins()
        cache_dir = self.cache_var.get().strip()

        if not selected:
            self._log("[info] プラグインが選択されていません")
            return

        if not cache_dir:
            self._log("[error] キャッシュディレクトリが未設定です")
            return

        # 設定を保存
        repo_dir = self.repo_var.get().strip()
        if repo_dir:
            config.save_env(REPO_DIR=repo_dir)
        config.save_env(CACHE_DIR=cache_dir)

        cache_path = Path(cache_dir)
        total_ok = 0

        for name, version, source in selected:
            dest = cache_path / name / version
            self._log(f"[sync] {name} v{version}")

            try:
                # キャッシュ先を削除して丸ごとコピー
                if dest.exists():
                    shutil.rmtree(dest)
                    self._log(f"  [clean] 既存キャッシュを削除")

                shutil.copytree(source, dest)
                self._log(f"  [ok] {source} -> {dest}")
                total_ok += 1
            except OSError as e:
                self._log(f"  [error] {e}")

        self._log(f"--- done ({total_ok}/{len(selected)}) ---")
