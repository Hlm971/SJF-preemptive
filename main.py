import tkinter as tk
from ui import SchedulerApp


def main():
    root = tk.Tk()

    app = SchedulerApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()