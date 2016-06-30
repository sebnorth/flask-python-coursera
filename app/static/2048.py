# Mini-project 0 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_2048_template.py

import poc_2048_gui, random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def rowcow_helper(aaa,bbb):
    """
    Function that helps.
    """
    return {UP: (aaa, bbb),
           DOWN: (aaa, bbb),
           LEFT: (bbb, aaa),
           RIGHT: (bbb, aaa)}

def start_index(direction, grid_height, grid_width):
    """
    Function that helps.
    """
    if direction == UP:
        return 0
    elif direction == DOWN:
        return grid_height-1
    elif direction == LEFT:
        return 0
    else:
        return grid_width-1
    

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    size = len(line)
    line2 = []; 
    for index in range(size):
        if line[index]:
            line2.append(line[index])
    size = len(line) - len(line2)
    for index in range(size):
        line2.append(0)
    index = 0
    line3 = []
    size = len(line2)
    while (index < size-1):
        if line2[index] == line2[index+1]:
            line3.append(2*line2[index])
            line3.append(0)
            index+=2
        else:
            line3.append(line2[index])
            index+=1     
    if index == size-1:
        line3.append(line2[index])
    line4 = []
    size= len(line3)
    for index in range(size):
        if line3[index]:
            line4.append(line3[index])
    size = len(line3) - len(line4)
    for index in range(size):
        line4.append(0)
    return line4

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._board = [[0 for _ in range(self._grid_width)] for _ in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._board)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        rowcow = rowcow_helper(self._grid_width, self._grid_height)
        count = 0
        for idw in range(rowcow[direction][0]):
            temp = []
            if direction == UP or direction == DOWN:
                row = start_index(direction, self._grid_height, self._grid_width)
                col = idw
            else:
                col = start_index(direction, self._grid_height, self._grid_width)
                row = idw
            for idh in range(rowcow[direction][1]):
                temp.append(self._board[row][col])
                row+=OFFSETS[direction][0]
                col+=OFFSETS[direction][1]
            new_temp = merge(temp)
            if direction == UP or direction == DOWN:
                row = start_index(direction, self._grid_height, self._grid_width)
                col = idw
            else:
                col = start_index(direction, self._grid_height, self._grid_width)
                row = idw
            for idh in range(rowcow[direction][1]):
                self._board[row][col] = new_temp[idh]
                row+=OFFSETS[direction][0]
                col+=OFFSETS[direction][1]
            if direction == UP or direction == DOWN:
                row = start_index(direction, self._grid_height, self._grid_width)
                col = idw
            else:
                col = start_index(direction, self._grid_height, self._grid_width)
                row = idw
            count+= sum([self._board[row][col] != temp[idh] for idh in range(rowcow[direction][1])])
        if count:
            self.new_tile()
                    

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile_values = [2,2,2,2,2,2,2,2,2,4]
        idx = 0
        idy = 0
        zero_board = [(idy, idx) for idy in range(self._grid_height) for idx in range(self._grid_width) if not self._board[idy][idx]]
        if zero_board:
            idx, idy = random.choice(zero_board)
            self._board[idx][idy] = random.choice(tile_values)
            
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._board[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

#import poc_simpletest
#
#suite = poc_simpletest.TestSuite()
#
#def test1():
#        suite.run_test(TwentyFortyEight(2, 2).__str__(), str([[0,0],[0,0]]), "Test #1")
#        suite.run_test(TwentyFortyEight(2, 3).__str__(), str([[0,0,0],[0,0,0]]), "Test #2")
#        suite.report_results()
#        
#def test2():
#    board = TwentyFortyEight(2, 2)
#    board.set_tile(0,0,2)
#    board.set_tile(0,1,2)
#    board.set_tile(1,0,2)
#    board.set_tile(1,1,2)
#    board.move(UP)
#    board.move(LEFT)
#    print board
#    
#
#test2()
