
import pygame
import numpy as np
from pygame.surface import Surface
from itertools import product

from .board import Board
from .move import get_possible_moves, get_all_attacks, is_in_check
from .utils import position_to_coordinates, coordinates_to_position


class Mouse:
    def __init__(self, screen) -> None:
        self.last = None
        self.cur = None
        self.toggle = False
        self.action = False
        self.screen = screen

    def update(self, cord: np.ndarray, toggle: bool) -> None:
        pos = coordinates_to_position(self.screen, cord)
        if max(pos) >= 8 or min(pos) < 0:
            self.toggle = toggle
            return None

        if self.toggle and not toggle and self.last is not None:  # mouse is let go
            self.action = True
        elif not self.toggle and toggle:  # mouse is clicked
            self.last = pos
        self.toggle = toggle
        self.cur = pos

    def get_pos(self) -> tuple[np.ndarray]:
        return self.last, self.cur


def get_img(piece: int, color: int, piece_img: Surface, scale: float = 0.5) -> Surface:
    x, y = 320*piece, 320*color
    img = piece_img.subsurface((x, y, 320, 320))
    size = (int(img.get_width() * scale), int(img.get_height() * scale))
    img = pygame.transform.scale(img, size)
    return img


def plot_dots(screen: Surface, pos: np.ndarray, color: tuple[int]) -> None:
    cord, step = position_to_coordinates(screen, pos)
    cord += step // 2
    pygame.draw.circle(screen, color, cord, radius=step*0.15)


def plot_tile(screen: Surface, pos: np.ndarray, color: tuple[int]) -> None:
    if len(color) < 4:
        color = (*color, 255)
    cord, step = position_to_coordinates(screen, pos)
    surface = pygame.Surface((step, step), pygame.SRCALPHA)
    surface.fill(color)
    screen.blit(surface, cord)


def plot_check(screen: Surface, pos: np.ndarray) -> None:
    cord, step = position_to_coordinates(screen, pos)
    surface = pygame.Surface((step, step), pygame.SRCALPHA)

    x, y = np.meshgrid(np.arange(step), np.arange(step))
    distance = np.sqrt((x - step // 2)**2 + (y - step // 2)**2)

    alpha_values = 255 * (1 - distance / (step / 1.8))
    alpha_values[alpha_values < 0] = 0

    surface.fill((255, 0, 0, 255))
    surface_array = pygame.surfarray.pixels_alpha(surface)
    surface_array[:, :] = alpha_values
    del surface_array

    screen.blit(surface, cord)


def render(
    board: Board,
    screen: Surface,
    piece_img: Surface,
    mouse: Mouse,
) -> None:

    screen.fill((22, 21, 18))
    color_light = (180, 136, 98)
    color_dark = (241, 217, 180)
    color_move = (107, 110, 64)
    color_last = (204, 210, 122, 150)

    for pos in product(range(8), range(8)):
        color = color_dark if sum(pos) % 2 == 0 else color_light
        plot_tile(screen, pos, color)

    if not hasattr(board, 'check'):
        board.check = is_in_check(board)
    if board.check is not None:
        plot_check(screen, board.check)

    if board.last is not None:
        for pos in board.last:
            plot_tile(screen, pos, color_last)

    for pos, piece in np.ndenumerate(board.board):
        if piece != 0:
            color = np.sign(piece)
            piece = abs(piece - color)
            cord, step = position_to_coordinates(screen, pos)
            img = get_img(piece, max(0, -color), piece_img,
                          scale=1 / (320 / step))
            screen.blit(img, cord)

    if mouse.toggle and mouse.last is not None:
        pos = mouse.last
        moves = get_possible_moves(board, pos)
        for move in moves:
            plot_dots(screen, move, color_move)
