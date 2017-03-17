#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script simplifies the encoding of casanatensis.xml
# and creates a file casanatensis_AL.xml with the Alphabetic
# Layer only. 
# It's written in Python 3.4, but also works with Python 2.7
# To-do: continue checking elements and dealing with them
#   - <pc> has annoying space before
#   - <lb> also leaves a blank space

from __future__ import print_function
import datetime
import shutil
import zipfile
import os
import re
import xml.etree.ElementTree as ET

# Clear screen
os.system('clear')

# Namespaces
n = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
xml = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
ns = {'tei': 'http://www.tei-c.org/ns/1.0',             # for TEI XML
        'xml': 'http://www.w3.org/XML/1998/namespace'}  # for attributes like xml:id

# Parse the tree of casanatensis.xml
casanaTree = ET.parse('casanatensis.xml')
# Parse the tree of the ALIM2 template: it will be the base for the output tree
tree = ET.parse('ALIM2_publication/teiHeader_template.xml')
root = tree.getroot()
root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

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
# Substitute/delete specific elements #
#######################################

# Turn <lb>, <cb> and <pb> into anchors
for x in ['lb', 'cb', 'pb']:    
    for br in tree.findall('.//' + n + x):
        br.tag = 'anchor'

# Delete all elements with name 'myElemName' and namespace myNameSpace. 
def deleteAllElements(myElemName, myNameSpace):
    search = ('.//{0}' + myElemName).format(myNameSpace)
    my_elem_parents = tree.findall(search + '/..')
    for x in my_elem_parents:
        for y in x.findall(myNameSpace + myElemName):
            x.remove(y)
            #print(y.tag)

deleteAllElements('note', n)

for pc in tree.findall('.//' + n + 'pc'):
    if pc.get('n') != '0':
        pc.text = pc.get('n').replace('question', '?').replace('quote', '"').replace('space', ' ')

"""
for x in ['note']: # I'm making this a list, just in case I want to get rid of more elements
    for br in tree.findall('.//' + n + x):
        #print(br.find('..'))
        print(.//{0}prop.format(n))
        """

"""
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
tree.write('ALIM2_publication/casanatensis_AL.xml', encoding='UTF-8', method='xml')
