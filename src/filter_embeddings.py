#!/usr/bin/env python

from codecs import open
from sys import argv

directories = '''UD_Ancient_Greek
UD_Ancient_Greek-PROIEL
UD_Arabic
UD_Basque
UD_Bulgarian
UD_Catalan
UD_Chinese
UD_Croatian
UD_Czech
UD_Czech-CAC
UD_Czech-CLTT
UD_Danish
UD_Dutch
UD_Dutch-LassySmall
UD_English
UD_English-LinES
UD_English-ParTUT
UD_Estonian
UD_Finnish
UD_Finnish-FTB
UD_French
UD_Galician
UD_Galician-TreeGal
UD_German
UD_Gothic
UD_Greek
UD_Hebrew
UD_Hindi
UD_Hungarian
UD_Indonesian
UD_Irish
UD_Italian
UD_Italian-ParTUT
UD_Japanese
UD_Kazakh
UD_Korean
UD_Latin
UD_Latin-ITTB
UD_Latin-PROIEL
UD_Latvian
UD_Norwegian-Bokmaal
UD_Norwegian-Nynorsk
UD_Old_Church_Slavonic
UD_Persian
UD_Polish
UD_Portuguese
UD_Portuguese-BR
UD_Romanian
UD_Russian
UD_Russian-SynTagRus
UD_Slovak
UD_Slovenian
UD_Slovenian-SST
UD_Spanish
UD_Spanish-AnCora
UD_Swedish
UD_Swedish-LinES
UD_Turkish
UD_Ukrainian
UD_Urdu
UD_Uyghur
UD_Vietnamese'''.split('\n')
languages = '''grc
grc_proiel
ar
eu
bg
ca
zh
hr
cs
cs_cac
cs_cltt
da
nl
nl_lassysmall
en
en_lines
en_partut
et
fi
fi_ftb
fr
gl
gl_treegal
de
got
el
he
hi
hu
id
ga
it
it_partut
ja
kk
ko
la
la_ittb
la_proiel
lv
no_bokmaal
no_nynorsk
cu
fa
pl
pt
pt_br
ro
ru
ru_syntagrus
sk
sl
sl_sst
es
es_ancora
sv
sv_lines
tr
uk
ur
ug
vi'''.split('\n')

emb_langs = '''ar
bg
ca
cs
da
de
el
en
es
et
eu
fa
fi
fr
ga
he
hi
hr
id
it
nl
no
pl
pt
sl
sv'''.split('\n')

def filter_embeddings(fname, exclude_vocab):
    c = 0
    with open(fname, 'r', encoding='utf-8') as in_f:
        with open(fname+'.filtered', 'w', encoding='utf-8') as out_f:
            for line in in_f:
                fields = line.strip().split()
                if fields:
                    word = fields[0]
                    if word not in exclude_vocab:
                        out_f.write(line)
                    else:
                        c+= 1

    print('skipped {0} words in {1}'.format(c, fname))

def read_vocab(fname):
    vocab = set()
    with open(fname, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            if not line.strip(): continue
            word = line.strip().split()[0]
            vocab.add(word)

    return vocab

if __name__ == '__main__':
    embeds_file = '/home/rvx618/data/poly_a/{0}.polyglot.txt'
    train_file = '/home/rvx618/data/{0}/{1}-ud-train.conllu.deprel'
    test_file = '/home/rvx618/data//{0}/{1}-ud-dev.conllu.deprel'
    for idx, directory in enumerate(directories):
        lang = languages[idx]
        if len(lang.split('_')) != 1: continue
        emb_lang_code = lang.split('_')[0]
        if emb_lang_code not in emb_langs: continue

        train_vocab = read_vocab(train_file.format(directory, lang))
        try:
            test_vocab = read_vocab(test_file.format(directory, lang))
        except IOError:
            print('error on {0}'.format(directory))
            continue
        exclusion_vocab = test_vocab.difference(train_vocab)
        filter_embeddings(embeds_file.format(emb_lang_code), exclusion_vocab)
