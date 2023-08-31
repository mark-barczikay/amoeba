
import random
from board import Board

HUMAN = 1
JARVIS = 2

eval = ""

def generate_move(board: Board, player):
    if select_best_move(board, player):
        return

    for i, j in board.cells():
        if not board.empty(i, j):
            continue
        # if board.isolated(i, j):
        #    continue
        board.play_move(i, j, player)
        return

def evaluate_move(board, i, j) -> int:
    global eval
    eval = ""
    value = 0
    value += board.count_horizontal(i, j, JARVIS)
    value += board.count_vertical(i, j, JARVIS)
    value += board.count_diagonal(i, j, JARVIS)
    value += board.count_other_diagonal(i, j, JARVIS)
    value += board.count_horizontal(i, j, HUMAN)
    value += board.count_vertical(i, j, HUMAN)
    value += board.count_diagonal(i, j, HUMAN)
    value += board.count_other_diagonal(i, j, HUMAN)
    return value

def get_eval():
    return eval

def select_best_move(board: Board, player) -> bool:
    best_score = 0
    best_move = None
    best_eval = None

    for i, j in board.cells():
        if board.empty(i, j):
            score = evaluate_move(board, i, j)
            ## print(i, j, score)
            if score > best_score:
                best_score = score
                best_move = (i, j)
                best_eval = eval

    if best_move == None:
        return False

    i, j = best_move
    board.play_move(i, j, player)
    print("Jarvis: ", best_score, best_eval)
    return True




