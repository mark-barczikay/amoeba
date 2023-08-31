import unittest
from board import Board
from jarvis import evaluate_move, JARVIS, HUMAN, get_eval

class TestBoard(unittest.TestCase):

    def no_test_cells(self):
        board = Board(3, 2)
        for cell in board.cells():
            print(cell)

    def est_o__oo(self):
        board = Board(8, 5)
        board.preset(0, 0, "oo_ox")

        self.assertEqual(0, board.count_horizontal(0, 2, JARVIS))

    def est_o___oo(self):
        board = Board(8, 5)
        board.preset(0, 0, "o___oo")

        self.assertEqual(2, board.count_horizontal(0, 1, JARVIS))

    def est_x__xx(self):
        board = Board(8, 5)
        board.preset(0, 0, "x__xx")

        self.assertEqual(4, board.count_horizontal(0, 1, HUMAN))

    def test_xxxx_(self):
        board = Board(8, 5)
        board.preset(0, 0, "xxxx_")

        print(evaluate_move(board, 0, 4))

    def est__xxxx(self):
        board = Board(18, 5)
        board.preset(0, 0, "_____xxxx")
        ## board.print()

        ## print(evaluate_move(board, 0, 4))
        ## print(board.count_horizontal_new(0, 4, HUMAN))

if __name__ == '__main__':
    unittest.main()
