import pygame
import time
from pygame import mixer
import jarvis
from board import Board

WIDTH, HEIGHT = 900, 600

WINDOW = pygame.display.set_mode( (WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRID_SIZE = 30
GAME_OVER = 0
GAME_GOING = 1
state = GAME_GOING

ROWS = 20
COLUMNS = 30

HUMAN = 1
JARVIS = 2

mixer.init()
win_sound = pygame.mixer.music.load("Win.mp3")
sound = mixer.Sound("Wrong.mp3")


# Set up the board
board = Board(COLUMNS, ROWS)


# Set up Pygame
pygame.init()

# Set up the font
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 90)


def play_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    time.sleep(4)
    pygame.mixer.music.stop()


def draw(won):
    WINDOW.fill(WHITE)

    for vertical_line in range(GRID_SIZE, WIDTH, GRID_SIZE):
        pygame.draw.rect(WINDOW, BLACK, (vertical_line, 0, 2, HEIGHT))

    for horizontal_line in range(GRID_SIZE, HEIGHT, GRID_SIZE):
        pygame.draw.rect(WINDOW, BLACK, (0, horizontal_line, WIDTH, 2))

    label_x = font.render("x", 1, BLACK)
    label_o = font.render("o", 1, RED)

    if won != 0:
        label_winner = font2.render(f"Player {won} is the winner!", 1, RED)
        text_rect = label_winner.get_rect(center = (450, 500))
        WINDOW.fill(WHITE, text_rect)
        WINDOW.blit(label_winner, text_rect)

    for i, j in board.cells():
        if board.get(i, j) == 1:
            WINDOW.blit(label_x, (j*GRID_SIZE+8, i*GRID_SIZE+2))
        elif board.get(i, j) == 2:
            WINDOW.blit(label_o, (j*GRID_SIZE+8, i*GRID_SIZE+2))

    pygame.display.update()

def winner(board: Board) -> int:
    for i, j in board.cells():
        if board.get(i, j) == HUMAN and board.connect(i, j, HUMAN):
            return HUMAN
        if board.get(i, j) == JARVIS and board.connect(i, j, JARVIS):
            return JARVIS

    return 0


def main():
    clock = pygame.time.Clock()
    run = True
    x, y = 0, 0
    last_move = None
    state = GAME_GOING
    won = False

    while run:
        clock.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if state != GAME_OVER:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y  = pygame.mouse.get_pos()
                    i, j = y//GRID_SIZE, x//GRID_SIZE

                    if board.board[i][j]: ## already occupied
                        sound.play()
                        break

                    if event.button == 1:
                        board.board[i][j] = 1
                        last_move = (i, j)
                        print("Human:", jarvis.evaluate_move(board, i, j), jarvis.eval)
                        won = winner(board)

                        if won == 0:
                            jarvis.generate_move(board, JARVIS)
                            won = winner(board)


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if last_move:
                            i, j = last_move
                            board.board[i][j] = 0

                draw(won)
                if won:
                    state = GAME_OVER
                    play_music("Fanfare.mp3")

    pygame.quit()


if __name__ == "__main__":
    main()


