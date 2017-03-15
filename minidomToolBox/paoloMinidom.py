# !/usr/bin/env python
# This is a toolbox I'm using to look for specific things in the XML DOM
from xml.dom.minidom import parse, parseString
#import xml.dom.minidom
xmldoc = parse('/home/ilbuonme/siti/paolo.monella/ursus/casanatensis.xml')
wordElementList = xmldoc.getElementsByTagName('ref')
x = False
for r in wordElementList:
    #print('cRef: '+r.attributes.getNamedItem('cRef').nodeValue)
    for c in r.childNodes:
        if c.nodeType == c.ELEMENT_NODE:
            if c.tagName == 'w' and x:
                print(c.attributes.getNamedItem('xml:id').nodeValue, end=' è la parola che viene dopo ')
                x = False
            if c.tagName == 'unclear':
                for w in c.childNodes:
                    #print(x, end=', ')
                    if w.nodeType == w.ELEMENT_NODE and w.tagName == 'pc':
                        print('Eureka!')
                        print(w.attributes.getNamedItem('n').nodeValue)
                        x = True
