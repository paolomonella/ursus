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
from lxml import etree as ET

# Clear screen
os.system('clear')

# Namespaces
n = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
xml = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
#ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')   # This used to work when I used ElementTree
ns = {'tei': 'http://www.tei-c.org/ns/1.0',             # for TEI XML
        'xml': 'http://www.w3.org/XML/1998/namespace'}  # for attributes like xml:id

# Parse the tree of casanatensis.xml
casanaTree = ET.parse('casanatensis.xml')
# Parse the tree of the ALIM2 template: it will be the base for the output tree
tree = ET.parse('ALIM2_publication/teiHeader_template.xml')
root = tree.getroot()
#root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

# Append the <body> of casanatensis.xml into <text> of the output xml file
myBody = casanaTree.getroot().find(n + 'text').find(n + 'body')
myText = root.find(n + 'text')        # <text> of output xml file
myText.append(myBody)

#############
# Functions #
#############

def manageWordLikeElem(w):
    pass



#######################
# Traverse the <body> # 
#######################

#for e in tree.findall('.//' + '*', ns):
for ab in tree.findall('.//' + n + 'ab'):
    # Insert a <head> with the title of the section
    if ab.get('n'):
        newHead = ET.Element('head')
        newHead.text = ab.get('n')
        ab.insert(0, newHead)
    for ref in ab: # Iterate over the <ref> children of <ab>
        for wLike in ref: # Iterate over word-like elements (such as <w>, <gap>, <pc> etc.)
            manageWordLikeElem(wLike)

#######################################
# Delete/substitute specific elements #
#######################################

def deleteAllElements(myElemName, myNameSpace):
    """ Delete all elements with name myElemName
        and namespace myNameSpace. 
    """
    search = ('.//{0}' + myElemName).format(myNameSpace)
    my_elem_parents = tree.findall(search + '/..')
    for x in my_elem_parents:
        for y in x.findall(myNameSpace + myElemName):
            x.remove(y)

def substituteAllElements(myElemName, newElemName, myNameSpace):
    """ Substitute all elements with name myElemName and
        namespace myNameSpace with elements with name newElemName.
    """
    for x in tree.findall('.//' + myNameSpace + myElemName):
        x.tag = newElemName

for i in ['note', 'hi']:
    deleteAllElements(i, n)

for i in ['lb', 'cb', 'pb']:    
    # § to-do: if <anchor> generates an empty space, change this to <span>
    substituteAllElements(i, n + 'anchor', n)

#for i in ['add']:    
    #substituteAllElements(i, 'span', n)

# Manage <add>s children of <ref>
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

wt = []
for w in tree.findall('.//' + n + 'w'):
    s = ''  # The string of characters of that word at the AL
    """ Possible children of <w>:
        {http://www.tei-c.org/ns/1.0}gap    # This is OK: leave it
	{http://www.tei-c.org/ns/1.0}anchor # This is OK: leave it
	{http://www.tei-c.org/ns/1.0}pc
	{http://www.tei-c.org/ns/1.0}choice
	{http://www.tei-c.org/ns/1.0}add
	"""
    cc = list(w) # Children of w
    for c in cc:
        if c.tag != '':
            #print(c.text, end=', ').strip()
            #print(c.localname, end=', ')
            print(ET.QName(c).localname, end=', ')
    # §§§ To-do: how do I find out it it's a text node
    # or an element node?

    """
    abbr = w.findall(n + '*')
    if len(abbr) == 0:
        print(abbr)
        """


"""
searchBis = './/' + n + 'add'
#searchBis = './/{1}add'.format(n)
for x in tree.findall(searchBis):
    my_parent = x.find('../')
    if my_parent:
        print(my_parent.tag)
    if my_parent.tag == n + 'ref':
        print('The parent is    ref')
    elif my_parent.tag == n + 'w':
        print('the parent is    w')
    #x.tag = newElemName
    """

# END OF THE WORD





def remove_whitespace_nodes(node, unlink=False):
    """Removes all of the whitespace-only text decendants of a DOM node.
    
    When creating a DOM from an XML source, XML parsers are required to
    consider several conditions when deciding whether to include
    whitespace-only text nodes. This function ignores all of those
    conditions and removes all whitespace-only text decendants of the
    specified node. If the unlink flag is specified, the removed text
    nodes are unlinked so that their storage can be reclaimed. If the
    specified node is a whitespace-only text node then it is left
    unmodified."""
    
    remove_list = []
    for child in node.childNodes:
        if child.nodeType == dom.Node.TEXT_NODE and \
           not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whilespace_nodes(child, unlink)
    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()

"""


for x in tree.findall('.//{0}add'.format(n)):
    aoa.append(x.get('place'))


temp = open('temp.txt', 'w')
for pc in tree.findall('.//' + n + 'pc'):
    if pc.get('n') != '0':
        pc.text = pc.get('n').replace('question', '?').replace('quote', '"').replace('space', ' ')
        if pc.tail and pc.tail != '\n' and pc.tail != '\n\t':
            #print('«' + pc.tail + '»\n---', file=temp)
            if pc.find('..'):
                print(pc.find('..'))
temp.close()


This is the list of word-like elements, possible children of <ref>:
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
