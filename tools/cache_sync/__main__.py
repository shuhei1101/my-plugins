"""python -m cache_sync で起動できるようにするエントリポイント。"""

import tkinter as tk
from cache_sync.app import CacheSyncApp

if __name__ == "__main__":
    root = tk.Tk()
    CacheSyncApp(root)
    root.mainloop()
