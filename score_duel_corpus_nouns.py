true_labels_file = open('duel_corpus_true_labels.txt')
true_labels_dict = {line.split()[0]: line.split()[1] for line in true_labels_file}
true_labels_file.close()
labeled_nouns_file = open('duel_corpus_output_coded.txt')
labeled_nouns = [line.split() for line in labeled_nouns_file]
labeled_nouns_file.close()



cat_labels = 'PERSON VEH LOC BPART WEAPON ITEM TIME'.split()
true_instances_dict = dict()
for cat in cat_labels:
	print(cat)
	with open('true_instances_lexicon//' + cat) as til:
		true_instances_dict[cat] = dict([line.split() for line in til])


def atrueinstance(wrd, cat):
	array_of_instances = true_instances_dict[cat]
	cat_dict = dict(array_of_instances)
	if cat_dict[wrd] == 1:
		return True
	else:
		return False

dc_est_file = open('duel_corpus_estimations','w')
dc_fnd_file = open('duel_corpus_founds','w')

import collections
est_correct = 0
est_total = 0
est_guesses_per_cat = collections.defaultdict(int)
est_correct_per_cat = collections.defaultdict(int)
est_actual_per_cat = collections.defaultdict(int)

found_correct = 0
found_total = 0
found_guesses_per_cat = collections.defaultdict(int)
found_correct_per_cat = collections.defaultdict(int)

for noun, label, discovery in labeled_nouns:
	if discovery == 'estimated' and true_labels_dict[noun] in cat_labels:
		actual_cat = true_labels_dict[noun]
		est_actual_per_cat[actual_cat] += 1
		dc_est_file.write('{}\t{}\t{}\n'.format(noun,label, actual_cat))

		if label == actual_cat:
			est_correct += 1
			est_correct_per_cat[label] += 1

		est_total += 1
		est_guesses_per_cat[label] += 1

	elif discovery == 'found':
		tid = dict(true_instances_dict[label])
		dc_fnd_file.write('{}\t{}\t{}\n'.format(noun, label, tid[noun]))

		if tid[noun] == '1':
			found_correct_per_cat[label] += 1
			found_correct += 1

		found_total += 1
		found_guesses_per_cat[label] += 1

dc_est_file.close()
dc_fnd_file.close()

print('estimations:\n')
if est_total > 0:
	print('total est {}'.format(est_total))
	print('percent correct est {}'.format(str(est_correct / est_total)))
	print('\n')
if found_total > 0:
	print('total found {}'.format(found_total))
	print('percent correct found {}'.format(str(found_correct / found_total)))

print('examine other things')
"""notes: for the estimated, we're only looking at items whose true category is one of the 7 collected.
Precision = percent of labels correct
Recall = percent of true instances of category correctly labeled.
"""