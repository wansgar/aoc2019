import sys
from itertools import chain
import math
from math import atan2

comets = [list(line.strip()) for line in sys.stdin.readlines()]
height = len(comets)
width = len(comets[0])

def on_board(r, c, board):
    if r >= len(board) or c >= len(board[0]) or r < 0 or c < 0:
        return False
    return True

def findcomets(orir, oric, r, c, dr, dc, comets, board, detected):
    r += dr
    c += dc
    if not on_board(r, c, comets):
        return
    if comets[r][c] == "#" and not detected[r][c]:
        detected[r][c] = True
        return
    findcomets(orir, oric, r, c, dr, dc, comets, board, detected)

def simpdir(direc):
    dx, dy = direc
    gcd = math.gcd(dx, dy)
    if (dx, dy) == (0, 0):
        return (0,0)
    elif gcd == 1:
        return direc
    else:
        return (dx // gcd, dy // gcd)

def angle(r, c):
    return - atan2(c, r) - math.pi

def outnum(r, c):
    return c*100 + r

def blast_comet(r, c, comets):
    comets[r][c] = "."

def detected_comets(r, c, comets):
    height = len(comets)
    width = len(comets[0])
    handleddirs = []
    detected = [[False for col in range(width)] for row in range(height)]
    for r2 in range(height):
        for c2 in range(width):
            direc = simpdir((r2-r, c2-c))
            if direc in handleddirs or direc == (0,0):
                continue
            handleddirs.append(direc)
            findcomets(r, c, r, c, direc[0], direc[1], comets, board, detected)
    return detected

board = [[0 for c in range(width)] for r in range(height)]
# find optimal comet
for r in range(height):
    for c in range(width):
        if comets[r][c] != "#":
            continue
        detected = detected_comets(r, c, comets)
        count = list(chain(*detected)).count(True)
        board[r][c] = count

# find comet with max comets in direct line of sight
maxx = -1
maxy = -1
maxval = -1
for r in range(height):
    for c in range(width):
        val = board[r][c]
        if val > maxval:
            maxval = val
            maxx = r
            maxy = c

r, c = (maxx, maxy) # optimal comet is now laser headquarters
print("laser at (%d, %d)" % (c, r))

remaining = 200
while True:
    # find comets in direct line of sight => detected
    detected = detected_comets(r, c, comets)
    angles = [(row, col, angle(row-r, col-c)) for col in range(width) for row in range(height) if detected[row][col]]
    angles.sort(key=lambda tup:tup[2])
    if len(angles) >= remaining:
        tup = angles[remaining-1]
        print("200th: %d" % outnum(tup[0], tup[1]))
        break
    else:
        poses = [(tup[0], tup[1]) for tup in angles]
        for cometx, comety in poses:
            blast_comet(cometx, comety, comets)
            remaining -= 1
