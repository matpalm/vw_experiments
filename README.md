# random vowpal wabbit experiments

## data

using the 20 newsgroup data...
    
    wget http://qwone.com/~jason/20Newsgroups/20news-bydate.tar.gz
    tar zxf 20news-bydate.tar.gz

## one against all

    # convert to vowpal format
    # dead simple binary features
    ./20news_to_vw.oaa.py 20news-bydate-train >train.oaa 2>group_id.train.tsv &
    ./20news_to_vw.oaa.py 20news-bydate-test  >test.oaa  2>/dev/null &  # labels assigned are irrelevant for test set
    wait

    # train model
    shuf train.oaa | vw -f model --oaa 20

    # test
    shuf test.oaa > foo; mv foo test.oaa
    cat test.oaa | vw -t -i model --quiet -p predictions

    # draw confusion matrix (though matplotlib blows, i'm going back to ggplot...)
    ./generate_confusion_matrix.py predictions group_id.train.tsv confusion_matrix.png

will this we get 5420 / 7532 correct ~= 70% which is pretty lame but with just binary features is fine

