# Ursus project

An experimental scholarly digital edition of section _De nomine_ (_folia_ 1r-11r) of the _Adbreviatio artis grammaticae_ by Ursus from Benevento from codex [Casanatensis  1086](http://manus.iccu.sbn.it/opac_SchedaScheda.php?ID=15974) (IX century), edited by [Paolo Monella](http://www.unipa.it/paolo.monella) within the [ALIM Project](http://it.alim.unisi.it/) (2016).

To view the edition in your browser, and not just its source code, go to http://www.unipa.it/paolo.monella/ursus/transcription.html

Full documentation in `documentation.md`.

## Source files

* `AToS.csv`: the table of signs of the Alphabetic Layer of the edition
* `GToS.csv`: the table of signs of the Graphematic Layer of the edition (a key part of this edition)
* `casanatensis.xml`: the source XML/TEI transcription of the manuscript (the heart of this edition)
* `lemmatized_casanatensis.xml`: in this version of `casanatensis.xml`, each `<w>` (word) element has a `@lemma` and an `@ana` element to identify it as, for example, the genitive singular of lemma _homo, -inis_ (this is a temporary file as of March 20, 2016: when I'll review the result of the automatic lemmatization, this will become the only version)

## Visualization

* `jsparser.js`: the JavaScript to visualize `casanatensis.xml` in a browser
* `sheet.xsl`: a first experiment in creating a XSLT file to visualize `casanatensis.xml` in a browser. I then abandoned XSLT and used JavaScript instead (see `jsparser.js`)
* `stylesheet.css`: the CSS stylesheet for `transcription.html`
* `transcription.html`: the HMTL file in which, thanks to `jsparser.js`, the user can read the edition. To view this file (and therefore the edition) in your browser, and not just its source code, go to http://www.unipa.it/paolo.monella/ursus/transcription.html 


## Other

* `documentation.md`: The full documentation on this edition
* `glyph_images`: this folder includes jpeg images of the glyphs found in the manuscript
* `lemma`: this folder includes my experiments with lemmatization/POS (part of speech) tagging
* `ursusMarkDown.py`: a Python script facilitating my work of keying in `casanatensis.xml`
* `ursusOutput.py`: a Python script exporting 'simplified' versions of the edition (e.d. including only one textual layer) -- currently under construction
* `vim_macros_for_ursus.vimrc`: This is a backup copy of the `.vimrc` configuration file for VIM that includes the macros I used to type in file `casanatensis.xml`
* `xmlToolBox`: this folder includes Python functions that I'm using to traverse the DOM of `casanatensis.xml`
