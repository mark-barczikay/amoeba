
HUMAN = 1
JARVIS = 2

class Board:
    def __init__(self, width, height):
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    def empty(self, i, j):
        return self.board[i][j] == 0

    def get(self, i, j):
        return self.board[i][j]

    def rows(self):
        """Generator to get all the rows"""
        row = 0
        while row < self.height:
            yield self.board[row]
            row += 1

    def cells(self):
        """Generator to iterate over all the cells"""
        i = 0
        j = 0
        while True:
            yield (i, j)
            j += 1
            if j == self.width:
                j = 0
                i += 1
                if i == self.height:
                    break

    def print(self):
        for row in self.rows():
            print(row)

    def play_move(self, i, j, player):
        self.board[i][j] = player

    def revert_move(self, i, j):
        self.board[i][j] = 0

    def preset(self, i, j, pattern):
        """Preset a pattern on the board for testing."""
        for k, c in enumerate(pattern):
            if c == '_':
                self.board[i][j+k] = 0 ## empty
            elif c == 'x':
                self.board[i][j+k] = HUMAN
            elif c == 'o':
                self.board[i][j+k] = JARVIS

    def count_left(self, i, j, player) -> int and bool:
        count = 0
        while j > 0 and self.board[i][j-1] == player:
            j = j - 1
            count += 1
        if j > 0 and self.board[i][j-1] == 0:
            return count, True
        else:
            return count, False

    def count_right(self, i, j, player) -> int and bool:
        count = 0
        while j < self.width-1 and self.board[i][j+1] == player:
            j = j + 1
            count += 1
        if j < self.width-1 and self.board[i][j+1] == 0:
            return count, True
        else:
            return count, False

    def count_up(self, i, j, player) -> int and bool:
        count = 0
        while i > 0 and self.board[i-1][j] == player:
            i = i - 1
            count += 1
        if i > 0 and self.board[i-1][j] == 0:
            return count, True
        else:
            return count, False

    def count_down(self, i, j, player) -> int and bool:
        count = 0
        while i < self.height-1 and self.board[i+1][j] == player:
            i = i + 1
            count += 1
        if i < self.height-1 and self.board[i+1][j] == 0:
            return count, True
        else:
            return count, False

    def count_upleft(self, i, j, player) -> int and bool:
        count = 0
        while i > 0 and j > 0 and self.board[i-1][j-1] == player:
            i = i - 1
            j = j - 1
            count += 1
        if i > 0 and j > 0 and self.board[i-1][j-1] == 0:
            return count, True
        else:
            return count, False

    def count_downright(self, i, j, player) -> int and bool:
        count = 0
        while i < self.height-1 and j < self.width-1 and self.board[i+1][j+1] == player:
            i = i + 1
            j = j + 1
            count += 1
        if i < self.height-1 and j < self.width-1 and self.board[i+1][j+1] == 0:
            return count, True
        else:
            return count, False

    def count_upright(self, i, j, player) -> int and bool:
        count = 0
        while i > 0 and j < self.width-1 and self.board[i-1][j+1] == player:
            i = i - 1
            j = j + 1
            count += 1
        if i > 0 and j < self.width-1 and self.board[i-1][j+1] == 0:
            return count, True
        else:
            return count, False

    def count_downleft(self, i, j, player) -> int and bool:
        count = 0
        while i < self.height-1 and j > 0 and self.board[i+1][j-1] == player:
            i = i + 1
            j = j - 1
            count += 1
        if i < self.height-1 and j > 0 and self.board[i+1][j-1] == 0:
            return count, True
        else:
            return count, False

    def count_horizontal(self, i, j, player) -> int:
        """Counts how many marks for player can be achieved horizontally
        by playing the i, j spot, so that it can be extended to 5."""

        leftcount, lefthole = self.count_left(i, j, player)
        rightcount, righthole = self.count_right(i, j, player)

        ## Check if playing (i, j) will result in a win
        if leftcount + rightcount >= 4:
            return 5000

        ## Check if playing (i, j) will result in a free-standing 4
        if leftcount + rightcount >= 3 and lefthole and righthole:
            return 2000

        ## Check if playing (i, j) will result in a 4:
        if leftcount + rightcount >= 3 and (lefthole or righthole):
            return 1000

        ## Check for xx._x
        if j > 1 and self.board[i][j-2] == player and self.board[i][j-1] == player \
            and j < self.width-2 and self.board[i][j+1] == 0 and self.board[i][j+2] == player:
            return 1000

        ## Check for x_.xx
        if j > 1 and self.board[i][j-2] == player and self.board[i][j-1] == 0 \
            and j < self.width-2 and self.board[i][j+1] == player and self.board[i][j+2] == player:
            return 1000

        ## Check for x._xx
        if j > 0 and self.board[i][j-1] == player \
            and j < self.width-3 and self.board[i][j+1] == 0 and self.board[i][j+2] == player \
            and self.board[i][j+3] == player:
            return 1000

        ## Check for xx_.x
        if j > 2 and self.board[i][j-3] == player and self.board[i][j-2] == player \
            and self.board[i][j-1] == 0 and j < self.width-1 and self.board[i][j+1] == player:
            return 1000

        ## Check for x.x_x
        if j > 1 and self.board[i][j-1] == player  \
            and j < self.width-3 and self.board[i][j+1] == player \
            and self.board[i][j+2] == 0 and self.board[i][j+3] == player:
            return 1000

        ## Check for x_x.x
        if j > 2 and self.board[i][j-1] == player and self.board[i][j-2] == 0 \
            and self.board[i][j-3] == player and j < self.width-2 and self.board[i][j+1] == player:
            return 1000

        ## Check for ._xxx
        if j < self.width-4 and self.board[i][j+1] == 0 \
            and self.board[i][j+2] == player and self.board[i][j+3] == player \
            and self.board[i][j+4] == player:
            return 1000

        ## Check for xxx_.
        if j > 3 and self.board[i][j-1] == 0 and self.board[i][j-2] == player \
            and self.board[i][j-3] == player and self.board[i][j-4] == player:
            return 1000

        ## Check if playing (i, j) will result in a free-standing 3
        if leftcount + rightcount >= 2 and lefthole and righthole:
            return 500

        ## Check if playing (i, j) will result in a 3:
        if leftcount + rightcount >= 2 and (lefthole or righthole):
            return 300

        ## Check if playing (i, j) will result in a free-standing 2
        if leftcount + rightcount >= 1 and lefthole and righthole:
            return 110

        ## Check if playing (i, j) will result in a 2:
        if leftcount + rightcount >= 1 and (lefthole or righthole):
            return 50

        return 0

    def count_vertical(self, i, j, player) -> int:
        """Counts how many marks for player can be achieved vertically
        by playing the i, j spot, so that it can be extended to 5."""

        upcount, uphole = self.count_up(i, j, player)
        downcount, downhole = self.count_down(i, j, player)

        ## Check if playing (i, j) will result in a win
        if upcount + downcount >= 4:
            return 5000

        ## Check if playing (i, j) will result in a free-standing 4
        if upcount + downcount >= 3 and uphole and downhole:
            return 2000

        ## Check if playing (i, j) will result in a 4:
        if upcount + downcount >= 3 and (uphole or downhole):
            return 1000

        ## Check for xx._x
        if i > 1 and self.board[i-2][j] == player and self.board[i-1][j] == player \
            and i < self.height-2 and self.board[i+1][j] == 0 and self.board[i+2][j] == player:
            return 1000

        ## Check for x_.xx
        if i > 1 and self.board[i-2][j] == player and self.board[i-1][j] == 0 \
            and i < self.height-2 and self.board[i+1][j] == player and self.board[i+2][j] == player:
            return 1000

        ## Check for x._xx
        if i > 0 and self.board[i-1][j] == player \
            and i < self.height-3 and self.board[i+1][j] == 0 and self.board[i+2][j] == player \
            and self.board[i+3][j] == player:
            return 1000

        ## Check for xx_.x
        if i > 2 and self.board[i-3][j] == player and self.board[i-2][j] == player \
            and self.board[i-1][j] == 0 and i < self.height-1 and self.board[i+1][j] == player:
            return 1000

        ## Check for x.x_x
        if i > 1 and self.board[i-1][j] == player  \
            and i < self.height-3 and self.board[i+1][j] == player \
            and self.board[i+2][j] == 0 and self.board[i+3][j] == player:
            return 1000

        ## Check for x_x.x
        if i > 2 and self.board[i-1][j] == player and self.board[i-2][j] == 0 \
            and self.board[i-3][j] == player and i < self.height-2 and self.board[i+1][j] == player:
            return 1000

        ## Check for ._xxx
        if i < self.height-4 and self.board[i+1][j] == 0 \
            and self.board[i+2][j] == player and self.board[i+3][j] == player \
            and self.board[i+4][j] == player:
            return 1000

        ## Check for xxx_.
        if i > 3 and self.board[i-1][j] == 0 and self.board[i-2][j] == player \
            and self.board[i-3][j] == player and self.board[i-4][j] == player:
            return 1000

        ## Check if playing (i, j) will result in a free-standing 3
        if upcount + downcount >= 2 and uphole and downhole:
            return 500

        ## Check if playing (i, j) will result in a 3:
        if upcount + downcount >= 2 and (uphole or downhole):
            return 300

        ## Check if playing (i, j) will result in a free-standing 2
        if upcount + downcount >= 1 and uphole and downhole:
            return 110

        ## Check if playing (i, j) will result in a 2:
        if upcount + downcount >= 1 and (uphole or downhole):
            return 50

        return 0

    def count_diagonal(self, i, j, player) -> int:
        """Counts how many marks for player can be achieved diagonally
        by playing the i, j spot, so that it can be extended to 5."""

        upleftcount, uplefthole = self.count_upleft(i, j, player)
        downrightcount, downrighthole = self.count_downright(i, j, player)

        ## Check if playing (i, j) will result in a win
        if upleftcount + downrightcount >= 4:
            return 5000

        ## Check if playing (i, j) will result in a free-standing 4
        if upleftcount + downrightcount >= 3 and uplefthole and downrighthole:
            return 2000

        ## Check if playing (i, j) will result in a 4:
        if upleftcount + downrightcount >= 3 and (uplefthole or downrighthole):
            return 1000

        ## Check for xx._x
        if i > 1 and j > 1 and self.board[i-2][j-2] == player and self.board[i-1][j-1] == player \
            and i < self.height-2 and j < self.width-2 and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == player:
            return 1000

        ## Check for x_.xx
        if i > 1 and j > 1 and self.board[i-2][j-2] == player and self.board[i-1][j-1] == 0 \
            and i < self.height-2 and j < self.width-2 and self.board[i+1][j+1] == player and self.board[i+2][j+2] == player:
            return 1000

        ## Check for x._xx
        if i > 0 and j > 0 and self.board[i-1][j-1] == player \
            and i < self.height-3 and j < self.width-3 and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == player \
            and self.board[i+3][j+3] == player:
            return 1000

        ## Check for xx_.x
        if i > 2 and j > 2 and self.board[i][j] == 0 and self.board[i-1][j-1] == player \
            and i < self.height-1 and j < self.width-1 and self.board[i+1][j+1] == player:
            return 1000

        ## Check for x.x_x
        if i > 1 and j > 1 and self.board[i-1][j-1] == player \
            and i < self.height-3 and j < self.width-3 and self.board[i+1][j+1] == player \
            and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == player:
            return 1000

        ## Check for x_x.x
        if i > 2 and j > 2 and self.board[i-1][j-1] == player and self.board[i-2][j-2] == 0 \
            and self.board[i-3][j-3] == player and i < self.height-2 and j < self.width-2 and self.board[i+1][j+1] == player:
            return 1000

        ## Check for ._xxx
        if i < self.height-4 and j < self.width-4 and self.board[i+1][j+1] == 0 \
            and self.board[i+2][j+2] == player and self.board[i+3][j+3] == player \
            and self.board[i+4][j+4] == player:
            return 1000

        ## Check for xxx_.
        if i > 3 and j > 3 and self.board[i-1][j-1] == 0 and self.board[i-2][j-2] == player \
            and self.board[i-3][j-3] == player and self.board[i-4][j-4] == player:
            return 1000

        ## Check if playing (i, j) will result in a free-standing 3
        if upleftcount + downrightcount >= 2 and uplefthole and downrighthole:
            return 500

        ## Check if playing (i, j) will result in a 3:
        if upleftcount + downrightcount >= 2 and (uplefthole or downrighthole):
            return 300

        ## Check if playing (i, j) will result in a free-standing 2
        if upleftcount + downrightcount >= 1 and uplefthole and downrighthole:
            return 110

        ## Check if playing (i, j) will result in a 2:
        if upleftcount + downrightcount >= 1 and (uplefthole or downrighthole):
            return 50

        return 0

    def count_other_diagonal(self, i, j, player) -> int:
        """Counts how many marks for player can be achieved diagonally
        by playing the i, j spot, so that it can be extended to 5."""

        uprightcount, uprighthole = self.count_upright(i, j, player)
        downleftcount, downlefthole = self.count_downleft(i, j, player)

        ## Check if playing (i, j) will result in a win
        if uprightcount + downleftcount >= 4:
            return 5000

        ## Check if playing (i, j) will result in a free-standing 4
        if uprightcount + downleftcount >= 3 and uprighthole and downlefthole:
            return 2000

        ## Check if playing (i, j) will result in a 4:
        if uprightcount + downleftcount >= 3 and (uprighthole or downlefthole):
            return 1000

        ## Check for xx._x
        if i > 1 and j < self.width-2 and self.board[i-2][j+2] == player and self.board[i-1][j+1] == player \
            and i < self.height-2 and j > 1 and self.board[i+1][j-1] == 0 and self.board[i+2][j-2] == player:
            return 1000

        ## Check for x_.xx
        if i > 1 and j < self.width-2 and self.board[i-2][j+2] == player and self.board[i-1][j+1] == 0 \
            and i < self.height-2 and j > 1 and self.board[i+1][j-1] == player and self.board[i+2][j-2] == player:
            return 1000

        ## Check for x._xx
        if i > 0 and j < self.width-1 and self.board[i-1][j+1] == player \
            and i < self.height-3 and j > 2 and self.board[i+1][j-1] == 0 and self.board[i+2][j-2] == player \
            and self.board[i+3][j-3] == player:
            return 1000

        ## Check for xx_.x
        if i > 2 and j < self.width-3 and self.board[i][j] == 0 and self.board[i-1][j+1] == player \
            and i < self.height-1 and j > 0 and self.board[i+1][j-1] == player:
            return 1000

        ## Check for x_x.x
        if i > 2 and j < self.width-3 and self.board[i-1][j+1] == player and self.board[i-2][j+2] == 0 \
            and self.board[i-3][j+3] == player and i < self.height-1 and j > 0 and self.board[i+1][j-1] == player:
            return 1000

        ## check for x.x_x
        if i > 1 and j < self.width-2 and self.board[i-1][j+1] == player and self.board[i][j] == 0 \
            and i < self.height-2 and j > 1 and self.board[i+1][j-1] == player and self.board[i+2][j-2] == player:
            return 1000

        ## Check for ._xxx
        if i < self.height-4 and j > 3 and self.board[i+1][j-1] == 0 \
            and self.board[i+2][j-2] == player and self.board[i+3][j-3] == player \
            and self.board[i+4][j-4] == player:
            return 1000

        ## Check for xxx_.
        if i > 3 and j < self.width-4 and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == player \
            and self.board[i-3][j+3] == player and self.board[i-4][j+4] == player:
            return 1000

        ## Check if playing (i, j) will result in a free-standing 3
        if uprightcount + downleftcount >= 2 and uprighthole and downlefthole:
            return 500

        ## Check if playing (i, j) will result in a 3:
        if uprightcount + downleftcount >= 2 and (uprighthole or downlefthole):
            return 300

        ## Check if playing (i, j) will result in a free-standing 2
        if uprightcount + downleftcount >= 1 and uprighthole and downlefthole:
            return 110

        ## Check if playing (i, j) will result in a 2:
        if uprightcount + downleftcount >= 1 and (uprighthole or downlefthole):
            return 50

        return 0


    def isolated(self, i, j) -> bool:
        if i+1 < self.height and self.board[i+1][j] != 0:
            return False
        if i > 0 and self.board[i-1][j] != 0:
            return False
        if j+1 < self.width and self.board[i][j+1] != 0:
            return False
        if j > 0 and self.board[i][j-1] != 0:
            return False
        if i+1 < self.height and j+1 < self.width and self.board[i+1][j+1] != 0:
            return False
        if i+1 < self.height and j > 0 and self.board[i+1][j-1] != 0:
            return False
        if i > 0 and j > 0 and self.board[i-1][j-1] != 0:
            return False
        if i > 0 and j+1 < self.width and self.board[i-1][j+1] != 0:
            return False
        return True


    def connect(self, i, j, player) -> int:
        """Checks if 5 is reached by placing at i, j"""

        if self.count_horizontal(i, j, player) >= 5000:
            return True

        if self.count_vertical(i, j, player) >= 5000:
            return True

        if self.count_diagonal(i, j, player) >= 5000:
            return True

        if self.count_other_diagonal(i, j, player) >= 5000:
            return True

        return False
