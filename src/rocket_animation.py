import asyncio
import curses

from curses_tools import draw_frame, read_controls, get_frame_size


async def rocket(canvas, start_row, start_column, frames, speed=1):
    """Display animation of rocket, speed can be specified."""
    rows, columns = curses.window.getmaxyx(canvas)
    while True:
        frame = next(frames)

        start_column, start_row = update_position(canvas, columns, frame, rows, speed, start_column, start_row)

        draw_frame(canvas, start_row, start_column, text=frame)
        await asyncio.sleep(0)
        draw_frame(canvas, start_row, start_column, text=frame, negative=True)

        start_column, start_row = update_position(canvas, columns, frame, rows, speed, start_column, start_row)

        draw_frame(canvas, start_row, start_column, text=frame)
        await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, text=frame, negative=True)


def update_position(canvas, columns, frame, rows, speed, start_column, start_row):
    """Reads controls and returns new start row and column position that can be used to draw new frame"""
    frame_rows, frame_columns = get_frame_size(frame)
    rows_direction, columns_direction, _ = read_controls(canvas)
    if rows_direction:
        start_row += rows_direction * speed
        if not (0 < start_row < rows - frame_rows):
            start_row = 1 if rows_direction < 0 else rows - frame_rows
    if columns_direction:
        start_column += columns_direction * speed
        if not (0 < start_column < columns - frame_columns):
            start_column = 1 if columns_direction < 0 else columns - frame_columns - 1
    return start_column, start_row


