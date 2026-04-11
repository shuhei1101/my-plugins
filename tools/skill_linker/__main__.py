"""python -m skill_linker で起動できるようにするエントリポイント。"""

import tkinter as tk
from skill_linker.app import SkillLinkerApp

if __name__ == "__main__":
    root = tk.Tk()
    SkillLinkerApp(root)
    root.mainloop()
