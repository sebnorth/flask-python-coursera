# Mini-project 2 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_ttt_template.py

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 50    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    simulation of a single game 
    """
    if len(board.get_empty_squares()) > 0:
        gra_w_toku = True
    else:
        gra_w_toku = False
    while gra_w_toku:
        tupka = random.choice(board.get_empty_squares())
        board.move(tupka[0], tupka[1], player)
        status = board.check_win()
        if status == player or status == provided.DRAW:
            gra_w_toku = not gra_w_toku
        player = provided.switch_player(player)
    return None



def helper(won, znak, player, scores, row, col):
    """
    helper function
    """
    if won:
        if znak == player:
            scores[row][col]+=MCMATCH
        elif znak == provided.EMPTY:
            pass   
        else:
            scores[row][col]-=MCOTHER 
    else:
        if znak == player:
            scores[row][col]-=MCMATCH
        elif znak == provided.EMPTY:
            pass
        else:
            scores[row][col]+=MCOTHER
    


def mc_update_scores(scores, board, player): 
    """
    return nothing but updating a score
    """
    status = board.check_win()
    if status == provided.DRAW:
        pass
    if status == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                    znak = board.square(row, col)
                    helper(True, znak, player, scores, row, col)
                
            
    if status == provided.switch_player(player):
         for row in range(board.get_dim()):
             for col in range(board.get_dim()):
                    znak = board.square(row, col)
                    helper(False, znak, player, scores, row, col)
       
                    
    return None

def get_best_move(board, scores):
    """
    return best_move. 
    """
    lista = board.get_empty_squares()
    score_max = [scores[dummy_x[0]][dummy_x[1]] for dummy_x in lista]
    score_max.sort()
    max_wynik = score_max[len(score_max)-1]
    lista_max = []
    for dummy_x in lista:
        if scores[dummy_x[0]][dummy_x[1]] == max_wynik:
            lista_max.append(dummy_x)
    return random.choice(lista_max)      
                

def mc_move(board, player, trials):
    """
    return a move for the machine player in the form of a (row, column) tuple. 
    """
    grid_of_scores = [[0 for dummy_i in range(board.get_dim())] for dummy_j in range(board.get_dim())]
    test_board = board.clone()
    for dummy_i in range(trials):
        mc_trial(test_board, player)
        mc_update_scores(grid_of_scores, test_board, player)
        test_board = board.clone()
    best_move = get_best_move(board, grid_of_scores)      
    return best_move



# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
