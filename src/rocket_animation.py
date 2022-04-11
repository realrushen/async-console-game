import asyncio
import curses

from curses_tools import draw_frame, read_controls, get_frame_size


async def rocket(canvas, start_row, start_column, frames, speed=1):
    """Display animation of gun shot, direction and speed can be specified."""
    rows, columns = curses.window.getmaxyx(canvas)
    while True:
        frame = next(frames)
        frame_rows, frame_columns = get_frame_size(frame)
        rows_direction, columns_direction, _ = read_controls(canvas)
        if rows_direction:
            start_row += rows_direction * speed

            if not (0 < start_row < rows - frame_rows):
                start_row -= rows_direction * speed

        if columns_direction:
            start_column += columns_direction * speed
            if not (0 < start_column < columns - frame_columns):
                start_column -= columns_direction * speed
        draw_frame(canvas, start_row, start_column, text=frame)
        await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, text=frame, negative=True)
