# This file is a shell script for problem5
date_start=$(date +%s)
echo '' > suffix_tagger.model
python tagger_history_generator.py GOLD < tag_train.dat > tag_train.gold
i=0
while [ $i -lt 5 ]
do  
        python pipe5.py suffix_tagger.model tag_train.dat tag_train.gold
        let i++  
        echo $i
done 
date_end=$(date +%s)
echo "Training Time:$((date_end-date_start))sec"
date_start=$(date +%s)
python pipe52.py ENUM suffix_tagger.model < tag_dev.dat > tag_dev_suffix.out
python eval_tagger.py tag_dev.key tag_dev_suffix.out
rm tag_train.gold
date_end=$(date +%s)
echo "Predicting Time:$((date_end-date_start))sec"