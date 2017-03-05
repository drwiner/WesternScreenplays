import spacy
print('loading english')
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

def dist_avg(wrd, wrd_list):
	dist_sum = 0
	for wd in wrd_list:
		dist_sum += cosine(wrd.vector, wd.vector)
	return dist_sum / len(wrd_list)

def sim(cat_words, pos_words, num_cutoff_per_word, shaving_number):
	cat_dict = dict()
	for cw in cat_words:
		try:
			pos_words.sort(key=lambda w: cosine(w.vector, cw.vector))
			pos_words.reverse()
			cndts = pos_words[:num_cutoff_per_word]
			cat_dict[cw.orth_] = [cndt.orth_ for cndt in cndts]
		except:
			continue

	total_words = set()
	running_words = set(cat_dict[cat_words[0].orth_])
	for cw, vals in cat_dict.items():
		running_words.intersection_update(vals)
		total_words.update(set(vals[:shaving_number]))

	return running_words.union(total_words)

# returns lexemes, rather than orth_
def sim2(cat_words, pos_words, num_cutoff_per_word, shaving_number):
	print('calculating similarities')
	cat_dict = dict()
	for cw in cat_words:
		try:
			pos_words.sort(key=lambda w: cosine(w.vector, cw.vector))
			pos_words.reverse()
			cndts = pos_words[:num_cutoff_per_word]
			# cndts in order of score
			cat_dict[cw.orth_] = cndts
		except:
			continue

	total_words = set()
	running_words = set(cat_dict[cat_words[0].orth_])
	for cw, vals in cat_dict.items():
		running_words.intersection_update(vals)
		total_words.update(set(vals[:shaving_number]))

	return running_words.union(total_words)

import operator

def sim3(cat_words, pos_words, num_cutoff_per_word):
	print('calculating similarities')
	noun_dict = dict()

	for noun in pos_words:
		try:
			noun_dict[noun] = sum(cosine(noun.vector, cw.vector) for cw in cat_words)
		except:
			continue

	sorted_nouns = list(reversed(sorted(noun_dict.items(), key=operator.itemgetter(1))))
	best_nouns = sorted_nouns[:num_cutoff_per_word]
	return [noun for noun, score in best_nouns]

def isGoodCndt(cndt, cat, other_cats):
	avg_sim = dist_avg(cndt, cat)
	for other_cat in other_cats:
		if dist_avg(cndt, other_cat) > avg_sim:
			return False
	return True


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

def makeBaseLineSeeds():
	return cats_dict

# v_expansion = set('leathers officiators concern .Dutch Redridge children Mac mob magazine warrior Everyone clerk Domino Tector Iles labor feather 11th stake Stellman em.back Bodyguard chances gunman bath'.split())
# expansion_words = getVocab(v_expansion)

all_nouns_file = open('all_nouns')
nouns = getVocab([w.split()[0] for w in all_nouns_file])
all_nouns_file.close()


def pairwiseCategory_topMembers(cats, freq_cutoff, shaving_adder=None):
	distinctive_words_per_cat = list()
	for cat in cats:

		# calculate noun - category similarities
		top_cat_words = sim3(cat, nouns, freq_cutoff)

		# remove other cats
		top_cat_list = list(top_cat_words)
		other_cats = list(cats)
		other_cats.remove(cat)

		binary_eval = [isGoodCndt(wrd, cat, other_cats) for wrd in top_cat_list]
		top_distinctive_words = [wrd for i, wrd in enumerate(top_cat_list) if binary_eval[i]]
		distinctive_words_per_cat.append(top_distinctive_words)

	return distinctive_words_per_cat, cat_labels


# find the most common nouns which are most similar to the category members, top 20-len(category_members)
def getDistinctiveWords_per_cat(freq_cutoff, shaver=None):

	distinctive_words_per_cat, c_labels = pairwiseCategory_topMembers(cats, freq_cutoff, shaver)
	for i, cat in enumerate(distinctive_words_per_cat):
		print('\n')
		print(cat_labels[i])
		print('\n')
		print(len(cat))
		print([t.orth_ for t in cat])
	return distinctive_words_per_cat, c_labels

from collections import defaultdict
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

import math

# words scored on the basis of patterns from Basilisk
def scoreWord(word, patterns):
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

		# find all instances of pattern in wep
		# find percentage of them which have word
		# record number

# rw2 = sim2(cat_words, nouns, 200, 20)
# print(rw)
# print(rw2)

# idea: check if any candidate is closer to original category than to


# for c in cat_words:
# 	num = 0
# 	for v in vocab_words:
# 		num += cosine(c.vector, v.vector)
# 	cat_dict[c.orth_] = num/len(vocab_words)
#
# print('getting all words')
# allWords = list({w for w in nlp.vocab if w.has_vector and w.orth_.islower() and w.lower_ not in category_members})
#
# print('adding cosines')
# # allWords.sort(key=lambda w: cosine(w.vector, nasa.vector))
#
# cat_dict = dict()
# for c in cat_words:
# 	try:
# 		allWords.sort(key=lambda w: cosine(w.vector, c.vector))
# 		allWords.reverse()
# 		cat_dict[c] = allWords[1:11]
# 		for word in allWords[:10]:
# 			print(c.orth_, word.orth_)
# 		print('\n')
# 	except:
# 		continue
#
# # for v in vocab_words:
# # 	num = 1
# # 	for c in allWords:
# # 		try:
# # 			num += cosine(c.vector, v.vector)
# # 		except:
# # 			continue
# # 		# num += cosine(c.vector, v.vector)
# # 	# voc_dict[v.orth_] = num/len(cat_words)
# # 	voc_dict[v.orth_] = num
#
# # import operator
# # vsort = reversed(sorted(voc_dict.items(), key=operator.itemgetter(1)))
# # print(vsort)
# print('ok')
