# config.py
import os

BASE_DIR = os.path.dirname(__file__)
USERDATA_DIR = os.path.join(BASE_DIR, "userdata")
os.makedirs(USERDATA_DIR, exist_ok=True)

BINDINGS_PATH = os.path.join(USERDATA_DIR, "bindings.json")
JOYSTICK_BINDINGS_PATH = os.path.join(USERDATA_DIR, "joystick_bindings.json")

SCREEN_WIDTH = 375
SCREEN_HEIGHT = 175
FPS = 60

JOYSTICK_CENTER = (75, 85)
JOYSTICK_RADIUS = 50
JOYSTICK_STICK_LENGTH = 40

BUTTON_RADIUS = 30

COLOR_BG = (0, 0, 0, 0)
COLOR_STICK = (100, 100, 100)
COLOR_STICK_KNOB = (0, 255, 0)
COLOR_BUTTON_INACTIVE = (80, 80, 80)
COLOR_BUTTON_ACTIVE = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)

BUTTON_FORMAT = 6

def get_button_labels():
    if BUTTON_FORMAT == 4:
        return ["LP", "LK", "HP", "HK"]
    return ["LP", "MP", "HP", "LK", "MK", "HK"]

def get_icon_paths():
    icon_map = {
        "LP": os.path.join("icons", "lp.png"),
        "MP": os.path.join("icons", "mp.png"),
        "HP": os.path.join("icons", "hp.png"),
        "LK": os.path.join("icons", "lk.png"),
        "MK": os.path.join("icons", "mk.png"),
        "HK": os.path.join("icons", "hk.png"),
    }
    return [icon_map[label] for label in get_button_labels()]

def get_button_positions():
    full_positions = [
        (195, 50),   # LP
        (265, 50),   # MP
        (335, 50),   # HP
        (195, 130),  # LK
        (265, 130),  # MK
        (335, 130)   # HK
    ]
    return full_positions[:len(get_button_labels())]