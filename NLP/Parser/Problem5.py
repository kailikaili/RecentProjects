
# Problem 5
# This file is used to record the procedure of Problem 5
# CKY Parser implementation
# file 'cky_parser.py'

# counting nonterminals, unary_rules, binary_rules
python count_cfg_freqs.py parse_train.dat > cfg.counts
#replacing the rare terminals by _RARE_
python replace.py cfg.counts parse_train.dat parse_new_train.dat
# recount the replaced traing data
python count_cfg_freqs.py parse_new_train.dat > new_cfg.counts

# Do CKY parser
# python ckyparser.py count_file input_sentences_file out_put_file
python cky_parser.py new_cfg.counts parse_dev.dat res.tree

# evaluation
python eval_parser.py parse_dev.key res.tree
