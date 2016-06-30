"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2
import matplotlib.pyplot as plt

if DESKTOP:
    import matplotlib.pyplot as plt
    import module4_project as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


def question1():
	human = read_protein(HUMAN_EYELESS_URL)
	fly = read_protein(FRUITFLY_EYELESS_URL)
	scoringmatrix = read_scoring_matrix(PAM50_URL)
	alignmentmatrix = student.compute_alignment_matrix(human, fly, scoringmatrix, False)
	score, align_x, align_y = student.compute_local_alignment(human, fly, scoringmatrix, alignmentmatrix)
	print score
	print align_x
	print align_y
	print len(align_x), len(align_y)

# question1()	

def question2():
	human = read_protein(HUMAN_EYELESS_URL)
	fly = read_protein(FRUITFLY_EYELESS_URL)
	scoringmatrix = read_scoring_matrix(PAM50_URL)
	pax = read_protein(CONSENSUS_PAX_URL)
	alignmentmatrix = student.compute_alignment_matrix(human, fly, scoringmatrix, False)
	score, align_x, align_y = student.compute_local_alignment(human, fly, scoringmatrix, alignmentmatrix)
	align_x2 = ""
	for item in align_x:
		if not item == '-':
			align_x2 += item 
	align_y2 = ""
	for item in align_y:
		if not item == '-':
			align_y2 += item 
	alignmentmatrix = student.compute_alignment_matrix(align_x2, pax, scoringmatrix, True)
	score3, align_x3, align_y3 = student.compute_global_alignment(align_x2, pax, scoringmatrix, alignmentmatrix)
	print align_x3
	print align_y3	
	print sum([align_x3[item] == align_y3[item] for item in range(len(align_x3))])/float(len(align_x3))
	
	alignmentmatrix = student.compute_alignment_matrix(align_y2, pax, scoringmatrix, True)
	score3, align_x3, align_y3 = student.compute_global_alignment(align_y2, pax, scoringmatrix, alignmentmatrix)
	print align_x3
	print align_y3	
	print sum([align_x3[item] == align_y3[item] for item in range(len(align_x3))])/float(len(align_x3))

# question2()

def question3():
	letters = "ACBEDGFIHKMLNQPSRTWVYXZ"
	human = [random.choice(letters) for item in range(133)]
	fly = [random.choice(letters) for item in range(133)]
	print human
	print fly
	scoringmatrix = read_scoring_matrix(PAM50_URL)
	pax = read_protein(CONSENSUS_PAX_URL)
	alignmentmatrix = student.compute_alignment_matrix(human, fly, scoringmatrix, False)
	score, align_x, align_y = student.compute_local_alignment(human, fly, scoringmatrix, alignmentmatrix)
	align_x2 = ""
	for item in align_x:
		if not item == '-':
			align_x2 += item 
	align_y2 = ""
	for item in align_y:
		if not item == '-':
			align_y2 += item 
	alignmentmatrix = student.compute_alignment_matrix(align_x2, pax, scoringmatrix, True)
	score3, align_x3, align_y3 = student.compute_global_alignment(align_x2, pax, scoringmatrix, alignmentmatrix)
	print align_x3
	print align_y3	
	print sum([align_x3[item] == align_y3[item] for item in range(len(align_x3))])/float(len(align_x3))
	
	alignmentmatrix = student.compute_alignment_matrix(align_y2, pax, scoringmatrix, True)
	score3, align_x3, align_y3 = student.compute_global_alignment(align_y2, pax, scoringmatrix, alignmentmatrix)
	print align_x3
	print align_y3	
	print sum([align_x3[item] == align_y3[item] for item in range(len(align_x3))])/float(len(align_x3))

# question3()

def generate_null_distribution(seq_x,seq_y, scoring_matrix, num_trials):
	scoring_distribution = dict()
	seq_x_copy = list(seq_x)
	for item in range(num_trials):
		print item
		rand_y = list(seq_y)
		random.shuffle(rand_y)
		alignmentmatrix = student.compute_alignment_matrix(seq_x_copy, rand_y, scoring_matrix, False)
		score, align_x, align_y = student.compute_local_alignment(seq_x_copy, rand_y, scoring_matrix, alignmentmatrix)
		if score in scoring_distribution:
			scoring_distribution[score]+=1
		else:
			scoring_distribution[score] = 1
	return scoring_distribution

def question4():	
	human = read_protein(HUMAN_EYELESS_URL)
	fly = read_protein(FRUITFLY_EYELESS_URL)
	scoringmatrix = read_scoring_matrix(PAM50_URL)
	slownik = generate_null_distribution(human, fly, scoringmatrix, 100)
	xvals = slownik.keys()
	yvals = [slownik[key]/100.0 for key in xvals]
	plt.bar(xvals, yvals)
	plt.xlabel('scores')  
	plt.ylabel('the fraction of total trials corresponding to each score') 
	plt.title('normalized version of the distribution') 
	plt.show()
	return slownik 
	
# slownik = question4()	
# print slownik

{39: 1, 41: 1, 42: 4, 43: 2, 44: 2, 45: 8, 46: 7, 47: 2, 48: 7, 49: 12, 50: 9, 51: 4, 52: 9, 53: 8, 54: 3, 55: 5, 56: 3, 57: 3, 58: 1, 59: 1, 60: 2, 61: 1, 62: 2, 67: 1, 69: 1, 81: 1}

q4_dict =  {39: 1, 41: 1, 42: 4, 43: 2, 44: 2, 45: 8, 46: 7, 47: 2, 48: 7, 49: 12, 50: 9, 51: 4, 52: 9, 53: 8, 54: 3, 55: 5, 56: 3, 57: 3, 58: 1, 59: 1, 60: 2, 61: 1, 62: 2, 67: 1, 69: 1, 81: 1}

def question5():
	keys = q4_dict.keys()
	values = q4_dict.values()
	nominator = sum([keys[i] * values[i] for i in range(len(keys))])
	mean = float(nominator) / sum(values)
	nominator = sum([(keys[i] - mean)**2 * values[i] for i in range(len(keys))])
	stddev = math.sqrt(float(nominator) / sum(values))
	human = read_protein(HUMAN_EYELESS_URL)
	fly = read_protein(FRUITFLY_EYELESS_URL)
	scoringmatrix = read_scoring_matrix(PAM50_URL)
	alignmentmatrix = student.compute_alignment_matrix(human, fly, scoringmatrix, False)
	score, align_x, align_y = student.compute_local_alignment(human, fly, scoringmatrix, alignmentmatrix)
	return score, mean, stddev

# print question5()

def question7():
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	sx = 'dgfvdsgvds'
	sy = 'fghgafdsgfadsgfv'
	zakres = range(-2)
	for idx in zakres:
		for idy in zakres:
			for idz in zakres:
				scoringmatrix = student.build_scoring_matrix(set(alphabet), idx, idy, idz)
				alignmentmatrix = student.compute_alignment_matrix(sx, sy, scoringmatrix, True)
				score, align_x, align_y = student.compute_global_alignment(sx, sy, scoringmatrix, alignmentmatrix)
				if len(sx) + len(sy) - score == 3:
					print idx, idy, idz
	scoringmatrix = student.build_scoring_matrix(set(alphabet), 2,1,0)
	alignmentmatrix = student.compute_alignment_matrix(sx, sy, scoringmatrix, True)
	score, align_x, align_y = student.compute_global_alignment(sx, sy, scoringmatrix, alignmentmatrix)
	return len(sx) + len(sy) - score
	
# print question7()

def check_spelling(checked_word, dist, word_list):
	out = []
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	for item in word_list:
		print item
		sx = checked_word
		sy = item
		scoringmatrix = student.build_scoring_matrix(set(alphabet), 2,1,0)
		alignmentmatrix = student.compute_alignment_matrix(sx, sy, scoringmatrix, True)
		score, align_x, align_y = student.compute_global_alignment(sx, sy, scoringmatrix, alignmentmatrix)
		if len(sx) + len(sy) - score <= dist:
			out.append(item)
	return out		

def question8():
	checked_word = 'firefly'
	word_list = read_words(WORD_LIST_URL)
	return check_spelling(checked_word, 2, word_list)

print question8()
