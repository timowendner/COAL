import numpy as np
from copy import copy

from .board import Board


def check_line(board: Board, pos: np.ndarray, offset: np.ndarray, times: int = 8, capture: int = True) -> set[tuple[int]]:
    result = set()
    pos = copy(pos)
    color = np.sign(board[pos])
    for i in range(times):
        pos += offset
        if max(pos) >= 8 or min(pos) < 0:
            return result

        cur = np.sign(board[pos])
        if cur == -color and not capture:
            return result
        if cur == -color:
            result.add(tuple(pos))
            return result
        if cur == color:
            return result
        result.add(tuple(pos))
    return result


def pawn_moves(board: Board, pos: np.ndarray) -> set[tuple[int]]:
    result = set()
    piece = board[pos]
    piece, color = abs(piece), np.sign(piece)

    move = np.array([1, 0]) * -color
    times = 2 if pos[0] in (1, 6) else 1
    result = check_line(board, pos, move, times=times, capture=False)

    x, y = pos
    for cur in ((x - color, y - 1), (x - color, y + 1)):
        if not (0 <= cur[1] < 8):
            continue
        if np.sign(board[cur]) == -color or np.all(board.en_passant == cur):
            result.add(tuple(cur))
    return result


def castling(board: Board, pos: np.ndarray) -> set[tuple[int]]:
    result = set()
    if pos[0] == 7 and board.castle_right[0] and np.all(board[7, 5:7] == 0):
        result |= {(7, 6), (7, 7)}
    if pos[0] == 7 and board.castle_right[1] and np.all(board[7, 1:4] == 0):
        result |= {(7, 0), (7, 2)}
    if pos[0] == 0 and board.castle_right[2] and np.all(board[0, 5:7] == 0):
        result |= {(0, 6), (0, 7)}
    if pos[0] == 0 and board.castle_right[3] and np.all(board[0, 1:4] == 0):
        result |= {(0, 0), (0, 2)}
    return result


def get_moves(board: Board, pos: np.ndarray) -> set[tuple[int]]:
    result = set()
    if board.active != np.sign(board[pos]):
        return result
    piece = abs(board[pos])

    line_parameters = {
        0: ([], 0),
        1: ([(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)], 1),
        2: ([(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)], 8),
        3: ([(1, 1), (1, -1), (-1, 1), (-1, -1)], 8),
        3: ([(1, 1), (1, -1), (-1, 1), (-1, -1)], 8),
        4: ([(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)], 1),
        5: ([(1, 0), (-1, 0), (0, 1), (0, -1)], 8),
    }

    if piece in line_parameters:
        moves, times = line_parameters[piece]
        for move in moves:
            result |= check_line(
                board, pos, np.array(move), times=times
            )

    if piece == 1:
        result |= castling(board, pos)
    if piece == 6:
        result |= pawn_moves(board, pos)
    return result


def get_all_attacks(board: Board) -> set[tuple[int]]:
    result = set()
    for pos, piece in np.ndenumerate(board.board):
        result |= get_moves(board, pos)
    return result
