from itertools import cycle, chain
from dataclasses import dataclass, field



class TicTacToe:
    def __init__(self, n: int = 3) -> None:
        self._n = n
        self._move = cycle('XO')
        self._field = [[' ' for _ in range(n)] for _ in range(n)]
        self._winner = None
        self._move_counter = 0

    def mark(self, x: int, y: int) -> None:
        if self._winner in ('X', 'O', 'Ничья'):
            print('Игра окончена')
        elif self._field[x - 1][y - 1] in 'XO':
            print('Недоступная клетка')
        else:
            self._field[x - 1][y - 1] = next(self._move)
            self._move_counter += 1

        # if someone done N moves, because of minimal number of moves to win is N
        if self._move_counter >= (2 * self._n - 1):
            comb = [row for row in self._field]                                                   # all rows
            comb.extend([[self._field[j][i] for j in range(self._n)] for i in range(self._n)])    # all columns
            comb.append([self._field[i][i] for i in range(self._n)])                              # main diagonal
            comb.append([self._field[i][2 - i] for i in range(self._n)])                          # sub diagonal

            # check if the game has ended after the current move
            if ['X'] * self._n in comb:
                self._winner = 'X'
            elif ['O'] * self._n in comb:
                self._winner = 'O'
            elif ' ' not in chain.from_iterable(comb):
                self._winner = 'Ничья'

        self.show()

    def winner(self) -> str | None:
        return self._winner

    def show(self) -> None:
        field = ['|'.join(self._field[r]) for r in range(self._n)]
        print(*('\n-----\n'.join(field)), sep='')