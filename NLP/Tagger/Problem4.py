# Problem 4

#___________4.1_____________
# Firs, count. store into file 'ner.counts'

python count_freqs.py ner_train.dat > ner.counts

# Calculate emission: emission.py. Store into file emission.dat
# Format: [probabilisy] [word] [tag]

python emission.py ner.counts emission.file

#____________4.2____________
# Replace low frequent words that counts < 5 by '_RARE_'. Store into file ner_train_replaced.dat

python replace.py ner_train.dat ner_train_replaced.dat no_opt

# Count. Store into file 'ner_replaced.counts'

python count_freqs.py ner_train_replaced.dat > ner_repaced.counts

# Calculate emission. Store into file prior.dat
python emission.py ner_replaced.counts prior.file

#____________4.3______________
# tag the test file using base_tagger

python base_tagger.py prior.file ner_dev.key base_pre.file

# evaluate the performance of baseline tagger

python eval_ne_tagger.py ner_dev.key base_pre.file
