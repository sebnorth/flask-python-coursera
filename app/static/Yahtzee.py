# Mini-project 3 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_yahtzee_template.py

"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    list_hand = list(hand)
    if len(list_hand) == 0:
        return 0
    else:
        ilosci = [dummy_x*list_hand.count(dummy_x) for dummy_x in list_hand]
        return max(ilosci)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = set([x+1 for x in range(num_die_sides)])
    suma = 0
    lista = gen_all_sequences(outcomes, num_free_dice)
    for tupla in lista:
        held_dice_list = list(held_dice)
        tupla_list = list(tupla)
        held_dice_list.extend(tupla_list)
        hand = tuple(held_dice_list)
        suma+=score(hand)
    return suma/float(num_die_sides**num_free_dice)



def gen_all_combs(outcomes, length):
    """
    Iterative function that enumerates the set of all combinations of
    outcomes of given length
    """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            if len(list(seq)) == 0:
                outc = list(outcomes)
            else:
                lista = list(outcomes)
                outc = lista[max(list(seq))+1:]
            for item in outc:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

def gen_all_holds_len(hand, length, indeksy):
    """
    Generate all possible choices of dice from hand of given length to hold.
    """
    seq_outcomes = gen_all_combs(indeksy, length)
    wartosci_l = list(hand)
    holds = [tuple([wartosci_l[x] for x in tupla]) for tupla in seq_outcomes]
    return holds

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    temp = set([()])
    for dlugosc_podzbioru in range(len(hand)+1):
        outcomes = set(range(len(hand)))
        wartosci_l = gen_all_holds_len(hand, dlugosc_podzbioru, outcomes)
        for tupla in wartosci_l:
            temp.add(tupla)
    tupla_pusta = tuple()
    temp.add(tupla_pusta)
    return temp



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hand_discard = gen_all_holds(hand)
    score_max = 0.0
    for held in hand_discard:
        num_free_dice = len(hand) - len(held)
        score_num = expected_value(held, num_die_sides, num_free_dice)
        if score_num > score_max:
            score_max = score_num
            held_to_hold = held
    return (score_max, held_to_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

