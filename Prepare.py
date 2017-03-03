import spacy
print('loading english')
nlp = spacy.load('en')

# 10 movie names
movie_names = 'BadDayatBlackRock BookofEli,The DanceswithWolves Mariachi,El Roughshod StationWest TallintheSaddle TrueGrit WildBunch,The WildWildWest'.split()

def joinMovies(movie_names, combo_name):
	print('joining movies')
	cn = open(combo_name, 'w')
	for movie in movie_names:
		mn = open(movie)
		cn.writelines(mn)
		cn.write('\n')
	cn.close()

def pretab(wrd):
	return '\t' + wrd
def suftab(wrd):
	return wrd + '\t'

if __name__ == '__main__':
	combo_name = 'combo.txt'
	fnt = open('file_names.txt').readlines()

	if combo_name + '\n' not in fnt:
		joinMovies(movie_names, combo_name)

	print('reading')
	raw_doc = ''
	for line in open(combo_name):
		raw_doc += line
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
			parsed_line += suftab('_') + suftab(str(token.i)) + suftab(token.dep_) + '_\t_\n'
