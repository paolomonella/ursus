#!/usr/bin/env python


#import codecs


# Import module For XML
from xml.dom.minidom import parse, parseString

# For CLTK
#from cltk.corpus.utils.importer import CorpusImporter
#corpus_importer = CorpusImporter('latin')
#corpus_importer.import_corpus('latin_models_cltk')
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag


lemmatizer = LemmaReplacer('latin')
tagger = POSTag('latin')
j = JVReplacer()

text = []
#text = ['Gallia', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres']
with open('/home/ilbuonme/siti/paolo.monella/ursus/lemma/recycleBin/textForOrig-myCLTK.txt', 'r') as f:
    for x in f.readlines():
        for w in x.split(' '):
            text.append(w)

for t in text:
    if t:
        # Note: the tagger likes 'divisa', while the lemmatizer likes 'diuisa'
        lemmaList = lemmatizer.lemmatize(t.lower())
        posList   = tagger.tag_tnt(j.replace(t.lower()))
        form = posList[0][0]
        lemma = lemmaList[0].replace('v', 'u')
        pos = posList[0][1]
        print('<w n="' + form + '" lemma="'+lemma + '" ana="' + pos + '">')

"""
# Apprently j.replace... makes it worse for the POS tagger, so I'm dropping it in this case
text = j.replace(text.lower())
forms = tagger.tag_unigram(text.lower())
for fm in forms:
    print(fm)
"""
