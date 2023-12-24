import numpy as np

from .board import Board
from .pieces import get_moves, get_all_attacks


def simulate(board: Board, pos: np.ndarray, to: np.ndarray) -> Board:
    board = Board(vars(board))
    piece = board[pos]
    piece, color = abs(piece), np.sign(piece)

    if board.active == -1:
        board.fullmove += 1
    board.halfmove += 1
    if piece == 6 or board[to] != 0:
        board.halfmove = 0
    board.active *= -1

    board[pos] = 0
    board[to] = piece * color

    # track king
    if piece == 1:
        board.king_position[1 - max(0, color)] = tuple(to)

    # pawns (en passant, doublemove, promotion)
    if piece == 6 and np.all(to == board.en_passant):
        board[pos[0], to[1]] = 0

    board.en_passant = None
    if piece == 6 and np.max(np.abs(pos - to)) > 1:
        board.en_passant = pos - (pos - to) // 2

    if piece == 6 and to[0] in (0, 7):
        board[to] = 2 * color

    # castle right
    board.castle_right &= ~np.array([
        np.all(pos == (7, 4)) or np.all(pos == (7, 7)),
        np.all(pos == (7, 4)) or np.all(pos == (7, 0)),
        np.all(pos == (0, 4)) or np.all(pos == (0, 7)),
        np.all(pos == (0, 4)) or np.all(pos == (0, 0))
    ])

    # castling
    if piece == 1 and np.max(np.abs(pos - to)) > 1:
        if to[1] < pos[1]:
            board[pos[0], 0:5] = 0
            board[pos[0], 2] = 1 * color
            board[pos[0], 3] = 5 * color
            board.king_position[max(0, board.active)] = (pos[0], 2)
        else:
            board[pos[0], 4:8] = 0
            board[pos[0], 6] = 1 * color
            board[pos[0], 5] = 5 * color
            board.king_position[max(0, board.active)] = (pos[0], 6)
    return board


def is_in_check(board: Board) -> np.ndarray:
    board.active *= -1
    attacks = get_all_attacks(board)
    king = board.king_position[max(0, board.active)]
    board.active *= -1
    return king if king in attacks else None


def move(board: Board, pos: np.ndarray, to: np.ndarray) -> Board:
    if max(pos) >= 8 or min(pos) < 0 or max(to) >= 8 or min(to) < 0:
        return board
    if pos is None or tuple(to) not in get_possible_moves(board, pos):
        return board

    board = simulate(board, pos, to)
    board.check = is_in_check(board)
    board.last = (pos, to)
    return board


def get_possible_moves(board: Board, pos: np.ndarray) -> set[tuple[int]]:
    result = set()
    piece = abs(board[pos])
    candidates = get_moves(board, pos)
    for to in candidates:
        new_board = simulate(board, pos, to)
        attacks = get_all_attacks(new_board)
        king = new_board.king_position[max(0, new_board.active)]
        if piece == 1 and np.max(np.abs(pos - to)) > 1:
            direction = np.sign(pos[1] - to[1])
            if (pos[0], pos[1] - direction) in attacks or board.check is not None:
                continue
        if king not in attacks:
            result.add(to)
    return result
