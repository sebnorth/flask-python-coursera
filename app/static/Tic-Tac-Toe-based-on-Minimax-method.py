# Mini-project 6 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_tttmm_template.py


"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win():
        if provided.DRAW == board.check_win():
            return 0, (-1, -1)
        else:
            return SCORES[provided.switch_player(player)], (-1, -1)
    else:
        empty_sq = board.get_empty_squares()
        if player == provided.PLAYERX:
            max_x = -1
            best_move = (-1,-1)
            playerr = provided.switch_player(player)
            for item in empty_sq:
                boardd = board.clone()
                boardd.move(item[0], item[1], player)
                score_to_compare = mm_move(boardd, playerr)[0]
                if score_to_compare > max_x:
                    max_x = score_to_compare
                    best_move = item
                if max_x == 1:
                    break
            return max_x, best_move        
        else:
            min_x = 1
            best_move = (-1,-1)
            playerr = provided.switch_player(player)
            for item in empty_sq:
                boardd = board.clone()
                boardd.move(item[0], item[1], player)
                score_to_compare = mm_move(boardd, playerr)[0]
                if score_to_compare <= min_x:
                    min_x = score_to_compare
                    best_move = item
                if min_x == -1:
                    break
            return min_x, best_move   

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


#import user36_AQLww3W1YBS5oCt as unit_test
#unit_test.test_mm_move(mm_move)
