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

##########################################################################
# Methods
##########################################################################

def cosine(v1, v2):
	return dot(v1,v2)/(norm(v1) * norm(v2))

def sim(wrd, wrd_list):
	dist_sum = 0
	for wd in wrd_list:
		dist_sum += cosine(wrd.vector, wd.vector)
	return dist_sum / len(wrd_list)

def getVocab(vocab_list):
	"""

	:param vocab_list: expects spacy tokens
	:return: GloVe tokens
	"""
	v_vocab = []
	for v in vocab_list:
		try:
			v_vocab.append(nlp.vocab[v])
		except:
			continue
	return [v for v in v_vocab if v.has_vector and v.orth_.islower()]


##########################################################################
# Duel corpus nouns
duel_nouns = open('all_nouns_duel_corpus.txt')
duelwords ={dn.strip() for dn in duel_nouns}
duel_nouns.close()
##########################################################################
# Experimental Lexicons per Category (best-fscore cutoff and threshold used)
##########################################################################
exp_directory = 'exp_200_400_600_0_0.1_0.5//'

bpart_file = open(exp_directory+'ExpWords_catBPART_cutoff200_thresh0.txt')
bparts = [line.strip() for line in bpart_file]
bpart_file.close()

item_file = open(exp_directory+'ExpWords_catITEM_cutoff600_thresh0.txt')
items = [line.strip() for line in item_file]
item_file.close()

loc_file = open(exp_directory+'ExpWords_catLOC_cutoff400_thresh0.txt')
locations = [line.strip() for line in loc_file]
loc_file.close()

person_file = open(exp_directory+'ExpWords_catPERSON_cutoff600_thresh0.txt')
persons = [line.strip() for line in person_file]
person_file.close()

vehicle_file = open(exp_directory+'ExpWords_catVEH_cutoff200_thresh0.txt')
vehicles = [line.strip() for line in vehicle_file]
vehicle_file.close()

weapon_file = open(exp_directory+'ExpWords_catWEAPON_cutoff200_thresh0.txt')
weapons = [line.strip() for line in weapon_file]
weapon_file.close()

time_file = open(exp_directory+'ExpWords_catTIME_cutoff200_thresh0.txt')
timewords = [line.strip() for line in time_file]
time_file.close()

cats = [bparts, items, locations, persons, vehicles, weapons, timewords]
cats = [getVocab(cat) for cat in cats]
cat_labels = 'BPART ITEM LOC PERSON VEH WEAPON TIME'.split()
exp_cat_dict = dict(zip(cat_labels, cats))
##########################################################################

##########################################################################
# Baseline Seed words used as point of comparison, use similarity metric only
##########################################################################

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

# also import named entities, but later

# exp-cat_dict = wcs_nouns_per_cat
# cats_dict =

# duelwords

conglomo_wrds = set()
for cat in exp_cat_dict.values():
	for wrd in cat:
		conglomo_wrds.add(wrd.orth_)

noun_cats_dict = dict()
found_bool_dict = dict()

total_found = 0
for noun_unsplit in duelwords:
	nsp = noun_unsplit.split()
	noun = nsp[0]
	nn = nlp.vocab[noun]
	if not nn.orth_.islower() or not nn.has_vector:
		continue
	if noun in conglomo_wrds:
		for c_name, cat in exp_cat_dict.items():
			if noun in cat:
				noun_cats_dict[noun] = c_name
				found_bool_dict[noun] = 'found'
				total_found += 1
	else:
		max_sim = 0
		best_cat = None
		for c_name, cat in exp_cat_dict.items():
			nlp_noun = nlp.vocab[noun]
			delta = sim(nn, cat)
			if delta > max_sim:
				max_sim = delta
				best_cat = c_name
		if best_cat is None:
			AssertionError("best_cat is None")
		else:
			noun_cats_dict[noun] = best_cat
			found_bool_dict[noun] = 'estimated'
print(total_found / len(duelwords))

total_found = 0
baseline_dict = dict()
baseline_found_dict = dict()
for noun_unsplit in duelwords:
	nsp = noun_unsplit.split()
	noun = nsp[0]
	nn = nlp.vocab[noun]
	if not nn.orth_.islower() or not nn.has_vector:
		continue
	if noun in conglomo_wrds:
		for c_name, cat in cats_dict.items():
			if noun in cat:
				baseline_dict[noun] = c_name
				baseline_found_dict[noun] = 'found'
				total_found += 1
	else:
		max_sim = 0
		best_cat = None
		for c_name, cat in exp_cat_dict.items():
			nlp_noun = nlp.vocab[noun]
			delta = sim(nn, cat)
			if delta > max_sim:
				max_sim = delta
				best_cat = c_name
		if best_cat is None:
			AssertionError("best_cat is None")
		else:
			baseline_dict[noun] = best_cat
			baseline_found_dict[noun] = 'estimated'
print(total_found / len(duelwords))

duel_corpus_output = open('duel_corpus_output.txt', 'w')
duel_corpus_baseline_output = open('duel_corpus_baseline_output.txt', 'w')
for noun, cat in noun_cats_dict.items():
	duel_corpus_output.write('{}\t{}\t{}\n'.format(noun, cat, found_bool_dict[noun]))
for noun, cat in baseline_dict.items():
	duel_corpus_baseline_output.write('{}\t{}\t{}\n'.format(noun, cat, baseline_found_dict[noun]))
duel_corpus_output.close()
duel_corpus_baseline_output.close()
