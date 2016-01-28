# !/usr/bin/env python
# This is a toolbox I'm using to look for specific thinks in the XML DOM
from xml.dom.minidom import parse, parseString
#import xml.dom.minidom
xmldoc = parse('/home/ilbuonme/siti/paolo.monella/ursus/casanatensis.xml')
wordElementList = xmldoc.getElementsByTagName('ref')
for r in wordElementList:
    print('cRef: '+r.attributes.getNamedItem('cRef').nodeValue)
    for c in r.childNodes:
        if c.nodeType == c.ELEMENT_NODE:
            if (c.tagName == 'ref'):
                print('Eureka!')
