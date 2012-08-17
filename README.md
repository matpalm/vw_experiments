# random vowpal wabbit experiments

## data

using the 20 newsgroup data...
    
    wget http://qwone.com/~jason/20Newsgroups/20news-bydate.tar.gz
    tar zxf 20news-bydate.tar.gz

## one against all

it turns out vowpal does multi class prediction. it has a common of different options, let's start with the vanilla one-against-all

    # convert to vowpal format
    # dead simple binary features
    ./20news_to_vw.oaa.py 20news-bydate-train >train.oaa 2>group_id.train.tsv &
    ./20news_to_vw.oaa.py 20news-bydate-test  >test.oaa  2>/dev/null &  # labels assigned are irrelevant for test set
    wait

    # train model; use LBFGS 
    rm .cache
    shuf train.oaa | vw -f model --bfgs -c --passes 10 --l1 0.01 --oaa 20 --quiet

    # test
    shuf test.oaa > foo; mv foo test.oaa
    cat test.oaa | vw -t -i model --quiet -p predictions

    # draw confusion matrix (though matplotlib blows, i'm going back to ggplot...)
    ./generate_confusion_matrix.py predictions group_id.train.tsv confusion_matrix.png

with this we get 6013 / 7532 correct ~= 80% which is pretty lame but with just binary unweighted features this is good enough to start..

how do things look if we do represent the multi class as namespaced feature?

    ./20news_to_vw.group_namespace.py 20news-bydate-train >train.group_namespace 2>group_id.train.tsv &
    ./20news_to_vw.group_namespace.test.py 20news-bydate-test >test.group_namespace &
    wait

    rm .cache
    shuf train.group_namespace | vw -f model -q tg --bfgs -c --passes 10 --l1 0.01 --quiet
    cat test.group_namespace | vw -t -i model -q tq --quiet -p predictions








