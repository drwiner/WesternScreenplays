import spacy
print('loading english')
nlp = spacy.load('en')


if __name__ == '__main__':

	print('reading')
	raw_doc = ''
	for line in open('combo.txt'):
		raw_doc += line
	doc = nlp(raw_doc)

	print('parsing')

	sw = open('stopwords.dat')
	stopwords = {wd.strip() for wd in sw}

	from collections import Counter
	tc = Counter([token.orth_ for token in doc if token.orth_ not in stopwords])
	mcw = open('most_common words', 'w')
	mcw.write(tc.most_common(1000))
	mcw.close()
	tc_verbs = Counter([token.orth_ for token in doc if token.pos_ == 'VERB' and token.orth_ not in stopwords])
	tc_nouns = Counter([token.orth_ for token in doc if token.pos_ == 'NOUN' and token.orth_ not in stopwords])
	tcv = open('most_common_verbs','w')
	tcv.write('\n'.join([str(t) for t in tc_verbs.most_common(1000)]))
	tcv.close()
	tcn = open('most_common_nouns', 'w')
	tcn.write('\n'.join([str(t) for t in tc_nouns.most_common(1000)]))
	tcn.close()