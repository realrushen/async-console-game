#!/usr/bin/env python3

import curses
import random
import time
from itertools import cycle
from pathlib import Path

from fire_animation import fire
from rocket_animation import rocket
from star_animation import blink

TIC_TIMEOUT = 0.1


def load_frame(path: Path):
    path.resolve()
    with path.open(mode='r', encoding='utf-8') as f:
        return f.read()


def draw(canvas):
    rocket_frame_1 = load_frame(Path('./frames/rocket_frame_1.txt'))
    rocket_frame_2 = load_frame(Path('./frames/rocket_frame_2.txt'))
    rocket_frames = cycle([rocket_frame_1, rocket_frame_2])

    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(1)
    rows, columns = curses.window.getmaxyx(canvas)
    canvas.refresh()
    coroutines = [
        blink(canvas,
              row=random.randint(1, rows - 1),
              column=random.randint(1, columns - 1),
              symbol=random.choice('+*.:'),
              delay=random.randint(1, 10)
              ) for _ in range(100)
    ]
    coroutines.append(fire(canvas, 15, 15, rows_speed=-1))
    coroutines.append(
        rocket(
            canvas,
            start_row=int(rows / 2),
            start_column=int(columns / 2),
            frames=rocket_frames,
            speed=1
        )
    )
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
