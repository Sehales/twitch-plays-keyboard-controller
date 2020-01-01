import ctypes
from _ctypes import Structure
from ctypes import wintypes
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x57
VK_MENU = 0x12

VK_A = 0x41
VK_D = 0x44
VK_I = 0x49
VK_N = 0x4E
VK_R = 0x52
VK_S = 0x53
VK_T = 0x54
VK_U = 0x55
VK_W = 0x57
VK_Y = 0x59

VK_0 = 0x30
VK_1 = 0x31
VK_2 = 0x32
VK_3 = 0x33

VK_SHIFT = 0x10


# C struct definitions
wintypes.ULONG_PTR = wintypes.WPARAM
PUL = ctypes.POINTER(ctypes.c_ulong)


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class POINT(Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize


# Functions
def press_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def release_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def query_mouse_position():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return {"x": pt.x, "y": pt.y}


def move_mouse(direction):

    pos = query_mouse_position()
    if direction == "up":
        y = pos["y"] + 100
        x = pos["x"]
    elif direction == "right":
        y = pos["y"]
        x = pos["x"] + 100
    elif direction == "left":
        y = pos["y"]
        x = pos["x"] - 100
    else:
        y = pos["y"] - 100
        x = pos["x"]

    x = 1 + int(x * 65536./1920.)
    y = 1 + int(y * 65536./1080.)
    x = INPUT(type=INPUT_MOUSE,
              mi=MOUSEINPUT(dx=x, dy=y))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [
                ("mi", MouseInput),
                ]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def set_mouse_pos(direction):

    pos = query_mouse_position()

    print(pos)

    if direction == "up":
        y = pos["y"] - 25
        x = pos["x"]
    elif direction == "right":
        y = pos["y"]
        x = pos["x"] - 25
    elif direction == "left":
        y = pos["y"]
        x = pos["x"] + 25
    else:
        y = pos["y"] + 25
        x = pos["x"]

    x = 1 + int(x * 65536. / 1920.)
    y = 1 + int(y * 65536. / 1080.)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def press(key, press_time):
    press_key(key)
    time.sleep(press_time)
    release_key(key)


def press_w():
    press(VK_W, 0.01)


def press_a():
    press(VK_A, 4.01)


def press_s():
    press(VK_S, 0.01)


def press_d():
    press(VK_D, 4.01)


def press_fire():
    press(VK_0, 0.01)
    time.sleep(0.01)
    press(VK_0, 0.01)


def press_t():
    press(VK_T, 0.01)


def press_r():
    press(VK_R, 0.01)


def press_y():
    press(VK_Y, 0.01)


def press_i():
    press(VK_I, 0.01)


def press_u():
    press(VK_U, 0.01)


def press_shift():
    press(VK_SHIFT, 0.01)


def press_n():
    press(VK_N, 0.01)


def press_1():
    press(VK_1, 0.01)


def press_2():
    press(VK_2, 0.01)


def press_3():
    press(VK_3, 0.01)


if __name__ == "__main__":

    time.sleep(2.0)
    for i in range(1, 20):
        for j in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s"]:
            time.sleep(0.1)

            vote = j + str(i)

            c, num = vote[0], vote[1:]
            y = int(num) * 54
            x = 96 + (ord(c) - 97) * 96
            print("cord: %s %s" % (str(x), str(y)))
            set_mouse_pos("down")