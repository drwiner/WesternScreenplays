from os import listdir
from os.path import isfile, join

directory = 'true_instances_lexicon//'
cat_names = [f for f in listdir(directory) if isfile(join(directory, f))]

output_file = open('scoring', 'w')

output_file.write('baseline_acc\n')

# true instances per cat
true_instances_per_cat = dict()

for cat in cat_names:
	cat_file = open(directory + cat)
	correct_in_cat = []
	total = 0
	for line in cat:
		sp = line.split()
		if len(sp) != 2:
			AssertionError('something wrong with line {}'.format(line))
			continue
		if int(sp[1]) == 1:
			correct_in_cat.append(sp[0].strip())
		total += 1
	cat_file.close()
	true_instances_per_cat[cat] = correct_in_cat
	baseline_avg = len(correct_in_cat) / total
	output_file.write(cat + '\n')
	output_file.write('total: {}\n'.format(total))
	output_file.write('num_correct: {}\n'.format(str(len(correct_in_cat))))
	output_file.write('baseline_avg: {}\n\n'.format(str(baseline_avg)))

print('\n done baseline scoring')

# now, read results from experiment

directory = 'exp_200_400_600_0_0.1_0.5//'
exp_names = [f for f in listdir(directory) if isfile(join(directory, f))]

for exp in exp_names:
	exp_file = open(directory + exp)
	for line in exp_file:

	exp_file.close()

output_file.close()