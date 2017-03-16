#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script turns my own 'paolomarkdown' conventions into XML/TEI for the digital edition
# of manuscript Casanatensis 1086.
# It's written in Python 3.4, but also works with Python 2.7
#
# Warning: when writing in 'paolomarkdown', note that every string at the beginning
# of the line that does not start with '<' or end with '>'
# will be substituted by this script with
# <w ana="string">string</w>
# So, if this is not intended, every alphanumerical string that must not be substituted
# should start with whitespace, such as tab or space(s)

from __future__ import print_function
import datetime
import shutil
import zipfile
import os
import re
import xml.etree.ElementTree as ET

# Clear screen
#os.system('clear')

# The namespaces
t    = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
xml   = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
#ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
ns = {'tei': 'http://www.tei-c.org/ns/1.0',             # for TEI XML
        'xml': 'http://www.w3.org/XML/1998/namespace'}  # for attributes like xml:id

# Parse the tree
tree = ET.parse('casanatensis.xml')
#root = tree.getroot()


def manageWordLikeElem(elem):
    ow.append(elem.tag)

#for e in tree.findall('.//' + '*', ns):
ow = [] # Other word-like elements
for ab in tree.findall('.//' + t + 'ab'):
    # § Replicate in output xml
    for ref in ab: # Iterate over the <ref> children of <ab>
        for w in ref: # Iterate over word-like elements (such as <w>, <gap>, <pc> etc.)
            manageWordLikeElem(w)

"""
This is the list of word-like elements, possible children of <ref>:
{http://www.tei-c.org/ns/1.0}lb     # Replicate
{http://www.tei-c.org/ns/1.0}cb     # Replicate
{http://www.tei-c.org/ns/1.0}pb     # Replicate
{http://www.tei-c.org/ns/1.0}pc     # Use @n
{http://www.tei-c.org/ns/1.0}note   # Replicate?
{http://www.tei-c.org/ns/1.0}milestone  # Replicate?
{http://www.tei-c.org/ns/1.0}w      # Replicate?
{http://www.tei-c.org/ns/1.0}anchor # Ignore
{http://www.tei-c.org/ns/1.0}add
{http://www.tei-c.org/ns/1.0}unclear
{http://www.tei-c.org/ns/1.0}gap

"""
for o in set(ow):
    print(o)

"""
    if word.get(nx + 'id'):
        idstring = word.get(nx + 'id')
        idcount  = int(idstring[1:])
    else:
        idcount  = idcount + 3
        idstring = 'w' + str(idcount)
        word.set(nx + 'id', 'w' + str(idcount))

# Quando risolvo il problema, devo de-commentare la riga seguente:
tree.write('output.xml', encoding="UTF-8", method="xml")

############################################
# Check that all IDs are sequential so far #
############################################

# ... and if there are words without an ID still

# Parse the tree
tree = ET.parse('output.xml')

idcount = 0
for word in tree.findall('.//' + n + 'w'):
    if word.get(nx + 'id'):
        idstring = word.get(nx + 'id')
        old_idcount  = idcount
        idcount  = int(idstring[1:])
        if idcount > old_idcount:
            #print(str(idcount) + ' > ' + str(old_idcount))
            pass
        else:
            print('Nuovo counter: ' + str(idcount) + '. Counter precedente: ' + str(old_idcount))




"""
