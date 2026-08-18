import tkinter as tk

from ui import SchedulerApp
from test_loader import load_test_case

root = tk.Tk()

app = SchedulerApp(root)

app.processes = load_test_case(
    "test1000.txt"
)
root.mainloop()