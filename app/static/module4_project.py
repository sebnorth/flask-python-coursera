def make_dict(keys, default_value):
    """
    Creates a new dictionary with the specified keys and default value.

    Arguments:
    keys          -- A list of keys to be included in the returned dictionary.
    default_value -- The initial mapping value for each key.

    Returns:
    A dictionary where every key is mapped to the given default_value.
    """
    result = { }

    for key in keys:
        result[key] = default_value
    
    return result

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
	"""
	asda
	"""
	alphabet_dashed = alphabet
	alphabet_dashed.add('-')
	characters = list(alphabet_dashed)
	slownik = make_dict(characters, 0)
	dict_list = [make_dict(characters, 0) for dummy in range(len(characters))]
	slownik = dict(zip(slownik, dict_list))
	for idx in slownik.keys():
		for idy in slownik[idx].keys():
			if idx == '-' or idy == '-':
				slownik[idx][idy] = dash_score
			elif idx == idy and not idx == '-':
				 slownik[idx][idy] = diag_score
			else:
				slownik[idx][idy] = off_diag_score 
	return slownik		

#build_scoring_matrix(set(['A', 'C', '-', 'T', 'G']), 6, 2, -4)
# print build_scoring_matrix(set(['A', 'C', '-', 'T', 'G']), 6, 2, -4)

def compute_flagtrue(seq_x, seq_y, macierz, scoring_matrix):
	"""
	asfasa
	"""
	rows = len(seq_x)
	cols = len(seq_y)
	for idx in range(1, rows + 1):
			macierz[idx][0] = macierz[idx - 1][0] + scoring_matrix[seq_x[idx-1]]['-']
	for idy in range(1, cols + 1):
		macierz[0][idy] = macierz[0][idy - 1] + scoring_matrix['-'][seq_y[idy - 1]]
	for idx in range(1, rows + 1):
		for idy in range(1, cols + 1):
			macierz[idx][idy] = max( macierz[idx - 1][idy - 1] + scoring_matrix[seq_x[idx-1]][seq_y[idy - 1]] ,macierz[idx - 1][idy] + scoring_matrix[seq_x[idx-1]]['-'],  macierz[idx][idy - 1] + scoring_matrix['-'][seq_y[idy - 1]])

def compute_flagfalse(seq_x, seq_y, macierz, scoring_matrix):
	"""
	asds
	"""
	rows = len(seq_x)
	cols = len(seq_y)
	for idx in range(1, rows + 1):
			macierz[idx][0] = macierz[idx - 1][0] + scoring_matrix[seq_x[idx-1]]['-']
			if macierz[idx][0] < 0:
				macierz[idx][0] = 0
	for idy in range(1, cols + 1):
		macierz[0][idy] = macierz[0][idy - 1] + scoring_matrix['-'][seq_y[idy - 1]]
		if macierz[0][idy] < 0:
			macierz[0][idy] = 0
	for idx in range(1, rows + 1):
		for idy in range(1, cols + 1):
			macierz[idx][idy] = max( macierz[idx - 1][idy - 1] + scoring_matrix[seq_x[idx-1]][seq_y[idy - 1]] ,macierz[idx - 1][idy] + scoring_matrix[seq_x[idx-1]]['-'],  macierz[idx][idy - 1] + scoring_matrix['-'][seq_y[idy - 1]])
			if macierz[idx][idy] < 0:
				macierz[idx][idy] = 0
	
def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
	"""
	asfasa
	"""
	rows = len(seq_x)
	cols = len(seq_y)
	macierz = [[0 for dummy_x in range(cols + 1)] for dummy_y in range(rows + 1)]
	# print macierz
	if global_flag:
		compute_flagtrue(seq_x, seq_y, macierz, scoring_matrix)
	else:
		compute_flagfalse(seq_x, seq_y, macierz, scoring_matrix)	
	return macierz				
	
# m = compute_alignment_matrix('ACTACT', 'AGCTA', {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1}, 'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1}, '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0}, 'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1}, 'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}, True) 

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	"""
	asdfas
	"""
	rows = len(seq_x)
	cols = len(seq_y)
	align_x = ""
	align_y = ""
	while not rows == 0 and not cols == 0:
		if alignment_matrix[rows][cols] == alignment_matrix[rows-1][cols-1] + scoring_matrix[seq_x[rows-1]][seq_y[cols - 1]]:
			align_x = seq_x[rows-1]+align_x
			align_y = seq_y[cols - 1]+align_y
			rows-=1
			cols-=1 
		elif alignment_matrix[rows][cols] == alignment_matrix[rows-1][cols] + scoring_matrix[seq_x[rows-1]]['-']:
			align_x = seq_x[rows-1]+align_x
			align_y = "-"+align_y
			rows-=1
		else:
			align_x =  "-"+align_x
			align_y = seq_y[cols - 1]+align_y
			cols-=1
	while not rows == 0:
		align_x = 	seq_x[rows-1] + align_x
		align_y = 	'-' + align_y
		rows-=1	
	while not cols == 0:
		align_x = 	'-' + align_x
		align_y = 	seq_y[cols-1] + align_y
		cols-=1		
	score = sum([scoring_matrix[align_x[idx]][align_y[idx]] for idx in range(len(align_x)) ])
	return (score, align_x, align_y)

def alignment_matrix_maximum(macierz):
	"""
	fdsfds
	"""
	rows = len(macierz)
	cols = len(macierz[0])
	max_value = max([macierz[idx][idy] for idx in range(rows) for idy in range(cols)])
	for idx in range(rows):
		for idy in range(cols): 
			if macierz[idx][idy] == max_value:
				return (idx, idy)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	"""
	saf
	"""
	largest_x, largest_y = alignment_matrix_maximum(alignment_matrix)
	rows = largest_x
	cols = largest_y
	align_x = ""
	align_y = ""
	while alignment_matrix[rows][cols]:
		if alignment_matrix[rows][cols] == alignment_matrix[rows-1][cols-1] + scoring_matrix[seq_x[rows-1]][seq_y[cols - 1]]:
			align_x = seq_x[rows-1]+align_x
			align_y = seq_y[cols - 1]+align_y
			rows-=1
			cols-=1 
		elif alignment_matrix[rows][cols] == alignment_matrix[rows-1][cols] + scoring_matrix[seq_x[rows-1]]['-']:
			align_x = seq_x[rows-1]+align_x
			align_y = "-"+align_y
			rows-=1
		else:
			align_x =  "-"+align_x
			align_y = seq_y[cols - 1]+align_y
			cols-=1 
	score = sum([scoring_matrix[align_x[idx]][align_y[idx]] for idx in range(len(align_x)) ])
	return (score, align_x, align_y)
