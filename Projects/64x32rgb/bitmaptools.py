# polyfill for bitmaptools CircuitPython library

def arrayblit(bitmap, data, x1=0, y1=0, x2=-1, y2=-1):
    x2 = bitmap.width if x2 == -1 else x2
    y2 = bitmap.height if y2 == -1 else y2
    for i, y in enumerate(range(y1, y2)):
        for j, x in enumerate(range(x1, x2)):
            bitmap[x, y] = data[i * (x2 - x1) + j]