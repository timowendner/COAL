import pygame
import sys
import pkg_resources

from .board import Board
from .render import render, Mouse
from .move import move


def gamelogic(board: Board, mouse: Mouse) -> Board:
    if mouse.action and mouse.last is not None:
        pos, to = mouse.get_pos()
        board = move(board, pos, to)
    mouse.action = False
    return board


def start():
    pygame.init()

    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    pygame.display.set_caption("coal Chess")
    image_path = pkg_resources.resource_filename(__name__, 'img/pieces.png')
    piece_img = pygame.image.load(image_path)
    mouse = Mouse(screen)
    board = Board()
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    # fen = 'rnbqkbnr/ppp2ppp/8/1B1Pp3/8/8/PPPP1PPP/RNBQK1NR b KQkq - 1 3'
    board.setup_fen(fen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_size = event.size
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.update(event.pos, True)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.update(event.pos, False)

        board = gamelogic(board, mouse)
        render(board, screen, piece_img, mouse)

        pygame.display.flip()
        pygame.time.Clock().tick(60)


def main():
    start()


if __name__ == '__main__':
    main()
