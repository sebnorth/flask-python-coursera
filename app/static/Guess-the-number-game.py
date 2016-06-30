# Mini-project 2 for An Introduction to Interactive Programming in Python class
# based on the template from: http://www.codeskulptor.org/#examples-guess_the_number_template.py
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

# initialize global variables used in your code
secret_number = 0
low = 0
high = 100
number_of_remaining_guesses = 7


# helper function to start and restart the game
def new_game():
    global secret_number, number_of_remaining_guesses
    secret_number = random.randrange(low, high)  
    if high == 100:
        number_of_remaining_guesses = 7
    else:
        number_of_remaining_guesses = 10
    # print secret_number
    print 
    print "A new game! Choose a number in range [", low, ",", high, ")"
    print "Left", number_of_remaining_guesses, "guesses"
    # remove this when you add your code    
   


# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global low, high, number_of_remaining_guesses
    low = 0
    high = 100
    number_of_remaining_guesses = 7
    new_game()


def range1000():
    # button that changes range to range [0,1000) and restarts
    global low, high, number_of_remaining_guesses
    low = 0
    high = 1000
    number_of_remaining_guesses = 10   
    new_game() 

    
def input_guess(guess):
    # main game logic goes here	
    
    global number_of_remaining_guesses
    guessi = int(guess)
    print "Your choice is: ", guessi
    if guessi == secret_number:
        print "You won! Congratulations!:)"
        new_game()
        
    elif guessi < secret_number:
        print "Higher!:) "
        number_of_remaining_guesses-=1
        
        if (number_of_remaining_guesses == 0):
            print "Game over."
            new_game()
        else:
            print "Left", number_of_remaining_guesses, "guesses"
    else:
        print "Lower!:) "
        number_of_remaining_guesses-=1
        if (number_of_remaining_guesses == 0):
            print "Game over."
            new_game()
        else:
            print "Left", number_of_remaining_guesses, "guesses"
    pass

    
# create frame
frame = simplegui.create_frame("Window Name", 0, 200, 400)


# register event handlers for control elements
frame.add_button("leval 1 - [0,100) range", range100, 300)
frame.add_button("level 2 - [0,1000) range", range1000, 300)
frame.add_input("Enter your number: ", input_guess, 200)

# call new_game and start frame

new_game()
frame.start()



# always remember to check your completed program against the grading rubric
