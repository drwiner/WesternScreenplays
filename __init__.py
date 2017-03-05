import subprocess
from compareSeedsToOuput import getDistinctiveWords_per_cat, makeBaseLineSeeds, scoreWord

baseline_seeds = []
special_seeds = []

def makeSeedFile(label, cat):
	seed_file = open('seeds\\' + label.upper(), 'w')
	seed_file.write('\n'.join([seed.orth_ for seed in cat]))
	seed_file.close()

def makeBaselineSeeds():
	cats_dict = makeBaseLineSeeds()
	for cat_name, cat_list in cats_dict.items():
		makeSeedFile(cat_name, cat_list)

	return cats_dict.keys()

def makeSeedLists(freq):
	distinctive_words_per_cat, cat_labels = getDistinctiveWords_per_cat(freq)
	for i, cat in enumerate(distinctive_words_per_cat):
		makeSeedFile(cat_labels[i], cat)

	return cat_labels

def readPattern(pattern_file_name):
	pfn = open(pattern_file_name)
	pattern_dict = {line.split()[0]: line.split()[2] for line in pfn}
	pfn.close()
	return pattern_dict

if __name__ == '__main__':

	base = False
	semantic = True
	experiment = False
	cutoffs = [200, 400]
	thresholds = [0.4, 0.6]

	if base:
		baseline_list = makeBaselineSeeds()

		bsl = open('baseline-seeds-list.txt', 'w')
		bsl.write('seeds/\n')
		bsl.write('\n'.join([label.upper() for label in baseline_list]))
		bsl.close()

		command = 'java -jar BASILISK2.0.jar baseline-seeds-list.txt Western.extractionpattern stopwords.dat -n 1 -o baseline_output\ -t'
		print(command)
		subprocess.call(command, shell=True)
	else:
		baseline_list = makeBaseLineSeeds().keys()

	if semantic:
		# distinctive_words_per_cat, cat_labels = getDistinctiveWords_per_cat(500)
		# cat_dict = dict(zip(cat_labels, distinctive_words_per_cat))
		cat_list = makeSeedLists(500)
		sl = open('seeds-list.txt', 'w')
		sl.write('seeds/\n')
		sl.write('\n'.join([label.upper() for label in cat_list]))
		sl.close()


		command = 'java -jar BASILISK2.0.jar seeds-list.txt Western.extractionpattern stopwords.dat -n 1 -o basilisk_output\ -t'
		print(command)
		subprocess.call(command, shell=True)



	if experiment:
		# threshold_score = 0.2
		pattern_file_names = ['baseline_output/' + label.upper() + '.patterns' for label in baseline_list]
		patterns = [readPattern(pfn) for pfn in pattern_file_names]
		best_patterns = [[[p for p, v in p_dict.items() if float(v) >= th] for p_dict in patterns] for th in thresholds]
		distinctive_words_per_cat_per_cutoff = []

		from collections import defaultdict

		for cutoff in cutoffs:
			distinctive_words_per_cat, cat_labels = getDistinctiveWords_per_cat(cutoff)
			cat_dict = dict(zip(cat_labels, distinctive_words_per_cat))
			distinctive_words_per_cat_per_cutoff.append(cat_dict)

			# cut_off_dict = defaultdict(list)
			for i, (cat_name, cat_words) in enumerate(cat_dict.items()):
				print('\n')
				print(cat_name)
				print('_________')

				for j, bp in enumerate(best_patterns):
					exp_name = 'ExpWords_cat' + str(cat_name) + '_cutoff' + str(cutoff) + '_thresh' + str(thresholds[j]) + '.txt'
					catname_cutoff_file = open(exp_name, 'w')

					for wrd in cat_words:
						sw = scoreWord(wrd.orth_, bp[i])
						if sw > 0:
							# cut_off_dict[cat_name].append(wrd.orth_, sw)
							catname_cutoff_file.write(wrd.orth_ + '\n')
							print(wrd.orth_, sw)

					catname_cutoff_file.close()


	# 4 - score each word, print them in sorted order




	# then, compare performanc