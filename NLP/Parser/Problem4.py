
# Problem 4
# This file is detailed instruction of Problem4
# We only need to replace low frequency words and generate counts

# replacement could be done by 'replace.py'

# firstly, count freqs of original parse_train.dat
python count_cfg_freq.py parse_train.dat > cfg.counts

# replacing the rare terminals by _RARE_
python replace.py cfg.counts parse_train.dat parse_new_train.dat
