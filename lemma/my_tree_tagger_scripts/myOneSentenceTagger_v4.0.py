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
sentence = u'duce consulem'
textToParse = (sentence).split()
print(textToParse)
tags = tagger.tag_text(textToParse, numlines=True, tagonly=True)


newtagsetlist = {
        'ESSE:IND': 'Verbo ausiliare “Essere”: Indicativo',
        'ESSE:SUB': 'Verbo ausiliare “Essere”: Congiuntivo',
        'ESSE:INF': 'Verbo ausiliare “Essere”: Infinito',
        'V:IND': 'Verbo: Indicativo',
        'V:SUB': 'Verbo: Congiuntivo',
        'V:INF': 'Verbo: Infinito',
        'V:GER': 'Verbo: Gerundio',
        'V:GED': 'Verbo: Gerundivo',
        'V:PTC:nom': 'Verbo: Participio, nominativo',
        'V:PTC:acc': 'Verbo: Participio, accusativo',
        'V:PTC:abl': 'Verbo: Participio, ablativo',
        'V:PTC': 'Verbo: Participio',
        'V:SUP:acc': 'Verbo: Supino, accusativo',
        'V:SUP:abl': 'Verbo: Supino, ablativo',
        'V:IMP': 'Verbo: Imperativo',
        'PRON': 'Pronomi',
        'REL': 'Pronomi: Relativi',
        'POSS': 'Possessivi (Pronomi e/o Aggettivi)',
        'DIMOS': 'Dimostrativi (Pronomi e/o Aggettivi)',
        'INDEF': 'Pronomi: Indefiniti',
        'N:nom': 'Nomi, nominativo',
        'N:dat': 'Nomi, dativo',
        'N:gen': 'Nomi, genitivo',
        'N:loc': 'Nomi, locativo',
        'N:acc': 'Nomi, accusativo',
        'N:abl': 'Nomi, ablativo',
        'N:voc': 'Nomi, vocativo',
        'ADJ:NUM': 'Numerali (tutti i tipi)',
        'CC': 'Congiunzioni Coordinanti',
        'CS': 'Congiunzioni Subordinanti',
        'NPR': 'Nomi Propri',
        'ADJ': 'Aggettivi',
        'ADJ:COM': 'Aggettivi, comparativi',
        'ADJ:SUP': 'Aggettivi, superlativi',
        'ADJ:abl': 'Aggettivi, ablativi',
        'ADV': 'Avverbi',
        'PREP': 'Preposizioni',
        'INTV': 'Interiezioni',
        'ABBR': 'Abbreviazioni',
        'EXCL': 'Esclamazioni',
        'FW': 'Parole straniere',
        'SENT': 'Punteggiatura di fine frase',
        'PUN': 'Punteggiatura NON di fine frase',
        'SYM': 'Simboli',
        'CLI': 'Enclitiche'
        }


def parse_IT_tagset(ITString):
        '''This function returns a list with a human-readable version of the Index Thomisticus tag.
        It turns 11B---A1--- into ['Nominal', 'Positive' etc.]
        Update 02.03.2019. The tagset for treetagger seems to have changed, so this visualization seems
        not to work any longer.
        The new tagset seems to be the one in
        http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/Lamap-Tagset.pdf
        '''
        
        outList = []
        for p in range(len(ITString)):  # i.e. range(11). Variable 'p' is an integer
            ITCode      = ITString[p]               # for example, '1'
            try:
                ITMeaning   = tagsetlist[p][ITCode]   # for example, 'Nominal'
                outList.append(ITMeaning)
            except(KeyError):
                print('Il tag', ITCode, 'non viene riconosciuto, all\'interno della stringa', ITString)
        return outList

for t in tags:
    tForm, tTag, tLemma = t.split('\t')
    print('\n' + tForm + ':')
    print('\tLemma:\t' + tLemma)
    print('\tTag:\t' + newtagsetlist[tTag])
