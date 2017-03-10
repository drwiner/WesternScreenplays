from os import listdir
from os.path import isfile, join

directory_with_lexicons = 'basilisk_baseline_lexicons//'
directory = 'true_instances_lexicon//'
cat_names = [f for f in listdir(directory) if isfile(join(directory, f))]

# true instances per cat
true_instances_per_cat = dict()

for cat in cat_names:
	cat_file = open(directory + cat)
	correct_in_cat = []
	total = 0
	for line in cat_file:
		sp = line.split()
		if len(sp) != 2:
			AssertionError('something wrong with line {}'.format(line))
			continue
		if int(sp[1]) == 1:
			correct_in_cat.append(sp[0].strip())
		total += 1
	cat_file.close()

	true_instances_per_cat[cat] = correct_in_cat

print('\n done baseline scoring')


for cat in cat_names:
	lexicon_file = open(directory_with_lexicons + cat + '-BILPTVW-diffScore.lexicon')
	print(cat)
	TI = true_instances_per_cat[cat]
	correct = 0
	unique = 0
	total = 0
	for line in lexicon_file:
		sp = line.split()
		if len(sp) != 2:
			AssertionError('something wrong with line {}'.format(line))
			continue
		if int(sp[1]) == 1:
			correct += 1
			if str(sp[0]) not in TI:
				unique += 1
		total += 1

	print('correct : {}, unique : {}'.format(correct, unique))
	print(correct / total)
	print('\n')
	lexicon_file.close()
