# Problem 5

#________________5.1_______________
# calculate parameter of log(trigram), save into trigram.dat
# use the replaced file ver_replaced.counts
# output format: [tag1] [tag2] [tag3] [log p(tag3|tag1, tag2)]

python trigram.py ver_replaced.counts trigram.dat

# run viterbi tagger
python viterbi.py prior.file trigram.dat ner_dev.dat viterbi_pre.file no_opt

# evaluate the model
python eval_ne_tagger.py ner_dev.key viterbi_pre.file

