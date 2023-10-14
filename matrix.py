class Matrix:
    """A class describing a two-dimensional matrix"""
    def __init__(self, rows, cols, value=0):
        self.rows = rows
        self.cols = cols
        self._value = value
        self._matrix = [[value] * cols for _ in range(rows)]

    def get_value(self, row, col):
        return self._matrix[row][col]

    def set_value(self, row, col, value):
        self._matrix[row][col] = value

    def __repr__(self):
        return f'Matrix({self.rows}, {self.cols})'

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self._matrix])

    def __pos__(self):
        return self._create_matrix_instance(self.rows, self.cols)

    def __neg__(self):
        return self._create_matrix_instance(self.rows, self.cols, sign=-1)

    def __invert__(self):
        return self._create_matrix_instance(self.cols, self.rows, do_transpose=True)

    def __round__(self, n=0):
        return self._create_matrix_instance(self.rows, self.cols, do_round=True, n=n)

    def _create_matrix_instance(self, rows, cols, sign=1, do_transpose=False, do_round=False, n=0):
        """A generic method that is responsible for transposing a matrix,
        inverting and rounding its elements.

        sign - parameter responsible for inversion, if argument 1 is passed,
        the elements will remain in their original state, if -1, the elements
        will change their sign to the opposite one;
        do_transpose - parameter responsible for the necessity of matrix transposition;
        do_round - parameter responsible for the necessity of rounding of matrix elements;
        n - number of decimal places after rounding.
        """

        matrix = Matrix(rows, cols)
        for row in range(rows):
            for col in range(cols):
                r, c = (col, row) * do_transpose or (row, col)
                value = round(sign * self.get_value(r, c), n) * do_round or sign * self.get_value(r, c)
                matrix.set_value(row, col, value)
        return matrix