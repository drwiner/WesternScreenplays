print('loading spacy')
import spacy

print('loading english')
nlp = spacy.load('en')

print('loading numpy')
from numpy import dot
from numpy.linalg import norm

import operator
from collections import defaultdict
import math

def getVocab(vocab_list):
	v_vocab = []
	for v in vocab_list:
		try:
			v_vocab.append(nlp.vocab[v])
		except:
			continue
	return [v for v in v_vocab if v.has_vector and v.orth_.islower()]

print('loading all_nouns previously extracted from western screenplay corpus')
all_nouns_file = open('all_nouns')
nouns = getVocab([w.split()[0] for w in all_nouns_file])
all_nouns_file.close()

print('loading seeds for each category')

# initial seeds for each category
persons = set('man girl boy woman crowd people soldier rider engineer sergeant liutenant driver'.split())
person_words = getVocab(persons)

vehicles = set('horses wagon car cars jeep train mules horse pony truck'.split())
veh_words = getVocab(vehicles)

locations = set('road street room bank house village porch town building bar camp'.split())
loc_words = getVocab(locations)

bodyparts = set('eyes eye hand head feet foot fingers mouth body face arm shoulder leg neck'.split())
bpart_words = getVocab(bodyparts)

weapons = set('gun guns knife sword arrow pistol rifle rifles revolver shotgun weapon weapons'.split())
weapon_words = getVocab(weapons)

items = set('door fire table chair glass bottle cigarette rope phone saddle pipe drink money book'.split())
item_words = getVocab(items)

timewords = set('moment time before after again starts slowly stops begins night'.split())
time_words = getVocab(timewords)

cats = [person_words, veh_words, loc_words, bpart_words, weapon_words, item_words, time_words]
cat_labels = 'PERSON VEH LOC BPART WEAPON ITEM TIME'.split()
cats_dict = dict(zip(cat_labels, cats))

print('loading patterns previously extracted from western screenplay corpus')
wep = open('western.extractionpattern')
western_pattern_dict = defaultdict(set)
word_instances = []
pattern_instances = []
for line in wep:
	lsplit = line.split()
	western_pattern_dict[lsplit[0].strip()].add(lsplit[2])
	word_instances.append(lsplit[0])
	pattern_instances.append(lsplit[2])
wep.close()


def cosine(v1, v2):
	return dot(v1,v2)/(norm(v1) * norm(v2))


def sim(wrd, wrd_list):
	dist_sum = 0
	for wd in wrd_list:
		dist_sum += cosine(wrd.vector, wd.vector)
	return dist_sum / len(wrd_list)


def cutoff(cat_words, seeds, num_cutoff_per_word):
	print('calculating similarities')
	noun_dict = dict()

	for noun in seeds:
		try:
			noun_dict[noun] = sum(cosine(noun.vector, cw.vector) for cw in cat_words)
		except:
			continue

	sorted_nouns = list(reversed(sorted(noun_dict.items(), key=operator.itemgetter(1))))
	best_nouns = sorted_nouns[:num_cutoff_per_word]
	return [noun for noun, score in best_nouns]


def disfilter(cndt, cat, other_cats):
	avg_sim = sim(cndt, cat)
	for other_cat in other_cats:
		if sim(cndt, other_cat) > avg_sim:
			return False
	return True


def makeBaseLineSeeds():
	return cats_dict


def update(freq_cutoff):

	distinctive_words_per_cat = list()
	for cat in cats:

		# calculate noun - category similarities
		top_cat_words = cutoff(cat, nouns, freq_cutoff)

		# remove other cats -> C \ {c}
		top_cat_list = list(top_cat_words)
		other_cats = list(cats)
		other_cats.remove(cat)

		#
		binary_eval = [disfilter(wrd, cat, other_cats) for wrd in top_cat_list]
		top_distinctive_words = [wrd for i, wrd in enumerate(top_cat_list) if binary_eval[i]]
		distinctive_words_per_cat.append(top_distinctive_words)

	for i, cat in enumerate(distinctive_words_per_cat):
		print('\n')
		print(cat_labels[i])
		print('\n')
		print(len(cat))
		print([t.orth_ for t in cat])

	return distinctive_words_per_cat, cat_labels


def fit(word, patterns):
	""" words scored on the basis of patterns (FIT) """
	# simplified in paper (it's just used to determine if word is extracted by at least one pattern in patterns)

	if word not in western_pattern_dict.keys():
		return 0
	pat_values = []
	for pattern in patterns:
		if pattern not in western_pattern_dict[word]:
			continue
		p_instances = [pat for i, pat in enumerate(pattern_instances) if word_instances[i] == word and pat == pattern]
		log_score = math.log2(len(p_instances) + 1)
		pat_values.append(log_score)
	if len(pat_values) > 0:
		return float(sum(pat_values) / len(pat_values))
	return 0