# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
I'm using this script to lemmatize casanatensis.xml.
"""


##################
# IMPORT MODULES #
##################

from __future__ import print_function
import xml.etree.ElementTree as ET
import treetaggerwrapper
#import os
#import sys
#import re
#import glob
#import subprocess
#import pprint


##########################
# LEMMATIZE/TAG XML FILE #
##########################

# The namespace
n    = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
nx   = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

# Parse the tree
tree = ET.parse('/home/ilbuonme/ursus/casanatensis.xml')
#tree = ET.parse('/home/ilbuonme/ursus/lemma/tree_tagger_and_related_files/lemmatized_casanatensis.xml')
#root = tree.getroot()

# Create list of words to tag
ursus_words = tree.findall('.//' + n + 'w')
ursus_orig_ns = [unicode(uon_word.get('n').lower()) for uon_word in ursus_words]

# Do the tagging of the list
tagger = treetaggerwrapper.TreeTagger(TAGLANG='la')
tags = tagger.tag_text(ursus_orig_ns, numlines=True, tagonly=True)

# A list of values of <w type=""> that say that the word is not parsable
non_parsable_word_types = ['nonsense', 'alphabemes', 'ancientAbbreviation', 'foreign', 'numeral']

# Add new attributes to the <w> elements 
c = 0   # already parsed
d = 0   # parsed
e = 0   # unparsable
for i in range(len(tags)):
    if ursus_words[i].get('lemma'):    # Strangely enough, here the namespace should not be pre-pended
        print('Word "' + ursus_words[i].get('n') + '" (xml:id=' + ursus_words[i].get(nx+'id') + ') ', end='') 
        print('had already been lemmatized/parsed (@lemma="' + ursus_words[i].get('lemma') + '")')
        c = c +1
    else:
        if ursus_words[i].get('type') not in non_parsable_word_types:
            #ursus_words[i].set('n',     ursus_words[i].get('n'))
            if tags[i].split('\t')[0] != ursus_words[i].get('n').lower():
                print('WARNING: check modern spelling (@n) of the word with xml:id ' + ursus_words[i].get(nx + 'id'))
            ursus_words[i].set('ana',   tags[i].split('\t')[1])
            ursus_words[i].set('lemma', tags[i].split('\t')[2])
            d = d + 1
        else:
            #print('"' + ursus_words[i].get('n') + '" [' + ursus_words[i].get('type') + ']', end='')
            e = e + 1
            #pass

print('\nLemmatization/PoS tagging result:')
print('\t - ' + str(c) + ' words not parsed b/c they had been previously parsed')
print('\t - ' + str(d) + ' words parsed')
print('\t - ' + str(e) + ' words unparsable')


###############################
# TAGSET INTERPRETATION TABLE #
###############################

# This 'explanation' of the PoS tags is based on
# /home/ilbuonme/ursus/lemma/tree_tagger_and_related_files/parameter_files/from_treetagger_website/index_thomisticus/Tagset_IT.pdf

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
        #11 Graphical-Variation
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


#########################################################
# OUTPUT TO SCREEN HUMAN-READABLE RESULT OF THE PARSING #
#########################################################

def parse_IT_tagset(ITString):
        # This function returns a list with a human-readable version of the Index Thomisticus tag.
        # It turns 11B---A1--- into ['Nominal', 'Positive' etc.]
        outList = []
        for p in range(len(ITString)):  # i.e. range(11). Variable 'p' is an integer
            ITCode      = ITString[p]               # for example, '1'
            ITMeaning   = tagsetlist[p][ITCode]   # for example, 'Nominal'
            outList.append(ITMeaning)
        return outList

def print_tagging_output_to_terminal(my_tags):
    for t in my_tags:
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

# Uncomment this if I want to see it on screen
# § quando ho provato a decommentare questo, mi ha iniziato a dare un KeyError:
#   KeyError: u'S'
# Vd. come debuggarlo (quella chiave non c'è nel dizionario, veramente?)
#print_tagging_output_to_terminal(tags)


#################
# PRINT TO FILE #
#################

tree.write('/home/ilbuonme/ursus/lemmatized_casanatensis.xml', encoding="UTF-8", method="xml")
#tree.write('/home/ilbuonme/ursus/lemma/tree_tagger_and_related_files/lemmatized_casanatensis2.xml', encoding="UTF-8", method="xml")
