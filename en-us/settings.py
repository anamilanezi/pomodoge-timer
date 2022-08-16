import datetime as dt
from image_data import create_list
import urllib.request


def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False


online = connect()
secs = 60

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#CC435F"
LIGHT_PINK = "#f7cdd7"
RED = "#bb371a"
DARK_BLUE = "#333C83"
YELLOW = "#FEE440"
BLUE = "#36A3EB"
CREAM = "#FEF9EF"
BACKGROUND = "#A2D2FF"
ORANGE = "#FF865E"

FONT_NAME = "Fixedsys"

TIME_LIST = [25, 5, 20]

TEXTS = {
    "quantifiers": ["SUCH", "MUCH", "MANY"],
    "work": ["WORK", "JOBS", "TASKS", "BUSY", "FOCUS", "CHORES", "EFFORTS", "DUTIES"],
    "short": ["COFFEE", "WATER", "BREATH", "BREAK", "PAUSE", "FIVE"],
    "long": ["INTERVAL", "NAP", "REST", "WOW", "STRETCH"]
}

offline_pics = ["images/doge00.png", "images/doge01.png", "images/doge02.png", "images/doge03.png", "images/doge04.png",
                "images/doge05.png", "images/doge06.png", "images/doge07.png", "images/doge08.png", "images/doge09.png",
                "images/doge10.png", "images/doge11.png", "images/doge12.png"]

# ---------------------------- VARIABLES ------------------------------- #

images_list = create_list("shibes")

day = dt.datetime.now().today().strftime('%Y-%m-%d')
start_time = 0
working_time = []
work_finished = 0
saved = None

reps = 0
checks = []
pomos = []

timer = None
is_paused = False

