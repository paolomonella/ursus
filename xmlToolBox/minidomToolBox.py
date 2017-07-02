#! /usr/bin/env python
# This is a toolbox I'm using to look for specific things in the XML DOM

##################
# Import modules #
##################

from __future__ import print_function
from xml.dom.minidom import parse, parseString
#import xml.dom.minidom


#################
# Parse the XML #
#################

xmldoc=parse('/home/ilbuonme/siti/paolo.monella/ursus/casanatensis.xml')


###########
# Methods #
###########

def checkIDs():
    """
    This function checks whether there are duplicated or
    non-sequential xml:id's for <w> elements.
    """
    wordElementList = xmldoc.getElementsByTagName('ref')
    prevIdN = 0
    for r in wordElementList:
        #print('cRef: '+r.attributes.getNamedItem('cRef').nodeValue)
        for c in r.childNodes:
            if c.nodeType == c.ELEMENT_NODE and c.tagName == 'w':
                #print(c.attributes.getNamedItem('xml:id').nodeValue, end=', ')
                myId = c.attributes.getNamedItem('xml:id').nodeValue
                myIdN = int(myId[1:])
                #print(myIdN, end=', ')
                if not myIdN > prevIdN:
                    print('Trouble! Not greater...')
                    #print(myIdN, 'is greater than ', prevIdN)
                if myIdN == prevIdN:
                    print('Trouble! Equal')

def searchPcChildrenOfUnclear():
    """
    Print all <pc> elments that are children of <unclear>.
    """
    wordElementList = xmldoc.getElementsByTagName('ref')
    x = False
    for r in wordElementList:
        #print('cRef: '+r.attributes.getNamedItem('cRef').nodeValue)
        for c in r.childNodes:
            if c.nodeType == c.ELEMENT_NODE:
                if c.tagName == 'w' and x:
                    print(c.attributes.getNamedItem('xml:id').nodeValue, end=' viene dopo ')
                    x = False
                if c.tagName == 'unclear':
                    for w in c.childNodes:
                        #print(x, end=', ')
                        if w.nodeType == w.ELEMENT_NODE and w.tagName == 'pc':
                            print('Eureka!')
                            print(w.attributes.getNamedItem('n').nodeValue)
                            x = True

def searchTextNodesChildrenOfUnclear():
    """
    Print all textNodes that are children of <unclear>.
    """
    wordElementList = xmldoc.getElementsByTagName('ref')
    for r in wordElementList:
        #print('cRef: '+r.attributes.getNamedItem('cRef').nodeValue)
        for c in r.childNodes:
            if c.nodeType == c.ELEMENT_NODE:
                if c.tagName == 'unclear':
                    for w in c.childNodes:
                        if w.nodeType == w.ELEMENT_NODE and w.tagName != 'w':
                            #print(w.attributes.getNamedItem('n').nodeValue)
                            print(w.tagName)
                        if w.nodeType != w.ELEMENT_NODE and w.nodeValue != '\n' and w.nodeValue != '\n\t':
                            print('"'+w.nodeValue+'"\n---\n')

def listChildrenOfAnElement(elemName):
    """
    Return a list of elements that are direct children of the
    element with tag name elemName (e.g. 'w' or 'ref').
    """
    wordElementList = xmldoc.getElementsByTagName(elemName)
    cs=[]
    for e in wordElementList:
        for c in e.childNodes:
            if c.nodeType == c.ELEMENT_NODE:
                cs.append(c.tagName)
    return(set(cs))

def searchAttrib(elemName):
    """
    Check attributes of an element
    """
    L = []
    wordElementList = xmldoc.getElementsByTagName(elemName)
    for e in wordElementList:
        if e.attributes.getNamedItem('type'):
            n = e.attributes.getNamedItem('type').nodeValue
            if  n == 'emendation':
                if not e.attributes.getNamedItem('cert'):
                    L.append(e.attributes.getNamedItem('subtype').nodeValue)
                    #L.append(e.attributes.getNamedItem('subtype').nodeValue)
    for l in set(L):
        print(l)



def listDescendantsOfElement(myElement):
    ds=[]
    elementList = xmldoc.getElementsByTagName(myElement)
    for w in elementList:
        d = w.getElementsByTagName('*')
        for x in d:
            #if x.nodeType == x.ELEMENT_NODE and x.tagName != 'note':
            if x.nodeType == x.ELEMENT_NODE:
                ds.append(x.tagName)
    for y in set(ds):
        print(y)

def graphemeLint():
    """
    This function checks that all graphemes encoded directly within
    <w> elements (or within those of its descendant element that are
    supposed to include graphemes) are actually declared in the
    Graphemic Table of Signs. If they are not declared, it prints
    an 'Alas!' message.
    """

    # Import the graphemes in column 'Grapheme' of GToS.csv into list 'gl'
    gl = []
    with open('/home/ilbuonme/siti/paolo.monella/ursus/GToS.csv') as gtosFile:
        lineCount=0
        for l in gtosFile:
            if lineCount>0: # I'm skipping the first line (which has the column headers)
                gl.append(l[0])
            lineCount += 1

    # Possible descendants of <w>
    allowedElem=['lb', 'pc', 'am', 'choice', 'note', 'expan', 'add', 'hi', 'abbr', 'gap']
    noGraphemeContent=['lb', 'pc', 'gap', 'note', 'expan', 'choice'] # <expan> has alphabemes, not graphemes, as content
    graphemeContent=['am', 'hi']

    # Check the descendants of <w> (elements and textNodes)
    elementList = xmldoc.getElementsByTagName('w')
    for w in elementList:
        g = '' # This is a string including all graphemes in the <w> element
        for c in w.childNodes:
            if c.nodeType != c.ELEMENT_NODE: # With this we harvest all text nodes directly children of <w>
                g = g + c.nodeValue
        for x in w.getElementsByTagName('*'):
            if x.tagName not in allowedElem:
                print('<' + x.tagName + '> is not allowed as a descendant of <w>')
            elif x.tagName in graphemeContent: # These elements only have one textNode child, with graphemes
                g = g + x.firstChild.nodeValue
            elif x.tagName == 'abbr': # Its children can be <am> or <hi> (already taken care of), or textNode 
                for y in x.childNodes:
                    if y.nodeType != y.ELEMENT_NODE: # textNode child
                        g = g + y.nodeValue
                    else:   # element child: the only case as of 2017-03-16 is a <choice> child, so
                            # no need to worry about this, because its children <abbr>, <expan>
                            # and <am> are already taken care of
                        pass
            elif x.tagName == 'add': # Its children can be <w> or textNode 
                for y in x.childNodes:
                    if y.nodeType != y.ELEMENT_NODE: # textNode child
                        g = g + y.nodeValue
                    else:   # element child: the only case as of 2017-03-16 is a <choice> child, so
                            # no need to worry about this, because its children <abbr>, <expan>
                            # and <am> are already taken care of
                        pass

        for gx in g:            # For each character in the graphematic content of <w>
            if (gx not in gl) and (gx not in ['\n', '\t']):    # If it's not in the GToS (and it's not a tab or newline)
                print('Alas! Character "'+gx+'" is not in the Graphemic Table of Signs')
                


##################
# Call functions #
##################

# List children of <w>
# for x in listChildrenOfAnElement('w'): print(x, end=', ')
# print()

# List descendants of <w>
#graphemeLint()
#listDescendantsOfElement('choice')
searchAttrib('note')
