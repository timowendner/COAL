import pytest
import numpy as np
from itertools import product

from COAL.board import Board
from COAL.move import get_possible_moves, simulate


def get_games_count(depth: int):
    board: Board = Board().get_starting_position()
    seen = set()
    old = [board]
    for i in range(depth):
        new = []
        for board in old:
            for pos in product(range(8), range(8)):
                pos = np.array(pos)
                for to in get_possible_moves(board, pos):
                    new_board = simulate(board, pos, to)
                    if new_board not in seen:
                        seen.add(new_board)
                        new.append(new_board)
        old = new
    return len(old)


@pytest.mark.parametrize("test_input,expected", [
    (1, 20),
    (2, 400),
    (3, 8902),
    # (4, 197281),
    # (5, 4_865_609),
    # (6, 119_060_324),
    # (7, 3_195_901_860),
])
def test_game_count(test_input, expected):
    result = get_games_count(test_input)
    assert result == expected
