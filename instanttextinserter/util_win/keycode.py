# encoding: shift-jis

# 無効なコードを便宜上独自に定義.
INVALID = 0

# mouse buttons
LBUTTON = 1
RBUTTON = 2
MBUTTON = 4
XBUTTON1 = 5 #拡張1
XBUTTON2 = 6 #拡張2

# modifiers
SHIFT = 16
CONTROL = 17
CTRL = CONTROL
ALT = 18
LSHIFT = 160
RSHIFT = 161
LCONTROL = 162
RCONTROL = 163
LCTRL = LCONTROL
RCTRL = RCONTROL
LALT = 164
RALT = 165
LWIN = 91
RWIN = 92
WIN = LWIN # 左Winキーが一般的だから.

# misc
BACKSPACE = 8
BS = BACKSPACE
TAB = 9
RETURN = 13
ENTER = RETURN
PAUSE = 19
CAPSLOCK = 20
ESCAPE = 27
ESC = ESCAPE
CONVERT = 28
NONCONVERT = 29
SPACE = 32
PAGEUP = 33
PAGEDOWN = 34
END = 35
HOME = 36
LEFT = 37
UP = 38
RIGHT = 39
DOWN = 40
PRINTSCREEN = 44
INSERT = 45
DELETE = 46
ADD = 107 # テンキー +
SUBTRACT = 109
SUB = SUBTRACT
MULTIPLY = 106
MUL = MULTIPLY
DEVIDE = 111
DEV = DEVIDE
NUMLOCK = 144
SCROLL = 145

# alphabet
A = 65
B = 66
C = 67
D = 68
E = 69
F = 70
G = 71
H = 72
I = 73
J = 74
K = 75
L = 76
M = 77
N = 78
O = 79
P = 80
Q = 81
R = 82
S = 83
T = 84
U = 85
V = 86
W = 87
X = 88
Y = 89
Z = 90

# Function keys
F1 = 112
F2 = 113
F3 = 114
F4 = 115
F5 = 116
F6 = 117
F7 = 118
F8 = 119
F9 = 120
F10 = 121
F11 = 122
F12 = 123
F13 = 124
F14 = 125
F15 = 126
F16 = 127
F17 = 128
F18 = 129
F19 = 130
F20 = 131
F21 = 132
F22 = 133
F23 = 134
F24 = 135

# Mainkeyboard numbers
M0 = 48
M1 = 49
M2 = 50
M3 = 51
M4 = 52
M5 = 53
M6 = 54
M7 = 55
M8 = 56
M9 = 57
N0 = 96

# Numpad numbers
N1 = 97
N2 = 98
N3 = 99
N4 = 100
N5 = 101
N6 = 102
N7 = 103
N8 = 104
N9 = 105

VK_MAX = 256 # キーコード数

# 文字列からキーコードに変換する
def chara2keycode(chara):
    d = {
        "a":A,
        "b":B,
        "c":C,
        "d":D,
        "e":E,
        "f":F,
        "g":G,
        "h":H,
        "i":I,
        "j":J,
        "k":K,
        "l":L,
        "m":M,
        "n":N,
        "o":O,
        "p":P,
        "q":Q,
        "r":R,
        "s":S,
        "t":T,
        "u":U,
        "v":V,
        "w":W,
        "x":X,
        "y":Y,
        "z":Z,
        "backspace":BACKSPACE,
        "bs":BACKSPACE,
        "tab":TAB,
        "return":RETURN,
        "enter":RETURN,
        "pause":PAUSE,
        "pausebreak":PAUSE,
        "capslock":CAPSLOCK,
        "escape":ESCAPE,
        "esc":ESCAPE,
        "convert":CONVERT,
        "nonconvert":NONCONVERT,
        "space":SPACE,
        "pageup":PAGEUP,
        "pagedown":PAGEDOWN,
        "end":END,
        "home":HOME,
        "left":LEFT,
        "right":RIGHT,
        "up":UP,
        "down":DOWN,
        "printscreen":PRINTSCREEN,
        "insert":INSERT,
        "delete":DELETE,
        "0":M0,
        "m0":M0,
        "n0":N0,
        "1":M1,
        "m1":M1,
        "n1":N1,
        "2":M2,
        "m2":M2,
        "n2":N2,
        "3":M3,
        "m3":M3,
        "n3":N3,
        "4":M4,
        "m4":M4,
        "n4":N4,
        "5":M5,
        "m5":M5,
        "n5":N5,
        "6":M6,
        "m6":M6,
        "n6":N6,
        "7":M7,
        "m7":M7,
        "n7":N7,
        "8":M8,
        "m8":M8,
        "n8":N8,
        "9":M9,
        "m9":M9,
        "n9":N9,
        "f1":F1,
        "f2":F2,
        "f3":F3,
        "f4":F4,
        "f5":F5,
        "f6":F6,
        "f7":F7,
        "f8":F8,
        "f9":F9,
        "f10":F10,
        "f11":F11,
        "f12":F12,
        "f13":F13,
        "f14":F14,
        "f15":F15,
        "f16":F16,
        "f17":F17,
        "f18":F18,
        "f19":F19,
        "f20":F20,
        "f21":F21,
        "f22":F22,
        "f23":F23,
        "f24":F24,
    }
    ret = INVALID
    try:
        ret = d[chara.lower()]
    except KeyError:
        pass
    return ret
