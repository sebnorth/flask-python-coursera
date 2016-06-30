# Mini-project 5 for An Introduction to Interactive Programming in Python class

# based on the template from: http://www.codeskulptor.org/#examples-memory_template.py

import simplegui
import random

memory_deck = range(8) + range(8)
print memory_deck
exposed = [False]*8 + [False]*8

print exposed
board_height = 100
board_width = 800
half_card_width = board_width / 32
half_card_height = 44
first = -1
second = -1
state = 0
turns = 0


# helper function to initialize globals
def new_game():
    global state, exposed, first, second, state, turns
    first = -1
    second = -1
    state = 0
    turns = 0
    exposed = [False]*8 + [False]*8
    random.shuffle(memory_deck) 
    label.set_text("Turns = " + str(turns))
    

     
# define event handlers
def mouseclick(pos):
    global first, second, state, turns
    # add game state logic here
    # print pos[0]/(2*half_card_width)
    card_number = pos[0]/(2*half_card_width)
    if state == 0:
        if not exposed[card_number]:
            exposed[card_number] = not exposed[card_number]
            turns+=1
            label.set_text("Turns = " + str(turns))
            first = card_number
            state = 1
        else:
            pass
    elif state == 1:
        if not exposed[card_number]:
            exposed[card_number] = not exposed[card_number]
            second = card_number
            state = 2       
    else:
        if not exposed[card_number]:
            if memory_deck[first] == memory_deck[second]:
                pass
            else:
                exposed[first] = not exposed[first]
                exposed[second] = not exposed[second]
            exposed[card_number] = not exposed[card_number]
            turns+=1
            label.set_text("Turns = " + str(turns))
            first = card_number
            state = 1
        
    
        
                         
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for idx in range(16):
        if exposed[idx]:
            canvas.draw_text(str(memory_deck[idx]), (half_card_width + idx*board_width/16, board_height/2), 30, 'Red')
        else:
            LU = [idx*board_width/16, board_height/2 - half_card_height]
            RU = [idx*board_width/16 + 2*half_card_width , board_height/2 - half_card_height]
            RB = [idx*board_width/16 + 2*half_card_width , board_height/2 + half_card_height]
            LB = [idx*board_width/16, board_height/2 + half_card_height]
            canvas.draw_polygon([LU,RU,RB,LB], 2, 'Yellow', 'Green')
        
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
