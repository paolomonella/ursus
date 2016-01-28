#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To-do:
# - correct the 'except'
# - add 'if': only if w doesn't already have a @lemma and (and? or?) a @morph, do parsing
# - eventually, remove the 'mod' moderator
# - find correct attributes for @lemma and @morph
# - find out why it doesn't parse obvious words (such as 'ex')
# - possibly add 'clear' after each inflected form
# - report to DC list/wiki



# Import modules

from xml.dom.minidom import parse, parseString
import xmlrpclib
import codecs

# Set parameters for xmlrpclib

server = xmlrpclib.ServerProxy("http://archimedes.mpiwg-berlin.mpg.de:8098/RPC2")
lang = "-LA"

# Parse XML

xmldoc = parse('../../casanatensis.xml')
#xmldoc = parse('/home/ilbuonme/siti/paolo.monella/ursus/shorter_casanatensis.xml')
wordElementList = xmldoc.getElementsByTagName('w')


mod = 0
for w in wordElementList:
        # This 'mod' limits the number of words to be parsed
        if mod < 5:
            form = w.attributes['ana'].value
            # Parse the inflected word
            try:
                    results = server.lemma(lang, form, "full")
                    print('\n\n---\n\nForm: ' + form + '\n')
                    for fr in results:
                        lemmaOptions = results[fr]
                        count = 0
                        # Show the user all possible lemmas and morphological analysis
                        #print('\nPossible lemmas: ' + ', '.join(lemmaOptions))
                        for lemma in lemmaOptions:
                            morphAnaOptions  = lemmaOptions[lemma]
                            print('\tLemma: ' + lemma)
                            for i, m in enumerate(morphAnaOptions):
                                pass
                                count = count + 1
                                print('\t\t' + str(count) + ' ' + m)
                                morphAnaOptions[i] = {count: morphAnaOptions[i]}
                        # Prompt user for the right lemma/morphological analysis
                        answer = int(raw_input("Choose the number of the right lemma/morphological analysis: "))
                        # Retrieve the correct lemma/morphological analysis based on the user's answer
                        for lemma in lemmaOptions:
                            morphAnaOptions  = lemmaOptions[lemma]
                            for m in morphAnaOptions:
                                if m.keys()[0] == answer:
                                    correctMorph = m[m.keys()[0]]
                                    w.setAttribute('n', form)
                                    w.setAttribute('lemma', lemma)
                                    w.setAttribute('ana', correctMorph)
            except (xmlrpclib.Error, v):
                    print("ERROR", v)
            mod = mod + 1

                                     
f = open('output.xml', 'w')
#xmldoc.content.strip(codecs.BOM_UTF8)
#xmldoc.writexml(f).encode('utf-8').decode('utf-8')
f = codecs.lookup("utf-8")[3](f)
xmldoc.writexml(f, encoding="utf-8")
f.close()
