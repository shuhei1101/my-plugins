# tkinter — GUI script conventions

Conventions for when you need a lightweight GUI. For a full-fledged GUI consider other technologies
(Electron / Tauri, etc.), but tkinter is sufficient for attaching a small operation screen to a script.

---

## Basic structure

```python
#!/usr/bin/env python3
"""フォルダ選択 + 実行ボタンの簡易 GUI。"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


# ================================================================
# テーマ / スタイル
# ================================================================

WINDOW_TITLE = "My Tool"
WINDOW_SIZE = "480x240"
PADDING = 12

# アクセントカラー（青系・統一）
ACCENT_COLOR = "#2563eb"      # tailwind blue-600
ACCENT_HOVER = "#1d4ed8"      # blue-700


# ================================================================
# UI
# ================================================================

def _apply_style(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")  # OS 非依存で見た目を統一

    # アクセントボタン
    style.configure(
        "Accent.TButton",
        background=ACCENT_COLOR,
        foreground="white",
        padding=8,
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Accent.TButton",
        background=[("active", ACCENT_HOVER)],
    )


def build_root() -> tk.Tk:
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)
    _apply_style(root)
    return root


def main() -> int:
    root = build_root()

    folder_var = tk.StringVar(value=str(Path.cwd()))

    # フォルダ選択
    folder_frame = ttk.Frame(root, padding=PADDING)
    folder_frame.pack(fill="x")
    ttk.Label(folder_frame, text="Target folder:").pack(side="left")
    entry = ttk.Entry(folder_frame, textvariable=folder_var)
    entry.pack(side="left", fill="x", expand=True, padx=8)
    ttk.Button(
        folder_frame,
        text="Browse",
        command=lambda: _on_browse(folder_var),
    ).pack(side="left")

    # 実行ボタン（アクセント）
    button_frame = ttk.Frame(root, padding=PADDING)
    button_frame.pack(fill="x", side="bottom")
    ttk.Button(
        button_frame,
        text="Run",
        style="Accent.TButton",
        command=lambda: _on_run(folder_var.get()),
    ).pack(side="right")

    root.mainloop()
    return 0


# ================================================================
# Handlers
# ================================================================

def _on_browse(var: tk.StringVar) -> None:
    """フォルダ選択ダイアログを開いて変数を更新する。"""
    selected = filedialog.askdirectory(initialdir=var.get())
    if selected:
        var.set(selected)


def _on_run(folder: str) -> None:
    """Run ボタンの処理。実処理は別関数に委譲する。"""
    try:
        # 実処理を呼ぶ
        result = _do_work(Path(folder))
        messagebox.showinfo("Done", f"Processed {result} files.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def _do_work(folder: Path) -> int:
    """対象フォルダに対する実処理。テスト可能なように分離。"""
    # 実装
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

---

## Design guidelines

1. **Separate UI from processing**: button handlers only collect arguments; delegate actual processing to a separate function (`_do_work`). This makes it testable.
2. **Fix the theme to `clam`**: the OS default (`default`) looks very different across OSes, so unify with `clam`.
3. **Accent color is blue**: unified across the whole project (based on `#2563eb`).
4. **Errors via messagebox**: don't swallow exceptions; show them to the user with `messagebox.showerror`.
5. **Modal dialogs**: build them as `tk.Toplevel` subclasses when input is required.

---

## Settings dialog pattern

```python
class SettingsDialog(tk.Toplevel):
    """設定編集モーダル。Pydantic Settings を受け取って編集する。"""

    def __init__(self, master: tk.Tk, settings: Settings) -> None:
        super().__init__(master)
        self.title("Settings")
        self.transient(master)
        self.grab_set()  # モーダル化
        self.resizable(False, False)

        self._settings = settings
        self._result: Settings | None = None

        # ----- 入力欄 -----
        self._api_key_var = tk.StringVar(value=settings.openai_api_key.get_secret_value())
        ttk.Label(self, text="OpenAI API Key:").grid(row=0, column=0, sticky="e")
        ttk.Entry(self, textvariable=self._api_key_var, width=40, show="*").grid(row=0, column=1)

        # ----- ボタン -----
        button_frame = ttk.Frame(self, padding=PADDING)
        button_frame.grid(row=99, column=0, columnspan=2, sticky="e")
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="right", padx=4)
        ttk.Button(
            button_frame, text="Save", style="Accent.TButton",
            command=self._on_save,
        ).pack(side="right")

    def _on_save(self) -> None:
        try:
            self._result = self._settings.model_copy(update={
                "openai_api_key": SecretStr(self._api_key_var.get()),
            })
            self.destroy()
        except Exception as e:
            messagebox.showerror("Validation Error", str(e), parent=self)

    @property
    def result(self) -> Settings | None:
        return self._result


# 呼び出し側
def open_settings(root: tk.Tk, current: Settings) -> Settings | None:
    dialog = SettingsDialog(root, current)
    root.wait_window(dialog)
    return dialog.result
```

---

## File / folder selection

```python
from tkinter import filedialog

# フォルダ
folder = filedialog.askdirectory(initialdir="/", title="Select folder")

# ファイル（開く）
file = filedialog.askopenfilename(
    initialdir="/",
    title="Select file",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
)

# ファイル（保存）
out = filedialog.asksaveasfilename(
    defaultextension=".json",
    filetypes=[("JSON", "*.json")],
)
```

---

## Asynchronous processing (long tasks)

To avoid blocking the GUI thread, run long tasks in a separate thread:

```python
import threading
from queue import Queue

def _on_run_async(folder: str) -> None:
    queue: Queue[tuple[str, object]] = Queue()

    def worker() -> None:
        try:
            result = _do_work(Path(folder))
            queue.put(("ok", result))
        except Exception as e:
            queue.put(("err", e))

    threading.Thread(target=worker, daemon=True).start()

    def poll() -> None:
        if queue.empty():
            root.after(100, poll)
            return
        kind, payload = queue.get()
        if kind == "ok":
            messagebox.showinfo("Done", f"Processed {payload} files.")
        else:
            messagebox.showerror("Error", str(payload))

    root.after(100, poll)
```

The key is to collect the result on tk's event loop via `root.after(ms, fn)`.

---

## Things you must not do

```python
# ❌ ロジックを handler に直書き
def _on_run(folder: str) -> None:
    # ... 長い処理がここに ...   # _do_work() に分ける

# ❌ Tk() を複数作る
root = tk.Tk()
root2 = tk.Tk()   # NG（モーダルは Toplevel）

# ❌ 例外を握りつぶす
try:
    _do_work(...)
except:
    pass   # NG（messagebox.showerror でユーザーに伝える）
```

---

## Related files

- `scripts/Pythonスクリプト.md` — single-script structure (a GUI follows the same skeleton)
- `shared/設定.md` — the side that passes Settings
- `core/コメント.md` — how to write docstrings
