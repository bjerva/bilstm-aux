#!/usr/bin/env python

'''
Generate experiment runs for Select or Reject
:author: Johannes Bjerva
'''

import argparse

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
UD_French-ParTUT
UD_French-Sequoia
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
fr_partut
fr_sequoia
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--main-sample-range', nargs='*', type=int, required=True)
    parser.add_argument('--aux-sample-range', nargs='*', type=int, required=True)
    parser.add_argument('--n-runs', type=int, default=1)
    #parser.add_argument('--aux-dir', required=True)
    args = parser.parse_args()

    base_bilty = '''python -u src/bilty.py \
    --train ~/data/{0}/{1}-ud-train.conllu.deprel  ~/data/{0}/{1}-ud-test.conllu.pos \
    --dev ~/data/{0}/{1}-ud-dev.conllu.deprel  \
    --test ~/data/{0}/{1}-ud-test.conllu.deprel  ~/data/{0}/{1}-ud-test.conllu.pos  \
    --pred_layer 1 1  --trainer adam  \
    --main-samples {2} \
    --aux-samples {3}'''
    #0: train language dir,
    #1: lang code
    #1: main samples,
    #2: aux samples

    base_log = ' > ~/logs/{0}_{1}_{2}_{3}'
    #1: lang code
    #1: main samples,
    #2: aux samples


    base_slurm = '''#!/bin/bash
#SBATCH --job-name=SelRejMTL-{0}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=30:00:00

'''
    # 0: language
    for idx, directory in enumerate(directories):
        lang = languages[idx]
        curr_slurm = base_slurm.format(lang)
        for main_size in args.main_sample_range:
            for aux_size in args.aux_sample_range:
                curr_bilty = base_bilty.format(directory, lang, main_size, aux_size)
                for run in range(args.n_runs):
                    curr_bilty += base_log.format(lang, main_size, aux_size, run)
                    with open('runs/'+base_log.format(lang, main_size, aux_size, run)[10:]+'.sh', 'w') as out_f:
                        out_f.write(curr_slurm+curr_bilty)
                #print(curr_slurm + curr_bilty)
