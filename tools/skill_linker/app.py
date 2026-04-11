"""skill_linker GUI アプリケーション。"""

import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

from skill_linker import config
from skill_linker.scanner import find_skills


class SkillLinkerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Skill Linker — Claude Skill Linker")
        self.root.geometry("800x640")
        self.root.minsize(640, 520)

        self.skills: list[tuple[str, str, Path]] = []
        self.check_vars: list[tk.BooleanVar] = []

        self._build_ui()
        self._load_skills()

    # ── UI ──────────────────────────────────────────────────

    def _build_ui(self):
        # --- Claude スキルディレクトリ ---
        src_frame = ttk.LabelFrame(self.root, text="Claude スキルディレクトリ", padding=8)
        src_frame.pack(fill=tk.X, padx=10, pady=(10, 4))

        src_btn_row = ttk.Frame(src_frame)
        src_btn_row.pack(fill=tk.X, pady=(0, 4))
        ttk.Button(src_btn_row, text="追加...", command=self._add_src).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(src_btn_row, text="削除", command=self._remove_src).pack(side=tk.LEFT)

        self.src_listbox = tk.Listbox(src_frame, height=3, font=("Consolas", 9))
        self.src_listbox.pack(fill=tk.X)

        for d in config.SOURCE_DIRS:
            self.src_listbox.insert(tk.END, d)

        # --- 検出スキル一覧 ---
        skill_frame = ttk.LabelFrame(self.root, text="検出スキル一覧", padding=8)
        skill_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        btn_row = ttk.Frame(skill_frame)
        btn_row.pack(fill=tk.X, pady=(0, 4))
        ttk.Button(btn_row, text="全選択", command=lambda: self._set_all(True)).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(btn_row, text="全解除", command=lambda: self._set_all(False)).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="再読込", command=self._load_skills).pack(side=tk.RIGHT)

        canvas_frame = ttk.Frame(skill_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0, height=120)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.skill_inner = ttk.Frame(self.canvas)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.skill_inner, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _update_scroll(_event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # content fits inside canvas -> reset scroll to top, hide scrollbar
            if self.skill_inner.winfo_reqheight() <= self.canvas.winfo_height():
                self.canvas.yview_moveto(0)

        self.skill_inner.bind("<Configure>", _update_scroll)
        self.canvas.bind("<Configure>", lambda e: (
            self.canvas.itemconfig(self.canvas_window, width=e.width),
            _update_scroll(),
        ))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # --- ↓ リンク作成ボタン ---
        link_btn_frame = ttk.Frame(self.root)
        link_btn_frame.pack(fill=tk.X, padx=10, pady=4)
        tk.Button(
            link_btn_frame, text="↓ リンク作成", command=self._do_link,
            bg="#4a90d9", fg="white", activebackground="#3a7bc8", activeforeground="white",
            font=("", 10, "bold"), relief=tk.FLAT, cursor="hand2", pady=4,
        ).pack(fill=tk.X)

        # --- リンク先ディレクトリ ---
        dest_frame = ttk.LabelFrame(self.root, text="リンク先ディレクトリ", padding=8)
        dest_frame.pack(fill=tk.X, padx=10, pady=4)

        dest_btn_row = ttk.Frame(dest_frame)
        dest_btn_row.pack(fill=tk.X, pady=(0, 4))
        ttk.Button(dest_btn_row, text="追加...", command=self._add_dest).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(dest_btn_row, text="削除", command=self._remove_dest).pack(side=tk.LEFT)

        self.dest_listbox = tk.Listbox(dest_frame, height=3, font=("Consolas", 9))
        self.dest_listbox.pack(fill=tk.X)

        for d in config.DEST_DIRS:
            self.dest_listbox.insert(tk.END, d)

        # --- ログ ---
        log_frame = ttk.LabelFrame(self.root, text="ログ", padding=4)
        log_frame.pack(fill=tk.X, padx=10, pady=(4, 10))

        self.log_text = tk.Text(log_frame, height=5, state=tk.DISABLED, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.X)

    # ── ソースディレクトリ管理 ──────────────────────────────

    def _get_src_dirs(self) -> list[str]:
        return list(self.src_listbox.get(0, tk.END))

    def _save_src_dirs(self):
        config.save_env(SOURCE_DIRS=";".join(self._get_src_dirs()))
        self._load_skills()

    def _add_src(self):
        d = filedialog.askdirectory(title="Claude スキルディレクトリを追加")
        if d and d not in self._get_src_dirs():
            self.src_listbox.insert(tk.END, d)
            self._log(f"[src] added: {d}")
            self._save_src_dirs()

    def _remove_src(self):
        sel = self.src_listbox.curselection()
        if sel:
            removed = self.src_listbox.get(sel[0])
            self.src_listbox.delete(sel[0])
            self._log(f"[src] removed: {removed}")
            self._save_src_dirs()

    # ── リンク先ディレクトリ管理 ────────────────────────────

    def _get_dest_dirs(self) -> list[str]:
        return list(self.dest_listbox.get(0, tk.END))

    def _save_dest_dirs(self):
        config.save_env(DEST_DIRS=";".join(self._get_dest_dirs()))

    def _add_dest(self):
        d = filedialog.askdirectory(title="リンク先ディレクトリを追加")
        if d and d not in self._get_dest_dirs():
            self.dest_listbox.insert(tk.END, d)
            self._log(f"[dest] added: {d}")
            self._save_dest_dirs()

    def _remove_dest(self):
        sel = self.dest_listbox.curselection()
        if sel:
            removed = self.dest_listbox.get(sel[0])
            self.dest_listbox.delete(sel[0])
            self._log(f"[dest] removed: {removed}")
            self._save_dest_dirs()

    # ── スキル読み込み ──────────────────────────────────────

    def _load_skills(self):
        for w in self.skill_inner.winfo_children():
            w.destroy()

        self.skills = []
        self.check_vars = []

        src_dirs = self._get_src_dirs()
        self._log(f"[reload] scanning... ({len(src_dirs)} dirs)")

        for src in src_dirs:
            found = find_skills(Path(src))
            self.skills.extend(found)

        self._log(f"[reload] found {len(self.skills)} skills")

        if not self.skills:
            ttk.Label(self.skill_inner, text="No skills found.").pack(anchor=tk.W)
            return

        header = ttk.Frame(self.skill_inner)
        header.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(header, text="", width=3).pack(side=tk.LEFT)
        ttk.Label(header, text="スキル名", width=20, font=("", 9, "bold")).pack(side=tk.LEFT)
        ttk.Label(header, text="場所", width=40, font=("", 9, "bold")).pack(side=tk.LEFT)

        ttk.Separator(self.skill_inner, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=2)

        for name, location, path in self.skills:
            var = tk.BooleanVar(value=True)
            self.check_vars.append(var)

            row = ttk.Frame(self.skill_inner)
            row.pack(fill=tk.X, pady=1)
            ttk.Checkbutton(row, variable=var).pack(side=tk.LEFT)
            ttk.Label(row, text=name, width=20).pack(side=tk.LEFT)
            ttk.Label(row, text=location, width=40, foreground="gray").pack(side=tk.LEFT)

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

    def _selected_skills(self) -> list[tuple[str, Path]]:
        return [
            (s[0], s[2])
            for s, v in zip(self.skills, self.check_vars)
            if v.get()
        ]

    def _do_link(self):
        self._log_clear()
        selected = self._selected_skills()
        dest_dirs = self._get_dest_dirs()

        if not selected:
            self._log("[info] no skills selected")
            return

        if not dest_dirs:
            self._log("[error] no destination directories")
            return

        total_ok = 0
        total = len(selected) * len(dest_dirs)

        for dest_str in dest_dirs:
            dest = Path(dest_str)
            self._log(f"--- dest: {dest} ---")
            dest.mkdir(parents=True, exist_ok=True)

            for name, source in selected:
                link = dest / name

                # 既存のリンク/ディレクトリがあれば削除して再作成
                is_junction = link.is_dir() and link.is_junction() if hasattr(link, "is_junction") else False
                if link.exists() or link.is_symlink() or is_junction:
                    if (link.is_symlink() or is_junction) and link.resolve() == source.resolve():
                        self._log(f"  [skip] {name} -- already linked")
                        total_ok += 1
                        continue
                    # 古いリンク/ジャンクションを削除
                    if link.is_symlink() or is_junction:
                        link.rmdir()
                    else:
                        shutil.rmtree(link)
                    self._log(f"  [update] {name} -- replaced")

                try:
                    if os.name == "nt":
                        subprocess.run(
                            ["cmd", "/c", "mklink", "/J", str(link), str(source)],
                            check=True, capture_output=True,
                        )
                    else:
                        os.symlink(source, link, target_is_directory=True)
                    self._log(f"  [ok] {name}: linked")
                    total_ok += 1
                except (OSError, subprocess.CalledProcessError) as e:
                    self._log(f"  [error] {name}: {e}")

        self._log(f"--- done ({total_ok}/{total}) ---")
