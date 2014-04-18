
# Problem 6
# This file is used to record the precedure of Problem6
# CKY Parser implementation
# file 'cky_parser.py'

# counting nonterminals, unary rules, binary rules
python count_cfg_freqs.py parse_train_vert.dat > cfg_vert.counts

# replacing the rare terminals by _RARE_
python replace.py cfg_vert.counts parse_train_vert.dat rep_train_vert.dat

# recount
python count_cfg_freqs.py rep_train_vert.dat > rep_cfg_vert.counts

# cky_parser
python cky_parser.py rep_cfg_vert.counts parse_dev.dat res_vert.tree

#evaluation
python eval_parser.py parse_dev.key res_vert.tree
