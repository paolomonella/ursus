# Import modules

# For CLTK
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag

mydir = '/home/ilbuonme/travaglio/2018\ kore/schede_libro/latini/'

# Initialize CLTK
lemmatizer = LemmaReplacer('latin')
tagger = POSTag('latin')
j = JVReplacer()

# Input file

infile = '%sin.txt' % mydir

with open (infile, 'r') as IN:
    j = infile.read()

try:
    posList   = tagger.tag_tnt(j.replace(form.lower()))
    print(posList)
    pos = posList[0][1]
except:
    raise

"""
with open('output.xml', 'w') as f:
    f = codecs.lookup("utf-8")[3](f)
    xmldoc.writexml(f, encoding="utf-8")
"""

'''
f = open('%scltkout.txt' % mydir, 'w')
#f = codecs.lookup("utf-8")[3](f)
#xmldoc.writexml(f, encoding="utf-8")
f.close()
'''
