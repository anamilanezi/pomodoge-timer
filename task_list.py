import tkinter as tk
from tkinter import messagebox
from settings import *


class TaskList:

    def __init__(self, window, row, column):
        self.row = row
        self.new_row = row + 1
        self.column = column
        self.textentry = tk.Entry(window,
                                  font=("Consolas", 10),
                                  fg=DARK_BLUE,
                                  relief="flat",
                                  selectbackground=DARK_BLUE,
                                  selectforeground=BACKGROUND)
        self.textentry.insert(0, "Enter a task")
        self.textentry.bind("<Button-1>", self.some_callback)
        self.textentry.grid(row=self.row, column=self.column, sticky="EW", columnspan=2, pady=3, padx=3)
        add = tk.Button(text="Add",
                        font=(FONT_NAME, 9),
                        bg=ORANGE,
                        fg=CREAM,
                        borderwidth=0,
                        highlightthickness=2,
                        activebackground=DARK_BLUE,
                        activeforeground=CREAM,
                        command=self.add_checkbox)
        add.grid(row=self.new_row, column=self.column + 1, sticky="NE", padx=3)

    def add_checkbox(self):
        if self.new_row > 15:
            messagebox.showwarning(title="Wow much tasks", message="Please complete a task before adding another!")
            return
        task = self.textentry.get()
        if task == "" or task == "Enter a task":
            messagebox.showwarning(title="Such emptiness", message="Write some text to add a task!")
            return
        self.check = tk.Checkbutton(text=task,
                                    background=BACKGROUND,
                                    font=("Consolas", 9),
                                    foreground=DARK_BLUE,
                                    activebackground=BACKGROUND)
        self.check.grid(row=self.new_row, column=self.column, columnspan=3, sticky="NW", padx=3)
        self.textentry.delete(0, "end")
        self.new_row += 1
        print(self.new_row)

    def some_callback(self, event):
        event.widget.delete(0, "end")
        return None

    def change_color(self):
        self.check.config(font=("Consolas", 9, "italic"), foreground=BLUE)
