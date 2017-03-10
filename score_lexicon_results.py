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
	if total > 0:
		baseline_avg = len(correct_in_cat) / total
	else:
		baseeline_avg = 0
	output_file.write(cat + '\n')
	output_file.write('total: {}\n'.format(total))
	output_file.write('num_correct: {}\n'.format(str(len(correct_in_cat))))
	output_file.write('baseline_avg: {}\n\n'.format(str(baseline_avg)))

print('\n done baseline scoring')

# now, read results from experiment

directory = 'exp_200_400_600_0_0.1_0.5//'
exp_names = [f for f in listdir(directory) if isfile(join(directory, f))]

# based on order that output files are listed by directory
cuts = ([200,200,200, 400,400,400,600,600,600])*7
cuts = ([200 for i in range(3)] + [400 for i in range(3)] + [600 for i in range(3)])*7
ths = ([0.1, 0.5, 0])*21
cats = [cat for cat in cat_names for i in range(9)]

# need the 'i' to index conditions (cuts, ths, and cats)
for i, exp in enumerate(exp_names):
	exp_file = open(directory + exp)
	cat = cats[i]
	cut = cuts[i]
	th = ths[i]
	true_instances = true_instances_per_cat[cat]
	correct = 0
	total = 0
	for line in exp_file:
		wrd = line.split()[0].strip()
		if wrd in true_instances:
			correct +=1
		total +=1
	exp_file.close()

	output_file.write('{}\t{}\t{}'.format(cat, cut, th))
	# output_file.write('total: {}\n'.format(total))
	# output_file.write('num_correct: {}\n'.format(str(correct)))
	if len(true_instances) == 0:
		recall = 0
	else:
		recall = correct / len(true_instances)
	output_file.write('\t{}'.format(total))
	output_file.write('\t{}'.format(str(recall)))
	if total == 0:
		precision = 0
	else:
		precision = correct / total
	output_file.write('\t{}'.format(str(precision)))
	if recall + precision == 0:
		fscore = 0
	else:
		fscore = (recall * precision * 2) / (recall + precision)
	output_file.write('\t{}\n'.format(str(fscore)))


output_file.close()