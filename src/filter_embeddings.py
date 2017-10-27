#!/usr/bin/env python

from codecs import open
from sys import argv

def filter_embeddings(fname, exclude_vocab):
    with open(fname, 'r', encoding='utf-8') as in_f:
        with open(fname+'.filtered', 'w', encoding='utf-8') as out_f:
            for line in in_f:
                fields = line.strip().split()
                if fields:
                    word = fields[0]
                    if word not in exclude_vocab:
                        out_f.write(line)


def read_vocab(fname):
    vocab = set()
    with open(fname, 'r', encoding='utf-8') as in_f:
        for line in fname:
            word = line.strip().split('\t')[0]
            vocab.add(word)

    return vocab

if __name__ == '__main__':
    embeds_file = argv[0]
    train_file = argv[1]
    test_file = argv[2]

    train_vocab = read_vocab(train_file)
    test_vocab = read_vocab(test_file)
    exclusion_vocab = test_vocab.difference(train_vocab)

    filter_embeddings(embeds_file, exclusion_vocab)
