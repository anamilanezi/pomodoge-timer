import tkinter as tk
from tkinter import messagebox
from settings import *

class NewWindow:

    def __init__(self, window):
        self.window = window

    def open_window(self):
        self.new_window = tk.Toplevel(self.window)
        self.new_window.config(padx=15, pady=15, bg=BACKGROUND)
        self.new_window.title("Set timer")
        self.new_window.lift(aboveThis=self.window)
        self.new_window.iconbitmap('doge.ico')

        description_label = tk.Label(self.new_window, text="Customize your\npomodoro cycles: ", bg=BACKGROUND,
                                     font=('Consolas', 12, "bold"), fg=PINK)
        description_label.grid(column=0, row=0, columnspan=2, pady=10)

        work_label = tk.Label(self.new_window, text="Work time:", font=FONT_NAME, bg=BACKGROUND, fg=DARK_BLUE)
        work_label.grid(column=0, row=1, sticky="E")

        self.work_entry = tk.Entry(self.new_window, font=("Consolas", 10), width=5)
        self.work_entry.insert(0, f"{TIME_LIST[0]}")
        self.work_entry.bind("<Button-1>", self.some_callback)
        self.work_entry.grid(column=1, row=1, sticky="W")

        self.short_label = tk.Label(self.new_window, text="Short break time:", font=FONT_NAME, bg=BACKGROUND, fg=DARK_BLUE)
        self.short_label.grid(column=0, row=2, sticky="E")

        self.short_entry = tk.Entry(self.new_window, font=("Consolas", 10), width=5)
        self.short_entry.grid(column=1, row=2, sticky="W")
        self.short_entry.insert(0, f"{TIME_LIST[1]}")
        self.short_entry.bind("<Button-1>", self.some_callback)

        self.long_label = tk.Label(self.new_window, text="Long break time:", font=FONT_NAME, bg=BACKGROUND, fg=DARK_BLUE)
        self.long_label.grid(column=0, row=3, sticky="E")

        self.long_entry = tk.Entry(self.new_window, font=("Consolas", 10), width=5)
        self.long_entry.grid(column=1, row=3, sticky="W")
        self.long_entry.insert(0, f"{TIME_LIST[2]}")
        self.long_entry.bind("<Button-1>", self.some_callback)

        self.set_button = tk.Button(self.new_window, text="SET TIME",
                               width=10, font=(FONT_NAME, 9),
                               bg=DARK_BLUE,
                               fg=CREAM,
                               borderwidth=0,
                               highlightthickness=2,
                               activebackground=BLUE,
                               activeforeground=CREAM,
                               command=self.get_values)
        self.set_button.grid(column=0, row=4, columnspan=2, pady=10)

    def get_values(self):
        global TIME_LIST
        work_time = self.work_entry.get()
        short_time = self.short_entry.get()
        long_time = self.long_entry.get()
        try:
            TIME_LIST = [abs(int(work_time)), abs(int(short_time)), abs(int(long_time))]
        except ValueError:
            messagebox.showwarning(title="Oops", message="Please only numbers allowed!")
            self.new_window.lift(aboveThis=self.window)
        else:
            self.new_window.destroy()

    def some_callback(self, event):
        event.widget.delete(0, "end")
        return None
