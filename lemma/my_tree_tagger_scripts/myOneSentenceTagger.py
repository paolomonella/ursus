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




tagsetlist = [
        #1 Flexional-Type
        {
            '1' : 'Nominal',
            '2' : 'Participial',
            '3' : 'Verbal',
            '4' : 'Invariable',
            '5' : 'Pseudo-lemma',
            },
        #2 Nominals-Degree
        {
            '1' : 'Positive',
            '2' : 'Comparative',
            '3' : 'Superlative',
            '4' : 'Not stable composition',
            '-' : 'None',
            },
        #3 Flexional-Category
        {
            'A' : 'I decl',
            'B' : 'II decl',
            'C' : 'III decl',
            'D' : 'IV decl',
            'E' : 'V decl',
            'F' : 'Regularly irregular decl',
            'G' : 'Uninflected nominal',
            'J' : 'I conjug',
            'K' : 'II conjug',
            'L' : 'III conjug',
            'M' : 'IV conjug',
            'N' : 'Regularly irregular conjug',
            'O' : 'Invariable',
            'S' : 'Prepositional (always or not) particle',
            '-' : 'None',
            },
        #4 Mood
        {
            'A' : 'Active indicative',
            'J' : 'Pass/Dep indicative',
            'B' : 'Active subjunctive',
            'K' : 'Pass/Dep subjunctive',
            'C' : 'Active imperative',
            'L' : 'Pass/Dep imperative',
            'D' : 'Active participle',
            'M' : 'Pass/Dep Participle',
            'E' : 'Active gerund',
            'N' : 'Passive Gerund',
            'O' : 'Pass/Dep gerundive',
            'G' : 'Active supine',
            'P' : 'Pass/Dep supine',
            'H' : 'Active infinitive',
            'Q' : 'Pass/Dep infinitive',
            '-' : 'None',
            },
        #5 Tense
        {
            '1' : 'Present',
            '2' : 'Imperfect',
            '3' : 'Future',
            '4' : 'Perfect',
            '5' : 'Plusperfect',
            '6' : 'Future perfect',
            '-' : 'None',
            },
        #6 Participials-Degree
        {
            '1' : 'Positive',
            '2' : 'Comparative',
            '3' : 'Superlative',
            '-' : 'None',
            },
        #7 Case/Number
        {
            'A' : 'Singular Nominative',
            'J' : 'Plural Nominative',
            'B' : 'Singular Genitive',
            'K' : 'Plural Genitive',
            'C' : 'Singular Dative',
            'L' : 'Plural Dative',
            'D' : 'Singular Accusative',
            'M' : 'Plural Accusative',
            'E' : 'Singular Vocative',
            'N' : 'Plural Vocative',
            'F' : 'Singular Ablative',
            'O' : 'Plural Ablative',
            'G' : 'Adverbial',
            'H' : 'Casus "plurimus"',
            '-' : 'None',
            },
        #8 Gender/Number/Person
        {
            '1' : 'Masculine',
            '2' : 'Feminine',
            '3' : 'Neuter',
            '4' : 'I singular',
            '5' : 'II singular',
            '6' : 'III singular',
            '7' : 'I plural',
            '8' : 'II plural',
            '9' : 'III plural',
            '-' : 'None',
            },
        #9 Composition
        {
            'A' : 'Enclytic -ce',
            'C' : 'Enclytic -cum',
            'M' : 'Enclytic -met',
            'N' : 'Enclytic -ne',
            'Q' : 'Enclytic -que',
            'T' : 'Enclytic -tenus',
            'V' : 'Enclytic -ve',
            'H' : 'Ending homographic with enclytic',
            'Z' : 'Composed with other form',
            'W' : 'As lemma',
            '-' : 'None',
            },
        #10 Formal-Variation
        {
            'A' : 'I variation of wordform',
            'B' : 'II variation of wordform',
            'C' : 'III variation of wordform',
            'X' : 'Author mistake, or bad reading?',
            '-' : 'None',
            },
        {
            '1' : 'Baseform',
            '2' : 'Graphical variation A',
            '3' : 'Graphical variation B',
            '4' : 'Graphical variation C',
            '5' : 'Graphical variation D',
            '6' : 'Graphical variation E',
            '-' : 'None',
            }
        ]


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


#print('%10s %10s %16s' %  ('FORM', 'LEMMA', 'POS TAG'))
for t in tags:
    tForm, tTag, tLemma = t.split('\t')
    tTagList = parse_IT_tagset(tTag)    # This interprets the IT tagset codes and returns a list
    tTagList = [x for x in tTagList if x != 'None'] # This removes all 'None' elements from the list

    # Print format 1: messier, but less space-consuming
    #outTag = (', ').join(tTagList)
    #print('%10s %10s %16s' %  (tForm, tLemma, outTag))

    # Print format 2: clearer, but more space-consuming
    print('\n' + tForm, '('+tLemma+'):'.ljust(20))
    for x in tTagList:
        print('\t' + x.ljust(20))
    print('\t' + tTag)  # This prints the original 2-LM41A2--- string


#La 'spiegazione' dei POS tag è in
#../../ursus/lemma/tree_tagger_and_related_files/parameter_files/from_treetagger_website/index_thomisticus/Tagset_IT.pdf


# ALTERNATIVE WAYS OF PRINTING THE OUTPUT:

#pprint.pprint(tags)

#for x in textToParse:
#    originalForm = x
#    fullTag = tags[textToParse.index(x)]
#    tForm, tTag, tLemma = fullTag.split('\t')
#    print('%10s %10s %16s %10s' %  (originalForm, tForm, tTag, tLemma))


# Però il codice tags[textToParse.index(x)] non funzionerà sempre, perché index() trova il *primo* elemento della lista che ha quel valore. Che succederà quando ci saranno tanti 'in' nella lista? Bisogna trovare una strategia migliore, prendendo l'indice esatto 'y' della prima lista (magari con un counter) e usando un semplice tags[y] nella seconda lista. Probabilmente la cosa migliore è mettere degli xml:id nei <w>

