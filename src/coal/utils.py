import numpy as np


def position_to_algebraic(pos: np.ndarray) -> str:
    x, y = pos
    return chr(y+97) + str(7 - x)


def algebraic_to_position(alg: str) -> np.ndarray:
    if alg == '-':
        return None
    col, row = alg
    col = ord(col) - 97
    row = 8 - int(row)
    return np.array([row, col])


def calculate_sizes(screen_size: tuple[int]) -> tuple[int, int, np.ndarray]:
    size = min(min(screen_size), 1280)
    size = size - size % 8
    step = size // 8
    offset = (np.array(screen_size) - size) // 2
    return size, step, offset


def coordinates_to_position(cord: tuple[int], screen_size: tuple[int]):
    size, step, offset = calculate_sizes(screen_size)
    pos = (np.array(cord) - offset) // step
    return pos[::-1]


def position_to_coordinates(pos: np.ndarray, screen_size: tuple[int]) -> tuple[np.ndarray, int]:
    size, step, offset = calculate_sizes(screen_size)
    cord = np.array(pos[::-1])*step + offset
    return cord, step
