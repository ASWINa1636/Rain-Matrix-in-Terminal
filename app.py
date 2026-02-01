# Matrix rain effect for Linux terminal (Python 3).
# Usage: python3 matrix_rain.py
# Stop with Ctrl-C.

import curses
import random
import time
import locale
import sys
from itertools import cycle

locale.setlocale(locale.LC_ALL, '')

# Characters used in the rain. Katakana range + ASCII fallback.
ASCII = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()[]{}<>/\\|~;:,.")
CHARS =  ASCII

# Settings
TICK = 0.02           # seconds per frame (lower -> faster)
SPAWN_PROB = 0.02     # probability a column spawns a new drop on a tick
MAX_TRAIL = 20        # maximum trail length for a drop
INTENSITY_DECAY = 0.2   # how quickly trail fades (1 is faster, smaller is slower)


def run(stdscr):
    curses.curs_set(0)               # hide cursor
    stdscr.nodelay(True)            # non-blocking input
    stdscr.timeout(0)

    if curses.has_colors():
        curses.start_color()
        try:
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # normal green
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # head (bright)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # faded (use same color, render dim)
        except Exception:
            pass

    # Buffer of intensities per cell (0 = empty). We'll decrease intensity over time to create fading.
    height, width = stdscr.getmaxyx()
    intens = [[0] * width for _ in range(height)]
    chars = [[' '] * width for _ in range(height)]

    # For each column, we'll either have no active drop or an active head with current y and trail length
    # Represent drops as dict { 'y': int, 'trail': int, 'speed_skip': int }
    drops = [None] * width

    # Pre-generate characters iterator for variety
    char_cycle = cycle([random.choice(CHARS) for _ in range(1000)])

    last_resize = (height, width)

    try:
        while True:
            # Resize handling
            h, w = stdscr.getmaxyx()
            if (h, w) != last_resize:
                height, width = h, w
                intens = [[0] * width for _ in range(height)]
                chars = [[' '] * width for _ in range(height)]
                drops = [None] * width
                stdscr.clear()
                last_resize = (h, w)

            # Maybe spawn drops in some columns
            for x in range(width):
                # If no drop in column, spawn randomly
                if drops[x] is None and random.random() < SPAWN_PROB:
                    drops[x] = {
                        'y': 0,
                        'trail': random.randint(4, MAX_TRAIL),
                        'speed_skip': random.randint(0, 1)  # small variability in speed
                    }

            # Move drops and update buffer
            for x in range(width):
                d = drops[x]
                if d is None:
                    continue

                # Each tick, head moves down
                d['y'] += 1

                # Put a bright head at (y, x) if within screen
                y = d['y']
                if 0 <= y < height:
                    chars[y][x] = next(char_cycle)
                    intens[y][x] = d['trail'] + 2  # head intensity a bit higher

                # Put trailing characters above head
                for t in range(1, d['trail'] + 1):
                    ty = y - t
                    if 0 <= ty < height:
                        # choose char occasionally so trail looks varied
                        if random.random() < 0.3:
                            chars[ty][x] = next(char_cycle)
                        intens[ty][x] = max(intens[ty][x], d['trail'] - t + 1)

                # If head moved past screen + trail, remove drop
                if y - d['trail'] > height:
                    drops[x] = None

            # Decay intensities and render
            for y in range(height):
                row = ''.join(chars[y])
                # render column by column to apply attributes per cell
                for x in range(width):
                    if intens[y][x] > 0:
                        ch = chars[y][x]
                        intensity = intens[y][x]
                        # choose attributes based on intensity
                        if intensity >= (MAX_TRAIL // 2) + 2:
                            attr = curses.color_pair(2) | curses.A_BOLD  # head/bright
                        elif intensity >= 3:
                            attr = curses.color_pair(1)                    # normal green
                        else:
                            # dim / faded
                            # curses.A_DIM might not be supported everywhere; try it
                            attr = curses.color_pair(3)
                            try:
                                attr |= curses.A_DIM
                            except Exception:
                                pass

                        try:
                            stdscr.addstr(y, x, ch, attr)
                        except curses.error:
                            # writing to bottom-right corner may throw an error; ignore
                            pass

                        # decay
                        intens[y][x] = max(0, intens[y][x] - INTENSITY_DECAY)
                        if intens[y][x] == 0:
                            chars[y][x] = ' '
                    else:
                        # clear cell if empty
                        try:
                            stdscr.addstr(y, x, ' ')
                        except curses.error:
                            pass

            stdscr.refresh()

            # input check to allow quit with 'q'
            try:
                c = stdscr.getch()
                if c != -1:
                    if c in (ord('q'), ord('Q')):
                        break
            except Exception:
                pass

            time.sleep(TICK)

    except KeyboardInterrupt:
        # graceful exit on Ctrl-C
        pass
    finally:
        curses.curs_set(1)
        stdscr.nodelay(False)


def main():
    # Run curses wrapper (handles cleanup)
    try:
        curses.wrapper(run)
    except Exception as e:
        print("Error running Matrix rain:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()