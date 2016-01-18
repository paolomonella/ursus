# ursus

Digital scholarly edition of the IX century Latin grammatical works found in manuscript Casanatensis 1086 and mostly written by Ursus from Benevento.

## Key files for the editition

* casanatensis.xml: the source XML/TEI transcription of the manuscript
* GToS.csv: the table of signs of the graphematic layer of the edition (a very important part of this edition)
* AToS.csv: the table of signs of the alphabetic layer of the edition

## Visualization of the edition

* jsparser.js: the JavaScript code that transforms the XML/TEI transcription (casanatensis.xml) and turns it into a DOM visible on a browser
* transcription.html: the HMTL file in which, thanks to jsparser.js, the user can read the edition
* stylesheet.css: the CSS stylesheet for transcription.html
* sheet.xsl: a first experiment in creating a XSLT file to visualize the XML/TEI source (casanatensis.xml). I then abandoned XSLT and used JavaScript instead (see jsparser.js)

## Documentation and other

* documentation.md: The full documentation on this edition
* glyph_images: this folder includes jpeg images of the glyphs found in the manuscript
* lemma: this folder includes my experiments with lemmatization/POS (part of speech) tagging
* paoloMarkDown.py: some Python code facilitating my work of keying the XML/TEI transcription of the manuscript
