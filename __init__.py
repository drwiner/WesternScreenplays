import subprocess
from semantic_induction import update, fit, makeBaseLineSeeds

baseline_seeds = []
special_seeds = []

# CUTOFFS = [500, 200, 200, 400, 400]
# THRESHOLDS = [0, .4, .6, .4, .6]

CUTOFFS = [200, 400, 600]
THRESHOLDS = [0, 0.1, 0.5]

APPROX = 600

#############################################################
""" seed and pattern reading and loading """
def makeSeedFile(label, cat):
	seed_file = open('seeds\\' + label.upper(), 'w')
	seed_file.write('\n'.join([seed.orth_ for seed in cat]))
	seed_file.close()

def makeBaselineSeeds():
	cats_dict = makeBaseLineSeeds()
	for cat_name, cat_list in cats_dict.items():
		makeSeedFile(cat_name, cat_list)

	return cats_dict.keys()

def makeSeedLists(distinctive_words_per_cat, cat_labels):
	for i, cat in enumerate(distinctive_words_per_cat):
		makeSeedFile(cat_labels[i], cat)
	return

def readPattern(pattern_file_name):
	pfn = open(pattern_file_name)
	pattern_dict = {line.split()[0]: line.split()[2] for line in pfn}
	pfn.close()
	return pattern_dict
##############################################################


import sys
if __name__ == '__main__':

	try:
		base = bool(int(sys.argv[1]))
		semantic = bool(int(sys.argv[2]))
		experiment = bool(int(sys.argv[3]))
	except:
		# score patterns on baseline seeds
		base = True
		# score patterns with update seeds
		semantic = False
		# run update conditions
		experiment = True

	print('args:[base:\'' + str(int(base)) + ', sem:' + str(int(semantic)) + ', exp:' + str(int(experiment)) + '\']')

	# write baseline seeds and score patterns
	if base:
		baseline_list = makeBaselineSeeds()

		bsl = open('baseline-seeds-list.txt', 'w')
		bsl.write('seeds/\n')
		bsl.write('\n'.join([label.upper() for label in baseline_list]))
		bsl.close()

		# score patterns
		command = 'java -jar BASILISK2.0.jar baseline-seeds-list.txt Western.extractionpattern stopwords.dat -n 1 -o baseline_output\ -t'
		print(command)
		subprocess.call(command, shell=True)
	else:
		# load category names
		baseline_list = makeBaseLineSeeds().keys()

	# write updated seeds and score patterns
	if semantic:
		# Update
		candts, cat_list = update(APPROX)
		makeSeedLists(candts, cat_list)


		sl = open('seeds-list.txt', 'w')
		sl.write('seeds/\n')
		sl.write('\n'.join([label.upper() for label in cat_list]))
		sl.close()


		command = 'java -jar BASILISK2.0.jar seeds-list.txt Western.extractionpattern stopwords.dat -n 5 -o basilisk_output\ -t'
		print(command)
		subprocess.call(command, shell=True)



	if experiment:
		# load baseline patterns
		pattern_file_names = ['baseline_output/' + label.upper() + '.patterns' for label in baseline_list]
		patterns = [readPattern(pfn) for pfn in pattern_file_names]

		# patterns above threshold are best_patterns
		best_patterns = [[[p for p, v in p_dict.items() if float(v) >= th] for p_dict in patterns] for th in THRESHOLDS]
		distinctive_words_per_cat_per_cutoff = []

		# from collections import defaultdict

		for cutoff in CUTOFFS:
			distinctive_words_per_cat, cat_labels = update(cutoff)
			cat_dict = dict(zip(cat_labels, distinctive_words_per_cat))
			distinctive_words_per_cat_per_cutoff.append(cat_dict)

			# cut_off_dict = defaultdict(list)
			for i, (cat_name, cat_words) in enumerate(cat_dict.items()):
				print('\n')
				print(cat_name)
				print('_________')

				for j, bp in enumerate(best_patterns):
					exp_name = 'ExpWords_cat' + str(cat_name) + '_cutoff' + str(cutoff) + '_thresh' + str(THRESHOLDS[j]) + '.txt'
					catname_cutoff_file = open(exp_name, 'w')

					for wrd in cat_words:
						# measure fit of word with best patterns
						sw = fit(wrd.orth_, bp[i])
						if sw > 0:
							# cut_off_dict[cat_name].append(wrd.orth_, sw)
							catname_cutoff_file.write(wrd.orth_ + '\n')
							print(wrd.orth_, sw)

					catname_cutoff_file.close()
