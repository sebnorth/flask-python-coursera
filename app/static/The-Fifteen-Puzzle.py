# Mini-project 7 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_fifteen_template.py

"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui
import math 

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        wynik = True
        wynik = wynik and target_row > 1
        if wynik:
            wynik = wynik and self._grid[target_row][target_col] == 0
        for row in range(target_row+1, self._height):
            for col in range(self._width):
                wynik = wynik and self.current_position(row,col) == (row, col)
                if not wynik:
                    break
            if not wynik:
                    break
        for col in range(target_col+1, self._width):
                wynik = wynik and  self.current_position(target_row,col) == (target_row, col)
                if not wynik:
                    break
        return wynik

    def position_tile(self, target_row, target_col, current_row, current_col, par = True):
        """
        helper function
        """
        col_prim = abs(current_col - target_col)
        row_prim = target_row - current_row
        word = ''
        if target_col == current_col:
            word+='u'*row_prim
            word+= 'lddru'*(row_prim - 1)
            word+='ld'
        elif target_row == current_row:
            word = ''
            word+= 'l'*col_prim
            word+= 'urrdl'*(col_prim - 1)
        else:
            case2a = current_col - target_col > 0 and row_prim > 1
            case2b = current_col - target_col > 0 and row_prim == 1 and par
            case2c = current_col - target_col < 0 and row_prim > 1
            case2d = current_col - target_col < 0 and row_prim == 1
            case2e = current_col - target_col > 0 and row_prim == 1 and not par
            case2f = current_col - target_col < 0 and row_prim == 1 and not par
            if case2a or case2e:
                word = ''
                word+= 'u'*row_prim
                word+= 'r'*col_prim
                word+= 'dllur'*(col_prim - 1)
                word+= 'dl'*1
                word+= 'd'*(row_prim - 1) 
                word+='u'*row_prim
                word+= 'lddru'*(row_prim - 1)
                word+='ld'
            if case2b:
                word = '' + 'u'*1 + 'r'*col_prim + 'ulldr'*(col_prim - 1)
                word+= 'ullddr'*1
                word+='u'*row_prim
                word+= 'lddru'*(row_prim - 1)
                word+='ld'
            if case2c or case2f:
                word = '' + 'u'*row_prim + 'l'*col_prim + 'drrul'*(col_prim - 1)
                word+= 'dr'*1
                word+= 'd'*(row_prim - 1)
                word+='u'*row_prim
                word+= 'lddru'*(row_prim - 1)
                word+='ld'
            if case2d:
                word = '' + 'u'*1 + 'l'*col_prim + 'urrdl'*(col_prim - 1) + 'dr'*1
                word+='u'*row_prim + 'lddru'*(row_prim - 1) + 'ld'
        return word    
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        current_row, current_col = self.current_position(target_row, target_col)
        word = self.position_tile(target_row, target_col, current_row, current_col, True)
        self.update_puzzle(word)
        assert self.lower_row_invariant(target_row, target_col-1)
        return word

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), "przed"
        word = ''
        word+= "ur"
        self.update_puzzle(word)
        print word
        if self.current_position(target_row, 0) == (target_row, 0):
            word = 'r'*(self._width - 2)
            self.update_puzzle(word)
            # print (target_row - 1, self._width -1)
            if target_row-1 > 1:
                assert self.lower_row_invariant(target_row - 1, self._width -1), "po"
            return "ur" + word
        else:
            current_col, current_row = self.current_position(target_row, 0) 
            # col_prim = abs(current_col - 1)
            word = self.position_tile(target_row-1, 1, current_col, current_row, False) 
            self.update_puzzle(word)
            self.update_puzzle('ruldrdlurdluurddlur') 
            self.update_puzzle('r'*(self._width - 2))
            if target_row-1 > 1:
                assert self.lower_row_invariant(target_row - 1, self._width -1), "po"
            return 'ur' + word + 'ruldrdlurdluurddlur' + 'r'*(self._width - 2)

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        wynik = True
        if wynik:
            wynik = wynik and self._grid[0][target_col] == 0
        if wynik:
            wynik = wynik and  self.current_position(1,target_col) == (1,target_col)
        for row in range(2, self._height):
            for col in range(self._width):
                wynik = wynik and self.current_position(row,col) == (row, col)
                if not wynik:
                    break
            if not wynik:
                    break
        for col in range(target_col+1,self._width):
            wynik = wynik and  self.current_position(0,col) == (0, col)
            wynik = wynik and  self.current_position(1,col) == (1, col)
            if not wynik:
                    break
        return wynik

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        wynik = True
        # wynik = wynik and target_col >= 1
        if wynik:
            wynik = wynik and self._grid[1][target_col] == 0
        for row in range(2, self._height):
            for col in range(self._width):
                wynik = wynik and self.current_position(row,col) == (row, col)
                if not wynik:
                    break
            if not wynik:
                    break
        for col in range(target_col+1,self._width):
            wynik = wynik and  self.current_position(0,col) == (0, col)
            wynik = wynik and  self.current_position(1,col) == (1, col)
            if not wynik:
                    break
        return wynik

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        word = 'ld'
        self.update_puzzle(word)
        if self.current_position(0, target_col) == (0, target_col):
            assert self.row1_invariant(target_col-1)
            return 'ld'
        else:
            current_row, current_col = self.current_position(0, target_col)
            col_prim = abs(current_col - (target_col - 1))
            if col_prim == 0:
                word='uld'
            else:
                word = ''
                if current_row == 1:
                    word+='l'*col_prim
                    word+= 'urrdl'*(col_prim - 1)
                else:
                    word+='l'*col_prim
                    word+='urdl'
                    word+='urrdl'*(col_prim - 1)
            self.update_puzzle(word)
            self.update_puzzle('urdlurrdluldrruld')
        assert self.row1_invariant(target_col-1)
        return 'ld' + word + 'urdlurrdluldrruld'
    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        current_row, current_col = self.current_position(1, target_col)
        col_prim = abs(current_col - target_col)
        word = ''
        if current_row == 1:
            word+='l'*col_prim
            word+= 'urrdl'*(col_prim - 1)
            word+='ur'
        elif col_prim == 0:
            word+='u'
        else:
            word+='l'*col_prim
            word+='urdl'
            word+='urrdl'*(col_prim - 1)
            word+='ur'
        self.update_puzzle(word)
        print self
        assert self.row0_invariant(target_col)
        return word

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        done = False
        slowo = 'rdlurdlurdlurdlurdlu'
        slownik = {(0,0) : 'r', (0,1) : 'd', (1,0): 'u', (1,1): 'l'}
        current_row, current_col = self.current_position(0,0)
        kierunek = slownik[(current_row, current_col)]
        indeks =  slowo.index(kierunek)
        klon = self.clone()
        dummy_i = 0
        wynik = ''
        while not done and dummy_i<12 :
            lista = [klon.get_number(0,0), klon.get_number(0,1), klon.get_number(1,0), klon.get_number(1,1)]
            if lista == sorted(lista):
                done = True
            else:
                wynik+=slowo[indeks + dummy_i]
                klon.update_puzzle(slowo[indeks + dummy_i])
                dummy_i+=1        
        if done:
            self.update_puzzle(wynik)
            return wynik
        else:
            return "error"

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        word = ''
        zero_row, zero_col = self.current_position(0, 0)
        col_prim = self._width-1 - zero_col
        row_prim = self._height-1 - zero_row
        word+='d'*row_prim
        word+='r'*col_prim
        self.update_puzzle(word)
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width -1, 0, -1):
                word+=self.solve_interior_tile(row, col)
            word+=self.solve_col0_tile(row)
        for col in range(self._width -1, 1, -1): 
            word+=self.solve_row1_tile(col)
            word+=self.solve_row0_tile(col)
        word+=self.solve_2x2()
        return word

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

#my_puzzle = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0,7,8]])
#my_puzzle = Puzzle(4, 5, [[8, 2, 10, 9, 1], [7, 6, 5, 4, 3], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(my_puzzle)
#print my_puzzle.lower_row_invariant(2,1)
#print my_puzzle
#print my_puzzle.solve_col0_tile(2)

#my_puzzle = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(my_puzzle)
#print my_puzzle.solve_row0_tile(2) 

#my_puzzle = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
# poc_fifteen_gui.FifteenGUI(my_puzzle)
#print my_puzzle.solve_puzzle()
