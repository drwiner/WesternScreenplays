import spacy
print('loading english')
nlp = spacy.load('en')


if __name__ == '__main__':

	raw_doc = ''
	for line in open('combo.txt'):
		sp = line.split()
		raw_doc += ' '.join(wrd.strip() for wrd in sp if wrd != '\n')
		raw_doc += ' '
	doc = nlp(raw_doc)

	print('parsing')

	sw = open('stopwords.dat')
	stopwords = {wd.strip() for wd in sw}

	from collections import Counter
	# tc = Counter([token.orth_ for token in doc if token.orth_ not in stopwords])
	# mcw = open('most_common words', 'w')
	# mcw.write(tc.most_common(1000))
	# mcw.close()
	tc_verbs = Counter([token.orth_ for token in doc if token.pos_ == 'VERB' and token.orth_ not in stopwords])
	tc_nouns = Counter([token.orth_ for token in doc if token.pos_ == 'NOUN' and token.orth_ not in stopwords])
	tcv = open('all_verbs','w')
	for t, c in tc_verbs.items():
		tcv.write(t + '\t' + str(c) + '\n')
	tcv.close()
	# tcv.write('\n'.join([str(t) for t in tc_verbs.most_common(1000)]))
	# tcv.close()
	tcn = open('all_nouns', 'w')
	for t, c in tc_nouns.items():
		tcn.write(t + '\t' + str(c) + '\n')
	tcn.close()
	# tcn.write('\n'.join([str(t) for t in tc_nouns.most_common(1000)]))
	# tcn.close()