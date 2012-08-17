#!/usr/bin/env python
""" convert from 20news group to vw input """
import sys, os, nltk
from nltk.tokenize import PunktSentenceTokenizer, WordPunctTokenizer
from collections import defaultdict
from sequence import *

input_dir = sys.argv[1]

sent_tokenizer = PunktSentenceTokenizer()
token_tokenizer = WordPunctTokenizer()

group_seq = Sequence(1)
for group in os.listdir(input_dir):
    group_id = group_seq.id_for(group)
    sys.stderr.write("%s\t%s\n" % (group, group_id))
    for article_path in os.listdir("%s/%s" % (input_dir, group)):
        # stitch article into a single string
        article = ""
        for line in open("%s/%s/%s" % (input_dir, group, article_path)):
            line = line.strip()
            if len(line) > 0 and not line.startswith(">"):
                article += " "
                article += line
        # tokenise sentences then some simple normalisation, collect just binary features
        all_tokens = set()
        for sentence in sent_tokenizer.tokenize(article):
            tokens = token_tokenizer.tokenize(sentence)
            tokens = map(lambda t: t.lower().replace(":","").replace("|",""), tokens)  # : and | reserved for vw format
            tokens = filter(lambda t: len(t) > 3, tokens)
            all_tokens.update(tokens)
        # write out token features ; weight of 0.5
        sys.stdout.write("1 1 '%s_%s |tokens" % (group, article_path))  # 1 weight=1 label
        for token in all_tokens:
            sys.stdout.write(" %s:0.5" % token)
        # followed by single group feature (with weighting = magic 10, therefore quadratic features have weight 5)
        sys.stdout.write(" |group %s:10" % group)
        sys.stdout.write("\n")



