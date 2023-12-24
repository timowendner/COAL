import numpy as np
from copy import copy

from .utils import position_to_algebraic, algebraic_to_position


class Board:
    def __init__(self, state: dict = None) -> None:
        if state is not None:
            for name, value in state.items():
                setattr(self, name, copy(value))
        else:
            self.clear()

    def clear(self) -> None:
        if hasattr(self, 'check'):
            delattr(self, 'check')
        self.board = np.zeros((8, 8), dtype=int)
        self.active = 1
        self.castle_right = np.ones(4, dtype=bool)
        self.en_passant = None
        self.halfmove = 0
        self.fullmove = 1
        self.king_position = [None, None]

    def __repr__(self) -> str:
        return str(self.board)

    def __getitem__(self, key):
        if isinstance(key, tuple) or isinstance(key, np.ndarray):
            return self.board[*key]
        if isinstance(key, int):
            return self.board[key]
        raise AttributeError('Unknown Key')

    def __setitem__(self, key, value):
        if isinstance(key, tuple) or isinstance(key, np.ndarray):
            self.board[*key] = value
        elif isinstance(key, int):
            self.board[key] = value
        else:
            raise AttributeError('Unknown Key')

    def setup_fen(self, fen: str) -> None:
        self.clear()
        pieces, active, castle, en_passant, halfmove, fullmove = fen.strip().split(' ')

        self.active = 1 if active == 'w' else -1
        self.castle_right = np.array([
            'K' in castle,
            'Q' in castle,
            'k' in castle,
            'q' in castle,
        ])
        self.en_passant = algebraic_to_position(en_passant)
        self.halfmove = int(halfmove)
        self.fullmove = int(fullmove)

        mapping = {
            'k': 1,
            'q': 2,
            'b': 3,
            'n': 4,
            'r': 5,
            'p': 6,
        }

        for row, row_string in enumerate(pieces.split('/')):
            col = 0
            for piece_string in row_string:
                if piece_string.isnumeric():
                    col += int(piece_string)
                else:
                    color = 1 if piece_string.isupper() else -1
                    piece = mapping[piece_string.lower()]
                    self.board[row, col] = piece * color
                    if piece == 1:
                        self.king_position[1 - max(0, color)] = (row, col)
                    col += 1
