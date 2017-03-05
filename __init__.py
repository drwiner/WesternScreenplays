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

def makeSeedLists():
	distinctive_words_per_cat, cat_labels = getDistinctiveWords_per_cat()
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
	semantic = False


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
		distinctive_words_per_cat, cat_labels = getDistinctiveWords_per_cat()
		cat_dict = dict(zip(cat_labels, distinctive_words_per_cat))
		cat_list = makeSeedLists()
		sl = open('seeds-list.txt', 'w')
		sl.write('seeds/\n')
		sl.write('\n'.join([label.upper() for label in cat_list]))
		sl.close()


		command = 'java -jar BASILISK2.0.jar seeds-list.txt Western.extractionpattern stopwords.dat -n 1 -o basilisk_output\ -t'
		print(command)
		subprocess.call(command, shell=True)

	threshold_score = 0.2
	pattern_file_names = ['baseline_output/' + label.upper() + '.patterns' for label in baseline_list]
	patterns = [readPattern(pfn) for pfn in pattern_file_names]
	best_patterns = [[p for p, v in p_dict.items() if float(v) >= threshold_score] for p_dict in patterns]

	distinctive_words_per_cat, cat_labels = getDistinctiveWords_per_cat(200)
	cat_dict = dict(zip(cat_labels, distinctive_words_per_cat))

	for i, (cat_name, cat_words) in enumerate(cat_dict.items()):
		print('\n')
		print(cat_name)
		print('_________')
		for wrd in cat_words:
			sw = scoreWord(wrd.orth_, best_patterns[i])
			if sw > 0:
				print(wrd.orth_, sw)


	# 4 - score each word, print them in sorted order




	# then, compare performanc