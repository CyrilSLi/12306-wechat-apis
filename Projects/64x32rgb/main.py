from blinka_displayio_pygamedisplay import PyGameDisplay
display = PyGameDisplay(width=64, height=32, hw_accel=False, scale=16)

# from mcu import get, post
from pc import get, post

import displayio
from bitmaptools import arrayblit
#displayio.release_displays()

palette = displayio.Palette(8)
palette[0] = 0x000000
palette[1] = 0xFF0000
palette[2] = 0x00FF00
palette[3] = 0x0000FF
palette[4] = 0xFFFF00
palette[5] = 0xFF00FF
palette[6] = 0x00FFFF
palette[7] = 0xFFFFFF

_group = displayio.Group()
display.root_group = _group
matrix = displayio.Bitmap(64, 32, 3)
_tilegrid = displayio.TileGrid(matrix, pixel_shader=palette)
_group.append(_tilegrid)

with open("zh.bin", "rb") as f:
    zh_arr = f.read()
with open("ascii.bin", "rb") as f:
    ascii_arr = f.read()

def draw_zh(string, x, y, color):
    """
    Draws 16x16 Chinese characters from GNU Unifont
    """
    global matrix, zh_arr
    if any(ord(i) < 0x3200 or ord(i) >= 0xa000 for i in string):
        raise ValueError("Only Chinese characters are supported")
    for j, i in enumerate(string):
        arr_index = (ord(i) - 0x3200) * 32
        # convert bit array to colored bytes
        char_arr = bytes (color if (c & (128 >> b)) else 0 for c in zh_arr[arr_index: arr_index + 32] for b in range(8))
        arrayblit(matrix, char_arr, x + j * 16, y, x + (j + 1) * 16, y + 16)

def draw_ascii(string, x, y, color):
    """
    Draws 8x6 ASCII characters from https://web.archive.org/web/20160715002102/https://bitbucket.org/hudson/model100/src/tip/font.c?fileviewer=file-view-default
    """
    global matrix, ascii_arr
    if any(ord(i) < 0x20 or ord(i) >= 0x7f for i in string):
        raise ValueError("Only ASCII printable characters are supported")
    for j, i in enumerate(string):
        arr_index = (ord(i) - 0x20) * 5
        # convert bit array to colored bytes
        char_arr = bytes (color if (c & (128 >> b)) else 0 for c in ascii_arr[arr_index: arr_index + 5] for b in range(8))
        arrayblit(matrix, char_arr, x + j * 6, y, x + j * 6 + 5, y + 8)

def draw_text (string, color, *, x=0, y=0, align=None):
    """
    Wrapper for draw_ascii and draw_zh
    align: l=left, m=middle, r=right
    """
    if all(ord(i) >= 0x20 and ord(i) < 0x7f for i in string):
        mode = "ascii"
    elif all(ord(i) >= 0x3200 and ord(i) < 0xa000 for i in string):
        mode = "zh"
    else:
        raise ValueError("Invalid string " + string)
    if align == "l":
        x = 0
    elif align == "m":
        x = (64 - len(string) * (16 if mode == "zh" else 6)) // 2
    elif align == "r":
        x = 64 - len(string) * (16 if mode == "zh" else 6)
    else:
        raise ValueError("Invalid align mode " + align)
    if mode == "ascii":
        draw_ascii(string, x, y, color)
    else:
        draw_zh(string, x, y, color)

# start of program functions

draw_text("1234567890", 1, y=0, align="m")
draw_ascii("Hack", 0, 8, 2)
draw_ascii("Club", 24, 8, 3)
draw_ascii("<3", 52, 8, 4)
draw_zh("说的道理", 0, 16, 5)

while True:
    if display.check_quit():
        break