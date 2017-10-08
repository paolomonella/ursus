#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script simplifies the encoding of casanatensis.xml
# and creates a file ALIM2_publication/casanatensis_AL.xml
# with the Alphabetic Layer only. 
#
# It's written in Python 3.4, but also works with Python 2.7.
# It uses the Python lxml library.

from __future__ import print_function
import os
from lxml import etree


# Clear screen
os.system('clear')

# Namespaces
n = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
xml = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
#ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')   # This used to work when I used ElementTree
ns = {'tei': 'http://www.tei-c.org/ns/1.0',             # for TEI XML
        'xml': 'http://www.w3.org/XML/1998/namespace'}  # for attributes like xml:id

# Parse the tree of casanatensis.xml
tree = etree.parse('../casanatensis.xml')

# Corr with cert=medium

print('\n################################\n# CORRECTIONS WITH CERT=MEDIUM #\n################################\n\n')

L = []
c = 0
d = 0
for x in tree.findall('.//' + n + 'corr'):
    if x.get('cert') == 'medium':
        choice = x.getparent()
        sic = choice.find(n + 'sic')

        if sic.find(n + 'w') is not None:
            sicw = sic.find(n + 'w')        # 'wrong' word
            sicwtxt = sicw.xpath('normalize-space()').encode('utf8')
        else:
            sicwtxt = ''

        if x.find(n + 'w') is not None:
            corrw = x.find(n + 'w')         # 'right' word
            corrwid = corrw.get(xml + 'id')
            print(corrwid, end = '\t')
            corrwtxt = corrw.xpath('normalize-space()').encode('utf8')
            #wtxt = corrw.text.strip()
        else:
            corrwtxt = ''

        print('"' + str(sicwtxt) + '" → "' + str(corrwtxt) + '"')
        #print(x.get('subtype'))
        if x.find(n + 'note') is not None:
            y = x.find(n + 'note')
            print(y.text.encode('utf-8'))
            c = c + 1
        else:
            z = x.get('type')
            print('Error type: "' + z + '"')
            d = d + 1
        print()
for l in set(L):
    print(l)





# Notes with subtype='crux'

print('\n\n#############################\n# NOTES WITH SUBTYPE="CRUX" #\n#############################\n\n')

cc = 0
for x in tree.findall('.//' + n + 'note'):
    if x.get('type') == 'emendation' and x.get('subtype') == 'crux':
        prevWord = x.getprevious()      # The previous word
        print('\n' + prevWord.get(xml + 'id') + '\t"' + prevWord.xpath(".//text()")[0].strip() + '"')
        print(x.text.encode('utf-8'))
        cc = cc + 1






# Summary

print('\n\n###########\n# SUMMARY #\n###########\n\n')

print(str(c) + ' notes on general matters\n' \
        + str(d) + ' notes with a <correction> type\n' \
        + str(cc) + ' cruces desperationis\n')

# Parse the tree of the ALIM2 template: it will be the base for the output tree
no_blank = False
if no_blank:
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse('ALIM2_publication/teiHeader_template.xml', parser)
else:
    tree = etree.parse('ALIM2_publication/teiHeader_template.xml')

root = tree.getroot()
#root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

# Append the <body> of casanatensis.xml into <text> of the output xml file
myBody = casanaTree.getroot().find(n + 'text').find(n + 'body')
myText = root.find(n + 'text')        # <text> of output xml file
myText.append(myBody)

#######################################################
# Temporary section to check notes @type="emendation" #
#######################################################

f = open('/home/ilbuonme/Scrivania/foo.txt', 'w')
cc = 0
cww = 0
crr = 0
for x in tree.findall('.//' + n + 'note[@type="emendation"]'):
    cc = cc + 1
    daddy = x.getparent()
    dtag = etree.QName(daddy).localname
    if dtag == 'w':
        #print('Daddy is w')
        cww = cww + 1
    elif dtag == 'ref':
        print('"' + x.text + '"', file=f)
        print('---', file=f)
        crr = crr + 1
        x.set('subtype', 'emendation_to_whole_section')
    else:
        print(x.text)
print('Total: %s. Notes to word: %s. Notes to section: %s' % (cc, cww, crr))
f.close()


#############
# Functions #
#############

def deleteAllElements(myElemName, myNameSpace):
    search = ('.//{0}' + myElemName).format(myNameSpace)
    my_elem_parents = tree.findall(search + '/..')
    for x in my_elem_parents:
        for y in x.findall(myNameSpace + myElemName):
            x.remove(y)

def substituteAllElements(oldName, newName, myNameSpace):
    for x in tree.findall('.//' + myNameSpace + oldName):
        x.tag = myNameSpace + newName
        x.set('type', oldName)

def manageWord(wordElem):
    # Easy solution (only backdraw: it moves all elements children of <w> after the text). This is
    # OK (it's actually better) for 'anchor/pb/cb/lb', but it creates a slight inaccuracy with 'gap':
    tempText = wordElem.xpath('normalize-space()').replace(' ', '').replace('·', '') # This is the unified text of the word
    if wordElem.get('type') in ['alphabemes', 'foreign']:
        tempText = '"' + tempText + '"'
    for y in wordElem:
        yt = etree.QName(y).localname
        if yt in ['choice', 'add', 'pc', 'hi']:    # I'm removing them b/c they include text, or b/c it's <pc n="space">
            y.getparent().remove(y)
        y.tail = None
    wordElem.text = tempText

def managePunctuation(punctElem):
    v = punctElem.get('n').replace('question', '?')
    punctElem.text = v
    if v in ['0', 'quote', 'space']: # Delete <pc> altogether
        punctElem.getparent().remove(punctElem)
    elif v in ['.', '?', ',']:   # Append to the text content of previous <w>
        # I'm using '?' instead of 'question' because of the line that replaced 'question' with '?'
        if punctElem.getprevious() is None:
            # Just give up and leave the <pc> element as it is
            pass
        elif punctElem.getprevious().tag in [n + 'lb', n + 'milestone', n + 'gap']:
            # Just give up and leave the <pc> element as it is
            if punctElem.getprevious().tag != n + 'gap':
                print('Alas! Punctuation sign not coming immediately after <w> or <gap>')
                punctElem.set('type', 'trouble')
        elif punctElem.getprevious().tag == n + 'w': # If previous sibling is <w>, append punctuation to its textual content
            punctElem.getprevious().text = punctElem.getprevious().text + v
            #punctElem.getprevious().tail = v + '\n' # Nope: this generates code like
                                             # <w n="dicam" xml:id="w564">dicam<lb n="1r.a.23" break="no"/></w>,
            punctElem.getparent().remove(punctElem)
        elif punctElem.getprevious().tag in [n + 'add', n + 'unclear']:
            if punctElem.getprevious().find(n + 'w') is not None and len(punctElem.getprevious().find(n + 'w')) == 0:
                # If <add> or <unclear> have a <w> child and this <w> has no children (<lb> or <choice>)
                punctElem.getprevious().find(n + 'w').text = punctElem.getprevious().find(n + 'w').text + v
                punctElem.getprevious().find(n + 'w').text = punctElem.getprevious().find(n + 'w').text.replace('\n', '')
                punctElem.getprevious().find(n + 'w').text = punctElem.getprevious().find(n + 'w').text.replace('\t', '')
                punctElem.getparent().remove(punctElem)
            elif punctElem.getprevious().find(n + 'w') is not None and len(punctElem.getprevious().find(n + 'w')) > 0:
                # If the previous <w> has children (<lb> or <choice>, it's best to leave the <pc> as it is)
                pass
            else:
                print('Alas! Childless element <' + punctElem.getprevious().tag + '>')
                punctElem.getprevious().set('type', 'trouble')

##################################
# Take care of specific elements #
##################################

for i in ['note', 'abbr', 'pb', 'milestone']:
    deleteAllElements(i, n)

for cb in tree.findall('.//' + n + 'cb'):
    ocn = cb.get('n')   # Old Column @n
    ncn = 'Column_' + ocn   # New Column @n
    cb.set('n', ncn)

substituteAllElements('cb', 'pb', n) # § to-do: if <anchor> generates an empty space, change this to <span>

#######################
# Manage <w> and <pc> # 
#######################

for ab in root.findall(n + 'text/' + n + 'body/' + n + 'ab'):   # All 'ab' elements (children of <body>)

    # Insert an <ab type="added_heading"> with the title of the section (that I made up)
    newHead = etree.Element('ab')
    newHead.text = '[' + ab.get('n') + ']'
    newHead.tail = '\n'
    newHead.set('type', 'added_heading')
    newHead.set('rend', 'bold')
    previousPosition = ab.getparent().index(ab)  # This is an integer representing the previous position in <body>
    ab.getparent().insert(previousPosition, newHead)

    for ref in ab: # Iterate over the <ref> children of <ab>
        for w in ref: # Iterate over word-like elements (such as <w>, <gap>, <pc> etc.)
            wt = etree.QName(w).localname   # The tag name w/o namespace (e.g.: 'w', 'pc' etc.)
            if wt == 'w':
                manageWord(w)
            elif wt == 'add':
                # Possible children of 'add' are:     w, pc, gap (it may have more than one child)
                for c in w:
                    if c.tag == n + 'w':
                        manageWord(c)
                    elif c.tag == n + 'pc':
                        #pass
                        managePunctuation(c)
                    elif c.tag == n + 'milestone':
                        pass
            elif wt == 'unclear':    
                # Possible children of 'unclear' are: only 'w'
                unWord = w.find(n + 'w')
                manageWord(unWord)
            elif wt == 'anchor':    
                print('I found an <anchor>')
            elif wt == 'pc':
                managePunctuation(w)
            else:
                pass


    These are the possible @n <pc>s children of <ref>:
        0
        .
        question
        space
        ,
        quote

    Possible element children of <w>:
        {http://www.tei-c.org/ns/1.0}gap    # This is OK: leave it where it is
	{http://www.tei-c.org/ns/1.0}anchor # This is OK: leave it where it is
	{http://www.tei-c.org/ns/1.0}pc     # Delete this, if it's only n="space"
	{http://www.tei-c.org/ns/1.0}choice # Extract the text
	{http://www.tei-c.org/ns/1.0}add    # Extract the text

    this is the new list of world-like elements, possible children of <ref>:
            milestone   # leave it
            gap         # leave it
            anchor      # leave it (it occurs only once)
            unclear
            pc
            span

    This was the original the list of word-like elements, possible children of <ref>:
        {http://www.tei-c.org/ns/1.0}lb     # Turn into <anchor>... or just delete
        {http://www.tei-c.org/ns/1.0}cb     # same as above, but possibly anchor
        {http://www.tei-c.org/ns/1.0}pb     # same as above, but possibly anchor
        {http://www.tei-c.org/ns/1.0}pc     # Use @n as text content
        {http://www.tei-c.org/ns/1.0}note   # Replicate? Nope, delete
        {http://www.tei-c.org/ns/1.0}milestone  # Replicate?
        {http://www.tei-c.org/ns/1.0}w      # Replicate
        {http://www.tei-c.org/ns/1.0}anchor # Replicate
        {http://www.tei-c.org/ns/1.0}add
        {http://www.tei-c.org/ns/1.0}unclear
        {http://www.tei-c.org/ns/1.0}gap
    
tree.write('ALIM2_publication/casanatensis_AL.xml', encoding='UTF-8', method='xml', xml_declaration=True)
