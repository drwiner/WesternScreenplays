import spacy
print('loading english')
nlp = spacy.load('en')

# 10 movie names
movie_names = 'BadDayatBlackRock BookofEli,The DanceswithWolves Mariachi,El Roughshod StationWest TallintheSaddle TrueGrit WildBunch,The WildWildWest'.split()

def joinMovies(movie_names, combo_name):
	print('joining movies')
	cn = open(combo_name, 'w')
	for movie in movie_names:
		mn = open('movies\\' + movie)
		for line in mn:
			if line == '\n':
				continue
			cn.write(line)
		cn.write('\n')
		mn.close()
	cn.close()

def pretab(wrd):
	return '\t' + wrd
def suftab(wrd):
	return wrd + '\t'

if __name__ == '__main__':
	# run this script to create dependency parse.
	combo_name = 'combo.txt'
	# joinMovies(movie_names, combo_name)

	# # create combo.txt if not found in filenames
	# fnt = open('file_names.txt').readlines()
	# if combo_name + '\n' not in fnt:
	# 	joinMovies(movie_names, combo_name)

	print('reading')
	raw_doc = ''
	for line in open(combo_name):
		sp = line.split()
		raw_doc += ' '.join(wrd.strip() for wrd in sp if wrd != '\n')
		raw_doc += ' '
	doc = nlp(raw_doc)
	# print('nlp-ing')
	# for proc in nlp.pipeline:
	# 	proc(doc)

	print('parsing')
	output = open('western.parse', 'w')
	sents = []
	for span in doc.sents:
		sents.append([doc[i] for i in range(span.start, span.end)])


	for sent in sents:
		for i, token in enumerate(sent):
			parsed_line = suftab(str(i+1)) + suftab(token.orth_) + suftab('_') + suftab(token.pos_) + suftab(token.pos_)
			parsed_line += suftab('_') + suftab(str(sent.index(token.head)+1)) + suftab(token.dep_) + '_\t_\n'
			output.write(parsed_line)
		output.write('\n')