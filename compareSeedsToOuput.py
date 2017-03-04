import spacy
nlp = spacy.load('en')

seed_dir = 'seeds//'

cluster_avgs = dict()

# gather all known words, take only the lowercased versions
category_members = set('man girl boy men women woman crowd people he she soldier rider engineer sergeant liutenant driver'.split())
allWords = list({w for w in nlp.vocab if w.has_vector and w.orth_.islower() and w.lower_ not in category_members})

# read external words to compare
vocab_words = []
for w in allWords:
	pass

def dist_avg(seed, seed_list):
	dist_sun = 0
	for sd in seed_list:
		dist_sun += sd.vector

def getCluster(cluster_name):
	sd = open(seed_dir + cluster_name)
	cluster_avgs = dist_avg([line.strip() for line in sd])
