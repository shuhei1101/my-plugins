<!-- This file is a Japanese mirror of Tkinter.md. When updating the English original, update this file too. -->
# tkinter — GUI スクリプト規約

簡易 GUI が必要な場合の規約。本格的な GUI は別技術を検討（Electron / Tauri 等）するが、
スクリプトに小さい操作画面を付ける程度なら tkinter で十分。

---

## 基本構造

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

## 設計指針

1. **UI と処理を分離**: ボタン handler は引数を集めるだけ、実処理は別関数（`_do_work`）に委譲。テスト可能になる
2. **テーマは `clam` 固定**: OS デフォルト（`default`）は OS 間で見た目が大きく違うので、`clam` で統一
3. **アクセントカラーは青**: プロジェクト全体で統一（`#2563eb` 基準）
4. **エラーは messagebox**: 例外を握りつぶさず `messagebox.showerror` でユーザーに見せる
5. **モーダルダイアログ**: 入力が必要なら `tk.Toplevel` 派生で作成

---

## 設定ダイアログのパターン

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

## ファイル / フォルダ選択

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

## 非同期処理（長い処理）

GUI スレッドをブロックしないよう、長い処理は別スレッドで:

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

`root.after(ms, fn)` で tk のイベントループ上で結果を回収するのがポイント。

---

## やってはいけないこと

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

## 関連ファイル

- `scripts/Pythonスクリプト.md` — 単一スクリプト構造（GUI も同様の骨格）
- `shared/設定.md` — Settings を渡す方
- `core/コメント.md` — docstring の書き方
