# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# I'm using this script as a toolbox to parse text with treeTagger and the IT Latin parameter file.
# This script parses one sentence only, which must be included as a list of word in the 'text' variable.
# Change the value of list 'text' below to parse some text. Example:
#        textToParse = ['x', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres']
# or:
#        sentence = 'sententia est composita ex diuersis figuris quarum nonnullae figurae uocis sunt'
#        textToParse = (sentence).split()

import pprint
import treetaggerwrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='la')
#textToParse = ['x', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres']
sentence = u'nemo poeta est'
textToParse = (sentence).split()
print(textToParse)
tags = tagger.tag_text(textToParse, numlines=True, tagonly=True)

# The new tagset seems to be the one in
# http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/Lamap-Tagset.pdf

for t in tags:
    tForm, tTag, tLemma = t.split('\t')
    print('\n' + tForm + ':\n\tTag: ' + tTag + '\n\tLemma: ' + tLemma)
