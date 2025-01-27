from blinka_displayio_pygamedisplay import PyGameDisplay
display = PyGameDisplay(width=64, height=32, hw_accel=False, scale=16)

# from mcu import get, post
from pc import get, post

import displayio
from bitmaptools import arrayblit
from time import sleep
#displayio.release_displays()

palette = displayio.Palette(8)
palette[0] = 0x000000
palette[1] = 0xFF0000
palette[2] = 0x00FF00
palette[3] = 0xFFFF00
palette[4] = 0x0000FF
palette[5] = 0xFF00FF
palette[6] = 0x00FFFF
palette[7] = 0xFFFFFF

_group = displayio.Group()
display.root_group = _group
matrix = displayio.Bitmap(64, 32, 8)
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

def draw_text (string, color, *, x=0, y=0, align=None, truncate=True):
    """
    Wrapper for draw_ascii and draw_zh
    align: l=left, m=middle, r=right
    truncate: truncate string if it's too long
    """
    if all(ord(i) >= 0x20 and ord(i) < 0x7f for i in string):
        mode = "ascii"
    elif all(ord(i) >= 0x3200 and ord(i) < 0xa000 for i in string):
        mode = "zh"
    else:
        raise ValueError("Invalid string " + string)
    if truncate:
        string = string[:64 // (16 if mode == "zh" else 6)]
    if align == "l":
        x = 0
    elif align == "m":
        x = (64 - len(string) * (16 if mode == "zh" else 6)) // 2
    elif align == "r":
        x = 64 - len(string) * (16 if mode == "zh" else 6)
    else:
        string = string[:(64 - x) // (16 if mode == "zh" else 6)]
    if mode == "ascii":
        draw_ascii(string, x, y, color)
    else:
        draw_zh(string, x, y, color)

# start of program functions

cf = {
    "station": "HGH",
    "num_trains": 3,
    "wait": 4,
    "wait_small": 0.8,
    "wait_map": 8,
    "only_emu": False,
    "repeat_info": 2,
    "bureau": {
        'A': '新广铁',
        'B': '哈局',
        'C': '呼局',
        'D': '锦局',
        'E': '新成局',
        'F': '郑局',
        'G': '南局',
        'H': '上局',
        'I': '济局',
        'J': '兰局',
        'K': '济局',
        'L': '吉局',
        'M': '昆局',
        'N': '武局',
        'O': '青藏铁',
        'P': '京局',
        'Q': '广铁',
        'R': '乌局',
        'S': '福局',
        'T': '沈局',
        'U': '新上局',
        'V': '太局',
        'W': '成局',
        'X': '境外',
        'Y': '西局',
        'Z': '宁局'
    }
}
cache = {}

def fetch_data():
    global cache, cf, matrix
    datef, timef = None, None
    def get_time():
        nonlocal datef, timef
        tz = get("https://timeapi.io/api/time/current/zone?timeZone=Asia%2FShanghai")
        datef = tz["dateTime"].split("T")[0] # YYYY-MM-DD
        timef = tz["time"] # HH:MM

    print("\n-----\nRestart\n-----\n")
    matrix.fill(0)
    draw_text(cf["station"], 1, y=0, align="l") # e.g. SHH
    get_time()
    if cache.get("date") != datef:
        cache = {
            "date": datef,
            "dandang": {},
            "shape": {}
        }
    draw_text(datef, 6, y=8, align="m") # e.g. 1234-01-23
    draw_text(timef, 6, y=0, align="r") # e.g. 12:34
    date = datef.replace("-", "") # YYYYMMDD
    time = int(timef.replace(":", "")) # HHMM
    bigscreen = post(f"https://mobile.12306.cn/wxxcx/wechat/bigScreen/queryTrainByStation?train_start_date={date}&train_station_code={cf['station']}")
    bigscreen = [i for i in bigscreen["data"] if all(j in "0123456789" for j in i["arrive_time"].replace(":", ""))] # filter out trains which start at the station
    if cf["only_emu"]:
        bigscreen = [i for i in bigscreen if "train_style" in i]
    bigscreen = sorted(bigscreen, key=lambda x: (int(x["arrive_time"].replace(":", "")) - time) % 2400)[:cf["num_trains"]] # simple sort by time
    stationname = bigscreen[0]["station_name"]
    draw_text(stationname, 1, y=16, align="m") # e.g. 上海
    sleep(cf["wait"])
    for i in bigscreen:
        print(i["station_train_code"] + " " + i["train_no"])

        for j in range(cf["repeat_info"] + 1):
            matrix.fill(0)
            draw_text(i["station_train_code"], 1, y=0, align="l") # e.g. G1234
            draw_text(i["start_station_telecode"], 3, y=16, align="l") # e.g. GZQ
            draw_text(cf["station"], 5, y=16, align="m") # e.g. SHH
            draw_text(i["end_station_telecode"], 3, y=16, align="r") # e.g. BJP
            get_time()
            draw_text(timef, 1, y=24, align="l") # e.g. 12:34
            draw_text(i["arrive_time"], 2, y=24, align="r") # e.g. 12:56
            if "train_style" in i:
                draw_text(i["train_style"].split("_")[0], 6, y=8, align="m") # e.g. CR400BF-BS
                if cache["dandang"].get(i["station_train_code"]) is None:
                    dandang = get(f"https://mobile.12306.cn/wxxcx/openplatform-inner/miniprogram/wifiapps/appFrontEnd/v2/lounge/open-smooth-common/trainStyleBatch/getCarDetail?carCode=&trainCode={i["station_train_code"]}&runningDay={date}&reqType=form")
                    if "data" in dandang["content"]:
                        cache["dandang"][i["station_train_code"]] = dandang["content"]["data"]
                    else:
                        cache["dandang"][i["station_train_code"]] = False # no data
                dandang = cache["dandang"].get(i["station_train_code"])
                if dandang:
                    arrayblit(matrix, bytes(64 * 8), 0, 8, 64, 16) # clear line
                    draw_text(dandang["carCode"][:-5], 6, y=8, align="m") # e.g. CR400BF-BS
                    draw_text(dandang["carCode"][-4:], 6, y=0, align="r") # e.g. 5033

            sleep(cf["wait"])
            if j == cf["repeat_info"]:
                break

            arrayblit(matrix, bytes(128 * 8), 0, 16, 64, 32) # clear two lines
            draw_text(cf["bureau"][i["bureau_code"]], 2, y=16, align="m") # e.g. 新广铁
            sleep(cf["wait_small"])
            arrayblit(matrix, bytes(128 * 8), 0, 16, 64, 32)
            draw_text("由", 3, y=16, align="m")
            sleep(cf["wait_small"])
            arrayblit(matrix, bytes(128 * 8), 0, 16, 64, 32)
            draw_text(i["start_station_name"], 5, y=16, align="m")
            sleep(cf["wait_small"])
            arrayblit(matrix, bytes(128 * 8), 0, 16, 64, 32)
            draw_text("开往", 3, y=16, align="m")
            sleep(cf["wait_small"])
            arrayblit(matrix, bytes(128 * 8), 0, 16, 64, 32)
            draw_text(i["end_station_name"], 5, y=16, align="m")
            sleep(cf["wait_small"])
            arrayblit(matrix, bytes(128 * 8), 0, 16, 64, 32)
            draw_text("的", 3, y=16, align="m")
            sleep(cf["wait_small"])
            arrayblit(matrix, bytes(128 * 8), 0, 16, 64, 32)
            draw_text(i["train_type_name"], 2, y=16, align="m")
            sleep(cf["wait_small"])

        if cache["shape"].get(i["station_train_code"]) is None:
            shape = post(f"https://mobile.12306.cn/wxxcx/wechat/main/getTrainMapLine?version=v2&trainNo={i["train_no"]}")
            if "data" in shape and len(shape["data"]) > 0:
                cache["shape"][i["station_train_code"]] = shape["data"]
            else:
                cache["shape"][i["station_train_code"]] = False # no data
                print("No shape data found for " + i["train_no"])
        shape = cache["shape"].get(i["station_train_code"])
        if shape:
            matrix.fill(0)
            draw_text(i["station_train_code"], 1, x=34, y=0) # e.g. G1234
            draw_text(i["start_station_telecode"], 3, x=34, y=8) # e.g. BJP
            draw_text(cf["station"], 2, x=34, y=16) # e.g. SHH
            draw_text(i["end_station_telecode"], 6, x=34, y=24) # e.g. GZQ
            stopseg = [i for i in shape.keys() if i.startswith(stationname + "-")]
            if len(stopseg) == 0:
                stopseg = [i for i in shape.keys() if i.endswith("-" + stationname)] # end station
                if len(stopseg) == 0:
                    raise ValueError("No stop segment found for station " + stationname)
                elif len(stopseg) > 1:
                    raise ValueError(f"Multiple stop segments found for station {stationname}: {stopseg}")
                else:
                    stopseg = shape[stopseg[0]]["line"][-1] # station coordinates
            elif len(stopseg) > 1:
                raise ValueError(f"Multiple stop segments found for station {stationname}: {stopseg}")
            else:
                stopseg = shape[stopseg[0]]["line"][0] # station coordinates
            shape = sorted(list (shape.values()), key=lambda x: x["index"])
            shape = [c for i in shape for c in i["line"]]
            minx, miny = min(i[0] for i in shape), min(i[1] for i in shape)
            maxx, maxy = max(i[0] for i in shape), max(i[1] for i in shape)
            maxsize = max(maxx - minx, maxy - miny)
            scale = maxsize / (32 - 1)
            minx_scale = minx - scale / 2 # center
            miny_scale = miny - scale / 2 # center
            x_span, y_span = int((maxx - minx_scale) / scale), int((maxy - miny_scale) / scale)
            if x_span < 32:
                x_delta = (32 - x_span) // 2 # in pixels
            elif x_span > 32:
                raise ValueError(f"X span {x_span} too large")
            if y_span < 32:
                y_delta = (32 - y_span) // 2 # in pixels
            elif y_span > 32:
                raise ValueError(f"Y span {y_span} too large")

            def draw_pt(pt, color=1):
                nonlocal x_delta, y_delta
                x = int((pt[0] - minx_scale) / scale) + x_delta
                y = int((pt[1] - miny_scale) / scale) + y_delta
                if x >= 0 and x < 32 and y >= 0 and y < 32:
                    matrix[x, 31 - y] = color
                else:
                    print(f"Point ({x}, {y}) out of bounds")
            for j in shape:
                draw_pt(j)
            draw_pt(shape[0], 3)  # start station
            draw_pt(shape[-1], 6) # end station
            draw_pt(stopseg, 2)   # stop station
            sleep(cf["wait_map"])
        
    for i in ("dandang", "shape"):
        for j in list(cache[i].keys()):
            if j not in (k["station_train_code"] for k in bigscreen):
                del cache[i][j] # free up unused train data
                print(f"Cleared {i} cache for {j}")

while True:
    try:
        fetch_data()
    except Exception as e:
        print(e)
    else:
        pass # sinput ("Press Enter to continue...")