import spacy
nlp = spacy.load('en')
from numpy import dot
from numpy.linalg import norm

def cosine(v1, v2):
	return dot(v1,v2)/(norm(v1) * norm(v2))

seed_dir = 'seeds//'

def getVocab(vocab_list):
	v_vocab = []
	for v in vocab_list:
		try:
			v_vocab.append(nlp.vocab[v])
		except:
			continue
	return [v for v in v_vocab if v.has_vector and v.orth_.islower()]

def sim(cat_words, pos_words, num_cutoff_per_word):
	cat_dict = dict()
	for cw in cat_words:
		try:
			pos_words.sort(key=lambda w: cosine(w.vector, cw.vector))
			pos_words.reverse()
			cndts = pos_words[:num_cutoff_per_word]
			cat_dict[cw.orth_] = [cndt.orth_ for cndt in cndts]
		except:
			continue
	running_words = set(cat_dict[cat_words[0].orth_])
	for cw, vals in cat_dict.items():
		running_words.intersection_update(vals)
	return running_words


category_members = set(
		'man girl boy woman crowd people soldier rider engineer sergeant liutenant driver'.split())
cat_words = getVocab(category_members)

# v_expansion = set('leathers officiators concern .Dutch Redridge children Mac mob magazine warrior Everyone clerk Domino Tector Iles labor feather 11th stake Stellman em.back Bodyguard chances gunman bath'.split())
# expansion_words = getVocab(v_expansion)

all_nouns_file = open('all_nouns')
nouns = getVocab([w.split()[0] for w in all_nouns_file])
all_nouns_file.close()

# find the most common nouns which are most similar to the category members, top 20-len(category_members)
rw = sim(cat_words, nouns, 200)
print(rw)



for c in cat_words:
	num = 0
	for v in vocab_words:
		num += cosine(c.vector, v.vector)
	cat_dict[c.orth_] = num/len(vocab_words)

print('getting all words')
allWords = list({w for w in nlp.vocab if w.has_vector and w.orth_.islower() and w.lower_ not in category_members})

print('adding cosines')
# allWords.sort(key=lambda w: cosine(w.vector, nasa.vector))

cat_dict = dict()
for c in cat_words:
	try:
		allWords.sort(key=lambda w: cosine(w.vector, c.vector))
		allWords.reverse()
		cat_dict[c] = allWords[1:11]
		for word in allWords[:10]:
			print(c.orth_, word.orth_)
		print('\n')
	except:
		continue

# for v in vocab_words:
# 	num = 1
# 	for c in allWords:
# 		try:
# 			num += cosine(c.vector, v.vector)
# 		except:
# 			continue
# 		# num += cosine(c.vector, v.vector)
# 	# voc_dict[v.orth_] = num/len(cat_words)
# 	voc_dict[v.orth_] = num

# import operator
# vsort = reversed(sorted(voc_dict.items(), key=operator.itemgetter(1)))
# print(vsort)
print('ok')





def dist_avg(seed, seed_list):
	dist_sun = 0
	for sd in seed_list:
		dist_sun += sd.vector



def getCluster(cluster_name):
	sd = open(seed_dir + cluster_name)
	cluster_avgs = dist_avg([line.strip() for line in sd])
