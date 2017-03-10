David Winer's Basic IE System

input_file - content
--------------
combo.txt - Western Screenplay Corpus (WSC) cleaned in one file
western.parse - CoNLL format parsing of WSC
western.extractionpattern - input parse file for Basilisk
baseline-seeds-list.txt - path and seed file names
all_nouns - all nouns in WSC
all_nouns_duel_corpus - all nouns in duel corpus
stopwords.dat - stop words for parsing
duel_corpus_true_labels.txt - manually labeled classes of duel corpus estimates


folders - content
--------------
true_instance_lexicon - 600 cutoff no rlogf threshold filter output, manually labeled as correct or not
exp_200_400_600_0_0.1_0.5 - experimental output
baseline_output - the lexicon and patterns from running Basilisk 5 iterations with baseline seeds
seeds - seed files for Basilisk
movies - individual movie text (10 movies in WSC), combined into single document 'combo.txt', originally from imsdb.

python_file - content
--------------
__init__.py - master file for running basilisk or running experiments
semantic_induction.py - has all the system component functions
parseWCS.py - combines movie files and parses them into CoNLL output
extractionFormatConvertor.py - modified from https://github.com/haibonlp/basilisk to prepare patterns for Basilisk
score_basilisk_lexicon_results.py - compiles statistics for manually labeled basilisk output and compares to true-instance-lexicon to calculate intersection
label_duel_corpus_nouns.py - labels found duel corpus nouns and gives labels to words not found via similarity.
score_duel_corpus_nouns.py - uses the labels above to score
score_lexicon_results.py - scores the experimental lexicons based on true instance lexicon labels 

output_file - content
------------
scoring - experimental conditions output file
duel_corpus_founds - words in duel corpus nouns found in best f-score experimental lexicons
duel_corpus_estimates - words in duel corpus nouns not found in f-score experimental lexicons
duel_corpus_baseline_output.txt - estimated/found labels using only baseline seeds as lexicon
duel_corpus_output.txt - estimated/found labels using best- f-score lexcions


David Winer drwiner@cs.utah.edu