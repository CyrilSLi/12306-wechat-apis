import sys
if (len (sys.argv) != 3):
    print ("Usage: python3 process-unifont.py <input> <output>")
    sys.exit (1)

with open (sys.argv [1], "r") as f:
    l = f.read().splitlines()

# code points 0000 to 31FF and A000 to FFFF are stripped to optimize for Chinese characters
arr = bytearray (32 * (0xa000 - 0x3200))
for i in l:
    if i[4] == ":":
        index = int (i [ : 4], 16) - 0x3200
        arr [index * 32 : (index + 1) * 32] = bytes.fromhex (i [5 : ])

with open (sys.argv [2], "wb") as f:
    f.write (arr)