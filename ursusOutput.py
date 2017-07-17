#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script simplifies the encoding of casanatensis.xml
# and creates a file ALIM2_publication/casanatensis_AL.xml
# with the Alphabetic Layer only. 
#
# It's written in Python 3.4. If one runs it with Python 2.7,
# it raises a Unicode-related exception.
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

# General variables

# Parse the tree of casanatensis.xml
casanaTree = etree.parse('casanatensis.xml')
# Parse the tree of the ALIM2 template: it will be the base for the output tree
no_blank = False
if no_blank:
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse('ALIM2_publication/teiHeader_template.xml', parser)
else:
    tree = etree.parse('ALIM2_publication/teiHeader_template.xml')

# tree = etree.parse('ALIM2_publication/teiHeader_template.xml') # It works

root = tree.getroot()
#root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

# Append the <body> of casanatensis.xml into <text> of the output xml file
myBody = casanaTree.getroot().find(n + 'text').find(n + 'body')
myText = root.find(n + 'text')        # <text> of output xml file
myText.append(myBody)

"""
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
"""


#############
# Functions #
#############

def deleteAllElements(myElemName, myNameSpace):
    """ Delete all elements with name myElemName
        and namespace myNameSpace. This function could be
        re-written better now that I'm using lxml, but
        it words, so it's OK.
    """
    search = ('.//{0}' + myElemName).format(myNameSpace)
    my_elem_parents = tree.findall(search + '/..')
    for x in my_elem_parents:
        for y in x.findall(myNameSpace + myElemName):
            x.remove(y)

def substituteAllElements(oldName, newName, myNameSpace):
    """ Substitute all elements with base name oldName and
        namespace myNameSpace with elements with name newName:
        <cb n="1r.1"> becomes
        <pb n="1r.1" type="cb">
    """
    for x in tree.findall('.//' + myNameSpace + oldName):
        x.tag = myNameSpace + newName
        x.set('type', oldName)

def manageWord(wordElem):
    # print('Working on word\t' + wordElem.get(xml + 'id')) # debug
    # Easy solution (only backdraw: it moves all elements children of <w> after the text). This is
    # OK (it's actually better) for 'anchor/pb/cb/lb', but it creates a slight inaccuracy with 'gap':
    tempText = wordElem.xpath('normalize-space()').replace(' ', '').replace('·', '') # This is the unified text of the word
    if wordElem.get('type') in ['alphabemes', 'foreign', 'ancientAbbreviation']:
        tempText = '"' + tempText + '"'
    for y in wordElem:
        yt = etree.QName(y).localname
        if yt in ['choice', 'add', 'pc', 'hi']:    # I'm removing them b/c they include text, or b/c it's <pc n="space">
            y.getparent().remove(y)
        y.tail = None
    tempText = tempText.replace('æ', 'ae') # The alphabetic meaning of graphemes 'æ' are alphabemes 'ae'
    """ N.B.: In jsparser.js I'm using a function alph() to replace each grapheme with its alphabetic meaning
        based on the GToS. I'm not doing it here for brevity, since all graphemes outside <abbr> correspond
        to the alphabeme encoded with the same Unicode character, except for grapheme 'æ', so I'm just replacing
        'æ' with 'ae' in the line above. """
    wordElem.text = tempText.replace(' ', '')
    """
    # Complicated solution, not completely functional:
    for y in wordElem:
        yt = etree.QName(y).localname
        if yt == 'choice':
            # I'm changing this from <choice><expan>um</expan></choice> to 
            # <expan>um</expan>
            expan = y.find(n + 'expan')
            expanText = expan.text
            y.remove(expan) # Remove the original child <expan>
            y.text = expanText
            #y.tag = n + 'expan' # Transform the parent <choice> to <expan> (...or to <span>, in the future?)
        if y.tag == n + 'gap':
            print('Gap within the word: ' + wordElem.get(xml + 'id'))
    """

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
        """
        Possible elements that are the previous sibling:
            lb          jump to previous
            milestone   jump to previous
            gap         jump to previous
            w           
            add         jump to its last <w> child
            unclear     jump to its last <w> child
        """



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



##########################################################################
# Traverse the tree and manage <w>, <pc> and all other children of <ref> # 
##########################################################################

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
        for w in ref:   # Iterate over children of <ref>, i.e. word-like elements (such as <w>, <gap>, <pc> etc.)
                        # or parents of <w> such as that <add>, <unclear>, <choice>/<sic>/<corr> etc.
            wt = etree.QName(w).localname   # The tag name w/o namespace (e.g.: 'w', 'pc' etc.)
            if wt == 'w':
                manageWord(w)
            elif wt == 'add':
                # Possible children of 'add' are:     w, pc, gap (it may have more than one child)
                for c in w:
                    if c.tag == n + 'w':
                        manageWord(c)
                    elif c.tag == n + 'pc':
                        managePunctuation(c)
                    elif c.tag == n + 'milestone':
                        pass
                    """
                    if len(w) > 1:
                        print(c.tag)
                if len(w) > 1:
                    print('\n---\n')
                    """
            elif wt == 'unclear':    
                # Possible children of 'unclear' are: only 'w'
                unWord = w.find(n + 'w')
                manageWord(unWord)
            elif wt == 'anchor':    
                print('I found an <anchor>')
            elif wt == 'pc':
                managePunctuation(w)
            elif wt == 'choice':    # Since this <choice> is child of <ref>, then it must be parent of <sic> and <corr>
                if w.find(n + 'sic').find(n + 'w') is not None: # <sic> always has one <w> child only
                    mySicWord = w.find(n + 'sic').find(n + 'w')
                    manageWord(mySicWord)
                if w.find(n + 'corr').findall(n + 'w') is not None:
                    for myCorrWord in w.find(n + 'corr').findall(n + 'w'):      # <corr> may have more than one <w> child
                        manageWord(myCorrWord)
            else:
                pass



"""
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
    
    """

tree.write('ALIM2_publication/casanatensis_AL.xml', encoding='UTF-8', method='xml', xml_declaration=True)
