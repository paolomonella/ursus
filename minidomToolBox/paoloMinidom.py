# !/usr/bin/env python
# This is a toolbox I'm using to look for specific things in the XML DOM
from xml.dom.minidom import parse, parseString
#import xml.dom.minidom
xmldoc = parse('/home/ilbuonme/siti/paolo.monella/ursus/casanatensis.xml')
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
