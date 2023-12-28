import numpy as np
from pygame import Surface


def position_to_algebraic(pos: np.ndarray) -> str:
    if pos is None:
        return '-'
    x, y = pos
    return chr(y+97) + str(7 - x)


def algebraic_to_position(alg: str) -> np.ndarray:
    if alg == '-':
        return None
    col, row = alg
    col = ord(col) - 97
    row = 8 - int(row)
    return np.array([row, col])


def calculate_sizes(screen: Surface) -> tuple[int, int, np.ndarray]:
    size = min(min(screen.get_size()), 1280)
    size = size - size % 8
    step = size // 8
    offset = (np.array(screen.get_size()) - size) // 2
    return size, step, offset


def coordinates_to_position(screen: Surface, cord: tuple[int]):
    size, step, offset = calculate_sizes(screen)
    pos = (np.array(cord) - offset) // step
    return pos[::-1]


def position_to_coordinates(screen: Surface, pos: np.ndarray) -> tuple[np.ndarray, int]:
    size, step, offset = calculate_sizes(screen)
    cord = np.array(pos[::-1])*step + offset
    return cord, step
