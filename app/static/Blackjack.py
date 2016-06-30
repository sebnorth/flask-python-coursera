# Mini-project 6 for An Introduction to Interactive Programming in Python class

# based on the template from: http://www.codeskulptor.org/#examples-blackjack_template.py

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome_d = ""
outcome_p = ""
score = 0
WID = 600
HEI = 600

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return str([card.__str__() for card in self.hand])

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = sum([VALUES[x.get_rank()] for x in self.hand if not x.get_rank() == 'A'] ) 
        aces_in_hand  = sum([x.get_rank() == 'A' for x in self.hand])
        value = value + aces_in_hand
        for i in range(aces_in_hand):
            if value + 10 <= 21:
                value = value + 10
            else:
                pass
        return value
    
    def draw(self, canvas, pos):
        pom = pos
        for i in self.hand:
            i.draw(canvas, pom)
            pom[0]+=CARD_SIZE[0]
            
    def draw2(self, canvas, pos):
        pom = pos
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        pom[0]+=CARD_SIZE[0]
        for i in range(1, len(self.hand)):
            self.hand[i].draw(canvas, pom)
            pom[0]+=CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(x,y) for x in SUITS for y in RANKS]
        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        pom = self.deck.pop()
        return pom
    
    
    def __str__(self):
        return str([x.get_suit() + x.get_rank() for x in self.deck])



#define event handlers for buttons
def deal():
    global outcome_d, outcome_p, in_play, deck, player_hand, dealer_hand, canvas, score

    # your code goes here
    if in_play:
        outcome_d = "You lost, you pressed Deal button during the game"
        outcome_p =  "New Game? Press Deal button"
        score -=1
        in_play = False
    else:
        deck = Deck()
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        outcome_d = "Stand or Hit?"
        outcome_p = "Play!:)"
        #print "player's hand: ", player_hand
        #print "dealer's hand: ", dealer_hand
        in_play = True

def hit():
    global deck, player_hand, outcome_d, outcome_p, in_play, score
 
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome_d = "You have busted"
            in_play = False
            outcome_p =  "New Game? Press Deal button"
            score -= 1
    else:
        pass
            
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, outcome_d, outcome_p, dealer_hand, player_hand, score
    if not in_play:
        if player_hand.get_value() > 21:
            outcome_d = "I remind You, You have already busted"
    else:
        pom = dealer_hand.get_value()
        while (pom < 17):
            dealer_hand.add_card(deck.deal_card())
            pom = dealer_hand.get_value()
        if dealer_hand.get_value() > 21:
            outcome_d = "I have busted, You won!:)"
            score += 1
            in_play = False
            outcome_p = "New Game? Press Deal button"
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                in_play = False
                outcome_d = "I won, You lost"
                score -= 1
                outcome_p = "New Game? Press Deal button"
            else:
                in_play = False
                outcome_d = "I lost, You won"
                score += 1
                outcome_p = "New Game? Press Deal button"
            
  
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome_d, outcome_p, score, dealer_hand, player_hand, in_play
    canvas.draw_text('Blackjack', [WID/5, HEI/8], 55, 'Orange', 'serif')
    canvas.draw_text('Score: ' + str(score), [3*WID/4, HEI/8], 35, 'Purple')
    canvas.draw_text('Dealer', [WID/8, 3*HEI/10], 25, 'Black')
    canvas.draw_text(outcome_d, [WID/2, 3*HEI/10], 25, 'Yellow')
    canvas.draw_text('Player', [WID/8, 6*HEI/10], 25, 'Black')
    canvas.draw_text(outcome_p, [WID/2, 6*HEI/10], 25, 'Yellow')
    if in_play:
        dealer_hand.draw2(canvas, [WID/8, .35*HEI])
    else:
        dealer_hand.draw(canvas, [WID/8, .35*HEI])
    player_hand.draw(canvas, [WID/8, .65*HEI])
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    
#    c1 = Card("S", "A")
#    c2 = Card("C", "2")
#    c3 = Card("D", "T")
#    test_hand = Hand()
#    test_hand.add_card(c1)
#    test_hand.add_card(c2)
#    test_hand.add_card(c3)
#    test_hand.draw(canvas, [300, 300])

# initialization frame
frame = simplegui.create_frame("Blackjack", WID+300, HEI)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
# deck = Deck()
deal()
frame.start()



# remember to review the gradic rubric
