# PUSHEENTIMER #
import task_list as tl
import PIL
from playsound import playsound
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import choice
from settings import *
from image_data import *


def update_work_data(current_cycle):
    global checks, work_finished, pomos

    if current_cycle % 2 == 0:
        checks.append("✓")
        check_text = "".join(checks)
        checks_label.config(text=check_text)
        work_finished += 1

    if len(checks) == 4 and current_cycle % 8 == 0:
        checks = []
        pomos.append("🍅")

        if len(pomos) >= 4:
            pomo_text = f"{len(pomos)}🍅"
        else:
            pomo_text = "".join(pomos)
        # if len(pomos) % 4 == 0:
        #     pomos.append("\n")
        checks_label.config(text="")
        cycle_label.config(text=pomo_text)


def save_report():
    global saved
    saved = dt.datetime.now().time().isoformat(timespec='seconds')

    with open('pomoreport.csv', mode='a') as file:
        if file.tell() == 0:
            file.write(f"day;start_time;working_time_min;finished_work;full_pomodoros;saved\n")
        file.write(f"{day};{start_time};{sum(working_time[:work_finished])};{work_finished};{len(pomos)};{saved}\n")


def save_before_closing():
    if work_finished == 0:
        window.destroy()
    else:
        if saved is None:
            last_save_msg = "You haven't saved anything in this session."
        else:
            last_save_msg = f"Last report was saved at {saved}"
        wants_to_save = messagebox.askyesnocancel(title="Save report", message=f"Do you want to save your report before"
                                                                               f"closing?\n{last_save_msg}")
        if wants_to_save is None:
            return
        elif wants_to_save:
            save_report()
            window.destroy()
        else:
            window.destroy()


# ---------------------------- SET CUSTOM TIME ------------------------------- #
def open_window():

    def get_values():
        global TIME_LIST
        work_time = work_entry.get()
        short_time = short_entry.get()
        long_time = long_entry.get()
        try:
            TIME_LIST = [abs(int(work_time)), abs(int(short_time)), abs(int(long_time))]
        except ValueError:
            messagebox.showwarning(title="Oops", message="Please only numbers allowed!")
            new_window.lift(aboveThis=window)
        else:
            new_window.destroy()

    def some_callback(event):
        event.widget.delete(0, "end")
        return None

    new_window = tk.Toplevel(window)
    new_window.config(padx=15, pady=15, bg=BACKGROUND)
    new_window.title("Set timer")
    new_window.lift(aboveThis=window)
    new_window.iconbitmap('doge.ico')

    description_label = tk.Label(new_window, text="Customize your\npomodoro cycles: ", bg=BACKGROUND,
                                 font=('Consolas', 12, "bold"), fg=PINK)
    description_label.grid(column=0, row=0, columnspan=2, pady=10)

    work_label = tk.Label(new_window, text="Work time:", font=FONT_NAME, bg=BACKGROUND, fg=DARK_BLUE)
    work_label.grid(column=0, row=1, sticky="E")

    work_entry = tk.Entry(new_window, font=("Consolas", 10), width=5)
    work_entry.insert(0, f"{TIME_LIST[0]}")
    work_entry.bind("<Button-1>", some_callback)
    work_entry.grid(column=1, row=1, sticky="W")

    short_label = tk.Label(new_window, text="Short break time:", font=FONT_NAME, bg=BACKGROUND, fg=DARK_BLUE)
    short_label.grid(column=0, row=2, sticky="E")

    short_entry = tk.Entry(new_window, font=("Consolas", 10), width=5)
    short_entry.grid(column=1, row=2, sticky="W")
    short_entry.insert(0, f"{TIME_LIST[1]}")
    short_entry.bind("<Button-1>", some_callback)

    long_label = tk.Label(new_window, text="Long break time:", font=FONT_NAME, bg=BACKGROUND, fg=DARK_BLUE)
    long_label.grid(column=0, row=3, sticky="E")

    long_entry = tk.Entry(new_window, font=("Consolas", 10), width=5)
    long_entry.grid(column=1, row=3, sticky="W")
    long_entry.insert(0, f"{TIME_LIST[2]}")
    long_entry.bind("<Button-1>", some_callback)

    set_button = tk.Button(new_window, text="SET TIME",
                           width=10, font=(FONT_NAME, 9),
                           bg=DARK_BLUE,
                           fg=CREAM,
                           borderwidth=0,
                           highlightthickness=2,
                           activebackground=BLUE,
                           activeforeground=CREAM,
                           command=get_values)
    set_button.grid(column=0, row=4, columnspan=2, pady=10)


# ------------------------------ PAUSE TIMER --------------------------------- #
def pause_timer():
    global is_paused

    if is_paused:
        if start_time == 0:
            return
        pause_bt.config(text="PAUSE", bg=ORANGE, activebackground=BLUE)
        is_paused = False

        # Get current time at countdown
        current_count = canvas_clock.itemcget(timer_text, 'text')

        count_list = current_count.split(":")
        minutes = int(count_list[0]) * 60
        seconds = int(count_list[1])
        count = minutes + seconds
        count_down(count)
    else:
        is_paused = True
        pause_bt.config(text="RESUME", bg=DARK_BLUE, activebackground=ORANGE)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    try:
        window.after_cancel(timer)
        pause_bt.config(text="PAUSE", bg=ORANGE, state="disabled")
        start_bt.config(state="normal", bg=ORANGE)
        title_label.config(text=f"POMODOGE", fg=DARK_BLUE)
        canvas_clock.itemconfig(timer_text, text="00:00")
        checks_label.config(text="")
        global reps, is_paused, checks
        checks = []
        reps = 0
        is_paused = False
    except ValueError:
        pass


# # -------------------------- CHANGE CONFIG  ------------------------------- #

def change_photo(online_mode):
    global photo

    if online_mode:
        pass
    # ONLINE USES data=dog
        dog = resize_random(images_list)
        photo = ImageTk.PhotoImage(data=dog)
    else:
        #### offline
        file = rf"{choice(offline_pics)}"
        dog = PIL.Image.open(file)
        photo = ImageTk.PhotoImage(dog)
        ####

    doge_label.config(image=photo)


def change_text(type):
    first_word = choice(TEXTS["quantifiers"])
    if type == "short":
        second_word = choice(TEXTS["short"])
    elif type == "long":
        second_word = choice(TEXTS["long"])
    else:
        second_word = choice(TEXTS["work"])

    return f"{first_word} {second_word}"


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, working_time, start_time

    pause_bt.config(state="normal", bg=ORANGE)
    start_bt.config(state="disabled", disabledforeground=BACKGROUND)
    change_photo(online)


    if start_time == 0:
        start_time = dt.datetime.now().time().isoformat(timespec='seconds')
        checks_label.config(text="")
        cycle_label.config(text="")

    reps += 1

    work_min = TIME_LIST[0]
    short_break_min = TIME_LIST[1]
    long_break_min = TIME_LIST[2]

    work_sec = work_min * secs  # 60
    short_break_sec = short_break_min * secs  # 60
    long_break_sec = long_break_min * secs  # 60

    if not is_paused:

        if reps % 8 == 0:
            count = long_break_sec
            playsound('longbreak.wav')
            wow_label.config(text="wow long break")
            text = change_text("long")
            title_label.config(text=text, fg=RED, font=(FONT_NAME, 32))

        elif reps % 2 == 0:
            count = short_break_sec
            playsound('shortbreak.wav')
            wow_label.config(text="wow break")
            text = change_text("short")
            title_label.config(text=text, fg=PINK, font=(FONT_NAME, 32))

        else:
            working_time.append(work_min)
            count = work_sec
            playsound('work.wav')
            wow_label.config(text="ok work")
            text = change_text("work")
            title_label.config(text=text, fg=DARK_BLUE, font=(FONT_NAME, 32))

        count_down(count)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer

    count_time = count
    count_min = count_time // 60
    count_seg = count_time % 60

    if count_seg < 10:
        count_seg = f"0{count_seg}"

    # To change the content of a text from canvas, first it has to be assigned to a variable to use itemconfig with
    # the canvas object
    if not is_paused:
        canvas_clock.itemconfig(timer_text, text=f"{count_min}:{count_seg}")
        if count > 0:
            timer = window.after(1000, count_down, count_time - 1)

        else:
            start_timer()
            update_work_data(reps)


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Pomodoge Timer")
window.config(padx=20, pady=15, bg=BACKGROUND)
window.iconbitmap('doge.ico')

# HEADER -------------------------------------------------------------- #
title_label = tk.Label(text="POMODOGE",
                       fg=DARK_BLUE,
                       bg=BACKGROUND,
                       font=(FONT_NAME, 32),
                       width=13)
title_label.grid(column=3,
                 row=21,
                 columnspan=2,
                 stick="Ew")

wow_label = tk.Label(text="wow much efficiency",
                     bg=BACKGROUND,
                     fg=YELLOW,
                     font=('Comic Sans MS', 12, "bold"))

wow_label.grid(column=3,
               row=22,
               columnspan=2,
               sticky="EW")

# USING API:
# try:
if online:
    dog = resize_random(images_list)
    photo = ImageTk.PhotoImage(data=dog)
else:
    dog = PIL.Image.open(r"images/doge01.png")
    photo = ImageTk.PhotoImage(dog)

doge_label = tk.Label(image=photo)
doge_label.grid(column=0, row=3, columnspan=3, rowspan=17, pady=10, sticky="W")

# TIMER  -------------------------------------------------------------- #
canvas_clock = tk.Canvas(width=300, height=108, bg=BACKGROUND, highlightthickness=0)
clock_img = tk.PhotoImage(file='images/clock4.png')
canvas_clock.create_image(150, 54, image=clock_img)

timer_text = canvas_clock.create_text(150, 54, text="00:00", fill=DARK_BLUE, font=('Consolas', 36, 'bold'))
canvas_clock.grid(column=0, row=21, rowspan=4, columnspan=3, pady=5, sticky="EW")

# ORANGE ------------------------------------------------------------- #
start_bt = tk.Button(text="START",
                     width=6, font=(FONT_NAME, 9),
                     bg=ORANGE,
                     fg=CREAM,
                     borderwidth=0,
                     highlightthickness=2,
                     activebackground=YELLOW,
                     activeforeground=CREAM,
                     command=start_timer)

start_bt.grid(column=0, row=0, sticky="EW")

pause_bt = tk.Button(text="PAUSE",
                     width=6,
                     font=(FONT_NAME, 9),
                     bg=ORANGE,
                     fg=CREAM,
                     borderwidth=0,
                     highlightthickness=2,
                     activebackground=YELLOW,
                     activeforeground=CREAM,
                     disabledforeground=BACKGROUND,
                     state="disabled",
                     command=pause_timer)
pause_bt.grid(column=1, row=0, sticky="EW", padx=6)

reset_bt = tk.Button(text="RESET",
                     width=6,
                     font=(FONT_NAME, 9),
                     bg=ORANGE,
                     fg=CREAM,
                     borderwidth=0,
                     highlightthickness=2,
                     activebackground=YELLOW,
                     activeforeground=CREAM,
                     command=reset_timer)
reset_bt.grid(column=2, row=0, sticky="EW")

set_time_bt = tk.Button(text="SETTINGS",
                        font=(FONT_NAME, 9),
                        width=6,
                        bg=ORANGE,
                        fg=CREAM,
                        borderwidth=0,
                        highlightthickness=2,
                        activebackground=DARK_BLUE,
                        activeforeground=CREAM,
                        command=open_window
                        )
set_time_bt.grid(column=3, row=0, sticky="EW", padx=6)

save_report_bt = tk.Button(text="SAVE",
                           font=(FONT_NAME, 9),
                           width=6,
                           bg=ORANGE,
                           fg=CREAM,
                           borderwidth=0,
                           highlightthickness=2,
                           activebackground=DARK_BLUE,
                           activeforeground=CREAM,
                           command=save_report
                           )
save_report_bt.grid(column=4, columnspan=2, row=0, sticky="EW")

# CYCLE COUNTER ------------------------------------------------------- #
checks_label = tk.Label(text="🍅🍅🍅", fg=DARK_BLUE, bg=BACKGROUND, font=("Consolas", 16))
checks_label.grid(column=3, row=23, sticky="E")

cycle_label = tk.Label(text="🍅🍅🍅", fg=PINK, bg=BACKGROUND, font=("Consolas", 16))
cycle_label.grid(column=4, row=23, sticky="W")


task = tl.TaskList(window, row=3, column=3)

window.protocol('WM_DELETE_WINDOW', save_before_closing)

window.mainloop()
