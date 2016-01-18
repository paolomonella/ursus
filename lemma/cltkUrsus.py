# To-do:
# - add 'if': only if w doesn't already have a @lemma and (and? or?) a @morph, do parsing
# - possibly add 'clear' after each inflected form
# - report to DC list/wiki



# Import modules

# For XML
from xml.dom.minidom import parse, parseString
import codecs
# For CLTK
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag

# Initialize CLTK
lemmatizer = LemmaReplacer('latin')
tagger = POSTag('latin')
j = JVReplacer()

# Parse XML

xmldoc = parse('/home/ilbuonme/siti/paolo.monella/ursus/casanatensis.xml')
#xmldoc = parse('/home/ilbuonme/siti/paolo.monella/ursus/shorter_casanatensis.xml')
wordElementList = xmldoc.getElementsByTagName('w')

for w in wordElementList:
        form = w.attributes['ana'].value
        print(form)
        # Parse the inflected word
        try:
            lemmaList = lemmatizer.lemmatize(form.lower())
            lemma = lemmaList[0].replace('v', 'u')
            posList   = tagger.tag_tnt(j.replace(form.lower()))
            pos = posList[0][1]
            w.setAttribute('n', form)
            w.setAttribute('lemma', lemma)
            w.setAttribute('ana', pos)
        except:
            raise

"""
with open('output.xml', 'w') as f:
    f = codecs.lookup("utf-8")[3](f)
    xmldoc.writexml(f, encoding="utf-8")
"""

f = open('output.xml', 'wb')
f = codecs.lookup("utf-8")[3](f)
xmldoc.writexml(f, encoding="utf-8")
f.close()
