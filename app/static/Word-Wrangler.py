# Mini-project 5 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_wrangler_template.py

"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(10)

WORDFILE = "http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    
    if not list1:
        return []
    else:
        in_list = True
        list_counter = 0
        list_copy = []
        list_copy.append(list1[list_counter])
        len_list = len(list1)
        new_index = list_counter
        while in_list:
            new_index+=1
            if new_index < len_list:
                if list1[new_index] != list1[list_counter]:
                    list_counter = new_index
                    list_copy.append(list1[list_counter])
                else:
                    pass
            else:
                in_list = False
        return list_copy        
            

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    wynik = []
    wsk1 = 0
    wsk2 = 0
    if not list1:
        return wynik
    elif not list2:
        return wynik
    else:
        in_list = wsk1 < len(list1) and wsk2 < len(list2)
        while in_list:
            if list1[wsk1] == list2[wsk2]:
                wynik.append(list1[wsk1])
                wsk1+=1
                wsk2+=1
            elif list1[wsk1] < list2[wsk2]:
                wsk1+=1
            else:
                wsk2+=1
            in_list = wsk1 < len(list1) and wsk2 < len(list2)    
    return wynik

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    wynik = []
    clist1 = list(list1)
    clist2 = list(list2)
    in_list = len(clist1)>0 and len(clist2) > 0
    while in_list:
        if clist1[0] > clist2[0]:
            wynik.append(clist2.pop(0))
        else:
            wynik.append(clist1.pop(0))
        in_list = len(clist1)>0 and len(clist2) > 0
    if len(clist1) > 0:
        wynik.extend(clist1)
    if len(clist2) > 0:
        wynik.extend(clist2)    
    return wynik
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if not list1:
        return list1
    elif len(list1) == 1:
        return list1
    else:
        lewy = 0
        prawy = len(list1)-1
        srodkowy = (lewy + prawy) / 2
        lista_lewa = merge_sort(list1[lewy:srodkowy+1])
        lista_prawa = merge_sort(list1[srodkowy+1:])
        wynik = merge(lista_lewa, lista_prawa)
    return wynik

# Function to generate all strings for the word wrangler game
    
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    # print word
    if len(word) == 0:
        return [word]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        list_b = []
        # a.extend(rest_strings)
        for item in rest_strings:
            for dummy_i in range(len(item)+1):
                pom = list(item)
                pom.insert(dummy_i, first)
                list_b.extend([pom])    
        list_c = ["".join(dummy_i) for dummy_i in list_b]
        list_c.extend(rest_strings)
        return list_c

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    try:
        opened_file = urllib2.urlopen(filename)
    except IOError as e:
        print 'Your scrabble words file is missing.'
     
    return [word[:-1] for word in opened_file]
    
def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
  
#import user36_YLM2lAYOPYukMqi as unit_test
#unit_test.test_remove_duplicates(remove_duplicates)
#unit_test.test_intersect(intersect)
#unit_test.test_merge(merge)
#unit_test.test_merge_sort(merge_sort)
#unit_test.test_gen_all_strings(gen_all_strings)   
