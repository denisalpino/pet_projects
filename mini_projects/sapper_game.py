from dataclasses import dataclass, field
from random import shuffle


@dataclass(slots=True)
class Cell:
    row: int
    col: int
    mine: bool
    open: bool = field(default=False, init=False)
    neighbours: int = field(default=0, init=False)

@dataclass(slots=True)
class Game:
    rows: int
    cols: int
    mines: int
    board: list[list[Cell]] = field(init=False)

    def __post_init__(self) -> None:
        m = (self.mines * [True]) + ((self.rows * self.cols - self.mines) * [False])
        shuffle(m)
        self.board = [[Cell(i, j, m.pop()) for j in range(self.cols)] for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                start_i, start_j = i - (i - 1 >= 0), j - (j - 1 >= 0)
                stop_i, stop_j = i + (i + 1 < self.rows), j + (j + 1 < self.cols)
                nbs = [
                       self.board[r][c].mine
                       for r in range(start_i, stop_i + 1)
                       for c in range(start_j, stop_j + 1)
                       if (r, c) != (i, j)
                      ]
                setattr(self.board[i][j], 'neighbours', sum(nbs))