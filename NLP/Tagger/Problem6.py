# We need to reproduce a doc 'replace'

python replace.py ner_train.dat ner_train_opt.dat opt

# counts

python count_freqs.py ner_train_opt.dat > ner_opt.counts

# calculate emission

python emission.py ner_opt.counts emission_opt.file

# calculate trigram for viterbi

python trigram.py ner_opt.counts trigram_opt.file

# use viterbi tagger to tag the test file

python viterbi_tagger.py emission_opt.file trigram_opt.file ner_dev.dat viterbi_pre_opt.file opt

# evaluation

python eval_ne_tagger.py ner_dev.key viterbi_pre_opt.file
