# General links

Instructions are in:

http://docs.cltk.org/en/latest/installation.html
Installation

http://docs.cltk.org/en/latest/latin.html
Tools for Latin

http://docs.cltk.org/en/latest/importing_corpora.html
How to import a corpus.


# Installation

- choose the directory to work within, then:
$ pyvenv venv
$ source venv/bin/activate

- If you haven't done this before _in this directory_:
$ pip install cltk


# Use the tools
$ source venv/bin/activate
- some scripts should include, at the beginning:
from cltk.corpus.utils.importer import CorpusImporter
corpus_importer = CorpusImporter('latin')
corpus_importer.import_corpus('latin_models_cltk')
