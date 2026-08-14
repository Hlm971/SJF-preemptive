import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from models import Process


class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1000x780")

        self.processes = []

        # =========================
        # TITLE
        # =========================
        title = tk.Label(
            self.root,
            text="CPU SCHEDULING SIMULATOR",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        # =========================
        # PROCESS INPUT
        # =========================
        input_frame = ttk.LabelFrame(
            self.root,
            text="Process Input",
            padding=20
        )
        input_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            input_frame,
            text="PID:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.pid_entry = ttk.Entry(
            input_frame,
            width=15
        )
        self.pid_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            input_frame,
            text="Arrival Time:"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.arrival_entry = ttk.Entry(
            input_frame,
            width=15
        )
        self.arrival_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            input_frame,
            text="Burst Time:"
        ).grid(row=0, column=4, padx=5, pady=5)

        self.burst_entry = ttk.Entry(
            input_frame,
            width=15
        )
        self.burst_entry.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        add_button = ttk.Button(
            input_frame,
            text="Add Process",
            command=self.add_process
        )
        add_button.grid(
            row=0,
            column=6,
            padx=10,
            pady=5
        )

        # =========================
        # PROCESS TABLE
        # =========================
        table_frame = ttk.LabelFrame(
            self.root,
            text="Process Table",
            padding=10
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "pid",
            "arrival",
            "burst"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.tree.heading("pid", text="PID")
        self.tree.heading("arrival", text="Arrival Time")
        self.tree.heading("burst", text="Burst Time")

        self.tree.column(
            "pid",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "arrival",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "burst",
            width=150,
            anchor="center"
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # =========================
        # BUTTONS
        # =========================
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        delete_button = ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_selected
        )
        delete_button.grid(
            row=0,
            column=0,
            padx=5
        )

        reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_all
        )
        reset_button.grid(
            row=0,
            column=1,
            padx=5
        )

        gantt_button = ttk.Button(
            button_frame,
            text="Draw Gantt Chart",
            command=self.draw_gantt_chart
        )
        gantt_button.grid(
            row=0,
            column=2,
            padx=5
        )

        export_button = ttk.Button(
            button_frame,
            text="Export DOCX",
            command=self.export_docx
        )
        export_button.grid(
            row=0,
            column=3,
            padx=5
        )

        # =========================
        # GANTT CHART
        # =========================
        gantt_frame = ttk.LabelFrame(
            self.root,
            text="Gantt Chart",
            padding=10
        )
        gantt_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.canvas = tk.Canvas(
            gantt_frame,
            height=130,
            background="white"
        )
        self.canvas.pack(
            fill="x",
            expand=True
        )

    # =========================
    # ADD PROCESS
    # =========================
    def add_process(self):
        pid = self.pid_entry.get().strip()
        arrival_time = self.arrival_entry.get().strip()
        burst_time = self.burst_entry.get().strip()

        if not pid or not arrival_time or not burst_time:
            messagebox.showwarning(
                "Input Error",
                "Please enter all information."
            )
            return

        try:
            arrival_time = int(arrival_time)
            burst_time = int(burst_time)
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Arrival Time and Burst Time must be integers."
            )
            return

        if arrival_time < 0:
            messagebox.showerror(
                "Input Error",
                "Arrival Time must be greater than or equal to 0."
            )
            return

        if burst_time <= 0:
            messagebox.showerror(
                "Input Error",
                "Burst Time must be greater than 0."
            )
            return

        for process in self.processes:
            if process.pid == pid:
                messagebox.showerror(
                    "Input Error",
                    "PID already exists."
                )
                return

        process = Process(
            pid,
            arrival_time,
            burst_time
        )

        self.processes.append(process)

        self.tree.insert(
            "",
            tk.END,
            values=(
                process.pid,
                process.arrival_time,
                process.burst_time
            )
        )

        self.clear_entries()

    # =========================
    # CLEAR INPUT
    # =========================
    def clear_entries(self):
        self.pid_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)

        self.pid_entry.focus()

    # =========================
    # DELETE PROCESS
    # =========================
    def delete_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Delete Process",
                "Please select a process."
            )
            return

        for item in selected:
            values = self.tree.item(
                item,
                "values"
            )

            pid = values[0]

            self.processes = [
                process
                for process in self.processes
                if process.pid != pid
            ]

            self.tree.delete(item)

        self.draw_gantt_chart()

    # =========================
    # RESET
    # =========================
    def reset_all(self):
        self.processes.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.canvas.delete("all")

        self.clear_entries()

    # =========================
    # GANTT CHART
    # =========================
    def draw_gantt_chart(self):
        self.canvas.delete("all")

        if not self.processes:
            self.canvas.create_text(
                450,
                60,
                text="No process data",
                font=("Arial", 13)
            )
            return

        x = 40
        y = 25
        height = 50
        current_time = 0

        total_burst = sum(
            process.burst_time
            for process in self.processes
        )

        canvas_width = self.canvas.winfo_width()

        if canvas_width <= 1:
            canvas_width = 900

        available_width = canvas_width - 80
        scale = available_width / total_burst

        for process in self.processes:
            width = process.burst_time * scale

            self.canvas.create_rectangle(
                x,
                y,
                x + width,
                y + height,
                outline="black",
                width=2
            )

            self.canvas.create_text(
                x + width / 2,
                y + height / 2,
                text=process.pid,
                font=("Arial", 12, "bold")
            )

            self.canvas.create_text(
                x,
                y + height + 20,
                text=str(current_time)
            )

            current_time += process.burst_time
            x += width

        self.canvas.create_text(
            x,
            y + height + 20,
            text=str(current_time)
        )

    # =========================
    # EXPORT DOCX
    # =========================
    def export_docx(self):
        if not self.processes:
            messagebox.showwarning(
                "Export DOCX",
                "There is no process data to export."
            )
            return

        try:
            from docx import Document
        except ImportError:
            messagebox.showerror(
                "Missing Library",
                "python-docx is not installed."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save CPU Scheduling Report",
            defaultextension=".docx",
            filetypes=[
                ("Word Document", "*.docx")
            ]
        )

        if not file_path:
            return

        document = Document()

        document.add_heading(
            "CPU Scheduling Simulator",
            level=1
        )

        document.add_heading(
            "Process Information",
            level=2
        )

        table = document.add_table(
            rows=1,
            cols=3
        )

        table.style = "Table Grid"

        headers = [
            "PID",
            "Arrival Time",
            "Burst Time"
        ]

        for index, header in enumerate(headers):
            table.rows[0].cells[index].text = header

        for process in self.processes:
            cells = table.add_row().cells

            cells[0].text = str(process.pid)
            cells[1].text = str(process.arrival_time)
            cells[2].text = str(process.burst_time)

        total_burst = sum(
            process.burst_time
            for process in self.processes
        )

        document.add_paragraph()
        document.add_paragraph(
            f"Number of processes: {len(self.processes)}"
        )
        document.add_paragraph(
            f"Total burst time: {total_burst}"
        )

        document.add_heading(
            "Gantt Chart Order",
            level=2
        )

        gantt_order = " -> ".join(
            process.pid
            for process in self.processes
        )

        document.add_paragraph(gantt_order)

        document.save(file_path)

        messagebox.showinfo(
            "Export DOCX",
            "DOCX file exported successfully."
        )