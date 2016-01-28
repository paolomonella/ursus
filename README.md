# ursus

Digital scholarly edition of the IX century Latin grammatical works found in manuscript Casanatensis 1086 and mostly written by Ursus from Benevento.

Full documentation in `documentation.md`.

## Source files

* `AToS.csv`: the table of signs of the Alphabetic Layer of the edition
* `GToS.csv`: the table of signs of the Graphematic Layer of the edition (a key part of this edition)
* `casanatensis.xml`: the source XML/TEI transcription of the manuscript (the heart of this edition)

## Visualization

* `jsparser.js`: the JavaScript to visualize `casanatensis.xml` in a browser
* `sheet.xsl`: a first experiment in creating a XSLT file to visualize `casanatensis.xml` in a browser. I then abandoned XSLT and used JavaScript instead (see `jsparser.js`)
* `stylesheet.css`: the CSS stylesheet for `transcription.html`
* `transcription.html`: the HMTL file in which, thanks to `jsparser.js`, the user can read the edition

## Other

* `glyph_images`: this folder includes jpeg images of the glyphs found in the manuscript
* `lemma`: this folder includes my experiments with lemmatization/POS (part of speech) tagging
* `minidomToolBox`: this folder includes the script that I'm using to traverse the DOM of `casanatensis.xml`
* `documentation.md`: The full documentation on this edition
* `paoloMarkDown.py`: a Python script facilitating my work of keying in `casanatensis.xml`
