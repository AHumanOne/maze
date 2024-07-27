import random
import time
from cell import Cell


class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        if seed:
            random.seed(seed)
        self._break_walls_r(0,0)
        self._reset_cells_visited()
        self.solve()
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i,j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_moves = []
            if i-1 >= 0 and self._cells[i-1][j].visited == False:
                possible_moves.append((i-1, j))
            if j-1 >= 0 and self._cells[i][j-1].visited == False:
                possible_moves.append((i, j-1))
            if i+1 < self._num_cols and self._cells[i+1][j].visited == False:
                possible_moves.append((i+1, j))
            if j+1 < self._num_rows and self._cells[i][j+1].visited == False:
                possible_moves.append((i,j+1))
            if len(possible_moves) == 0:
                self._draw_cell(i,j)
                return
            random_move = random.choice(possible_moves)
            #need to break the walls between the 2 cells
            if random_move[0] == i and random_move[1] > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[random_move[0]][random_move[1]].has_top_wall = False

            if random_move[0] == i and random_move[1] < j:
                self._cells[i][j].has_top_wall = False
                self._cells[random_move[0]][random_move[1]].has_bottom_wall = False

            if random_move[0] > i and random_move[1] == j:
                self._cells[i][j].has_right_wall = False
                self._cells[random_move[0]][random_move[1]].has_left_wall = False

            if random_move[0] < i and random_move[1] == j:
                self._cells[i][j].has_left_wall = False
                self._cells[random_move[0]][random_move[1]].has_right_wall = False

            self._break_walls_r(random_move[0], random_move[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
    
    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        if i-1 >= 0 and self._cells[i-1][j].visited == False and not self._cells[i-1][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1,j):
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j], True)
        if j-1 >= 0 and self._cells[i][j-1].visited == False and not self._cells[i][j-1].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i,j-1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], True)
        if i+1 < self._num_cols and self._cells[i+1][j].visited == False and not self._cells[i+1][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1,j):
                return True
            self._cells[i][j].draw_move(self._cells[i+1][j], True)
        if j+1 < self._num_rows and self._cells[i][j+1].visited == False and not self._cells[i][j+1].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i,j+1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1], True)
        return False


            
