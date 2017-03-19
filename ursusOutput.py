#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script simplifies the encoding of casanatensis.xml
# and creates a file ALIM2_publication/casanatensis_AL.xml
# with the Alphabetic Layer only. 
#
# It's written in Python 3.4, but also works with Python 2.7
# To-do: continue checking elements and dealing with them
#   - <pc> has annoying space before
#   - <lb> also leaves a blank space
#       - but probably it'll be better to take care of this
#         after improving the management of <w> (I could
#         dispose of <w> altogether)
#   - check the space before <add> too.

from __future__ import print_function
import datetime
import shutil
import zipfile
import os
import re
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
foo = []    # § sgn: needed for debugging

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

#############
# Functions #
#############




#######################################
# Delete/substitute specific elements #
#######################################

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


for i in ['note', 'abbr', 'pb']:
    deleteAllElements(i, n)

substituteAllElements('cb', 'pb', n) # § to-do: if <anchor> generates an empty space, change this to <span>

"""
for wrapper in tree.findall('.//' + n + 'unclear'): [MORE RECENT CODE, BUT USELESS]
    Substitute <add> and <unclear> that are children of <ref>
        with <span type="add"> and <span type="unclear">.
        Possible children of 'unclear' are: only 'w'
        Possible children of 'add' are:     w, pc, gap
    if wrapper.getparent().tag == n + 'ref':
        wrapper
        for u in wrapper:   # The children of 'add'
            uName = etree.QName(u).localname
            foo.append(etree.QName(u).localname) # The tag name w/o namespace (e.g.: 'w', 'pc' etc.)

# Manage <add>s children of <ref> [OLD CODE]
mysearch = ('.//{0}' + 'add').format(n)
my_elem_parents = tree.findall(mysearch + '/..')
for x in my_elem_parents:
    for y in x.findall(n + 'add'):
        # x is the <ref> or <w> parent, y is the <add> child
        if x.tag == n + 'w':    # if <w>/<add>...
            pass # § To do: add its text content to <w>'s content...
                 # ... or, possibly better, manage this when managing
                 # the content of each <w>
        elif x.tag == n + 'ref': # if <ref>/<add>, change <add> to <span>
            y.tag = n + 'span'
"""

#######################
# Manage <w> and <pc> # 
#######################

for ab in root.findall(n + 'text/' + n + 'body/' + n + 'ab'):   # All 'ab' elements (children of <body>)

    """
    # Insert a <head> with the title of the section
    newHead = etree.Element('span')
    newHead.text = ab.get('n')
    newHead.set('rend', 'bold')
    ab.insert(0, newHead)
    """

    for ref in ab: # Iterate over the <ref> children of <ab>
        for w in ref: # Iterate over word-like elements (such as <w>, <gap>, <pc> etc.)
            #manageWordLikeElem(wLike)
            wt = etree.QName(w).localname   # The tag name w/o namespace (e.g.: 'w', 'pc' etc.)
            if wt == 'w':
                # Easy solution (only backdraw: it moves all elements children of <w> after the text). This is
                # OK (it's actually better) for 'anchor/pb/cb/lb', but it creates a slight inaccuracy with 'gap':
                tempText = w.xpath('normalize-space()').replace(' ', '') # This is the unified text of the word
                for y in w:
                    yt = etree.QName(y).localname
                    if yt in ['choice', 'add', 'pc', 'hi']:    # I'm removing them b/c they include text, or b/c it's <pc n="space">
                        y.getparent().remove(y)
                    y.tail = None
                w.text = tempText

                """
                # Complicated solution, not completely functional
                for y in w:
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
                        print('Gap within the word: ' + w.get(xml + 'id'))
                """
            elif wt == 'anchor':    # These anchors come from <pb>, <cb> or <lb> and have @type="pb", @type="cb" etc.
                pass
            elif wt == 'pc':
                z = [wt, w.attrib]
                v = w.get('n')
                if v in ['0', 'quote', 'space']: # Delete <pc>
                    ref.remove(w)
                elif v in ['.', 'question', ',']:   # Append to the text content of previous <w>
                    v = v.replace('question', '?')
                    if w.getprevious().tag in [n + 'lb', n + 'milestone', n + 'gap']:
                        # Just give up and leave the <pc> element as it is
                        if w.getprevious().tag != n + 'gap':
                            print('Alas! Punctuation sign not coming immediately after <w> or <gap>')
                            w.set('type', 'trouble')
                    elif w.getprevious().tag == n + 'w': # If previous sibling is <w>, append punctuation to its textual content
                        w.getprevious().text = w.getprevious().text + v
                        #w.getprevious().tail = v + '\n' # Nope: this generates code like
                                                         # <w n="dicam" xml:id="w564">dicam<lb n="1r.a.23" break="no"/></w>,
                        ref.remove(w)
                    elif w.getprevious().tag in [n + 'add', n + 'unclear']:
                        if w.getprevious().find(n + 'w') is not None and len(w.getprevious().find(n + 'w')) == 0:
                            # If <add> or <unclear> have a <w> child and this <w> has no children (<lb> or <choice>)
                            w.getprevious().find(n + 'w').text = w.getprevious().find(n + 'w').text + v
                            w.getprevious().find(n + 'w').text = w.getprevious().find(n + 'w').text.replace('\n', '')
                            w.getprevious().find(n + 'w').text = w.getprevious().find(n + 'w').text.replace('\t', '')
                            #print(w.getprevious().find(n + 'w').text)
                        elif w.getprevious().find(n + 'w') is not None and len(w.getprevious().find(n + 'w')) > 0:
                            # If the previous <w> has children (<lb> or <choice>, it's best to leave the <pc> as it is)
                            pass
                        else:
                            print('Alas! Childless element <' + w.getprevious().tag + '>')
                            w.getprevious().set('type', 'trouble')
                    #foo.append(pwt) # The tag name w/o namespace (e.g.: 'w', 'pc' etc.)
                    """
                    Possible elements that are the previous sibling:
                        lb          jump to previous
                        milestone   jump to previous
                        gap         jump to previous
                        w           
                        add         jump to its last <w> child
                        unclear     jump to its last <w> child
                    """
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

for f in set(foo):
    print(f)

tree.write('ALIM2_publication/casanatensis_AL.xml', encoding='UTF-8', method='xml', xml_declaration=True)
