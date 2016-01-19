# Conversazione Skype su lemmatizzazione e POS tagging

## Informazioni sulla conversazione

- chi
    - io, Marco Passarotti (e Eleonora Litta Modigliani Picozzi, che però non ha parlato)
        - entrambi UniCatt Milano, CIRCSE
    - tutto quel che annoto qui, sono consigli di Marco
- su cosa
    - il loro lemmatizzatore/tagger morfologico LemLat
    - opzioni per lemmatizzare/tagger morfologico
- quando e dove
    -  14.01.2016 ore 14.00 su Skype


# Consigli di Marco su come lemmatizzare/taggare

1. provo cltk
    - se non c'è troppo lavoro di aggiustamento da fare dopo
    - ma in realtà funziona abbastanza male
2. provo un POS (part of speech) tagger  alone, cioè humpos o lo stesso treetagger
    - posso usare uno dei due parameter files per il latino (meglio index thomisticus)
        - uno è quello basato sull'index thomisticus treebank (Thomisticus parameter file, qui di seguito)
        - l'altro è quello fatto da Bonini [ma forse è Brandolini] basato sul latino classico (Bonini parameter file, qui di seguito)
    - oppure ri-addestro treetagger o il suo fratellino humpos [e quindi, se non ho capito male, creo un nuovo parameter file]
        - lo addestro su uno degli "UD treebank" (universal dependencies treebank)
            - gli UD treebank sono sul sito universal dependencies (UD), https://universaldependencies.github.io/docs/
            - scarico le dependencies per il latino. Ce ne sono 3 [credo che dependencies e treebanks siano la stessa cosa]
                - Latin-ITT UD treebank: fatta sull'index thomisticus, M. Passarotti
                - Latin-PROIEL UD treebank: sviluppata a Oslo (nuovo testamento e lat. class.)
                - Latin UD treebank: piccola (un po' di cic., sall. etc.), Leipzig University (Humboldt Chair in DH, Prof. Gregory Crane)
            - e lo addestro su quelle dependencies
            - c'è un tutorial su come si addrestra un POS tagger
                - non è difficile
        - mi disinteresso della sintassi
            - estraggo solo le coppie lemma/POS
    - il POS tagger (humpos o treetagger) ha il vantaggio, rispetto a cltk, che
        - come cltk, sceglie il lemma/tagging (tagging = morphological tagging) giusto
        - ma meglio di cltk, non sceglie una forma perché è la più frequente, ma perché guarda a sinistra e a destra
3. o meglio
    - primo passaggio: lo fa morpheus o LemLat
    - secondo passaggio: un POS tagger sceglie tra le opzioni date dal primo passaggio
        - anche qui, il modo di usare il POS tagger è lo stesso indicato in 2


## Perché in 2 (e 3) conviene riaddestrare il POS tagger su uno dei 3 latin treebanks?

- Premesse
    - i 3 latin treebanks sono quelli citati sopra: Latin-ITT UD treebank, Latin-PROIEL UD treebank, Latin UD treebank
- Perché bisogna riaddestrare il POS tagger
    - online ci sono già due parameter files per il latino pronti da usare, ma non vanno bene perché
        - Thomisticus parameter file
            - questo funziona bene, ma è basato sul latino medievale di t. d'aquino
            - però non produce output in "universal part of speech tagset" (UPST)
            - e non dà 'avverbio', 'congiunzione' etc. ma dà 'parte invariabile'
        - Bonini parameter file
            - anch'esso non usa lo UPST
            - però almeno ti dà 'avverbio', 'congiunzione' etc.
            - però non funziona tanto bene quanto quello thomisticus


## Quale tagset?

- Universal part of speech tagset (UPST qui di seguito)
    - http://petrovi.de/data/universal.pdf
- le abbreviazioni per l'analisi morfologica prodotta da CLTK, cioè "A-S---FB-", somiglia, dice Marco, allo standard EAGLES
    - EAGLES: expert advisory group on language engineering standard
        - un progetto del 2001
    - LemLat usa codici molto simili a questi

## File che ho scaricato

- Ho scaricato questi file il 15.01.2016, dopo la conversazione su Skype

- i tre treebanks dal sito Universal Dependencies:
    - /home/ilbuonme/voluminosi/ursus/lemma/treebanks/universal-dependencies-1.2/UD_Latin
    - /home/ilbuonme/voluminosi/ursus/lemma/treebanks/universal-dependencies-1.2/UD_Latin-ITT
    - /home/ilbuonme/voluminosi/ursus/lemma/treebanks/universal-dependencies-1.2/UD_Latin-PROIEL
- i due parameter file dal sito di Treebank:
    - Thomisticus parameter file: /home/ilbuonme/voluminosi/ursus/lemma/parameter_files/from_treetagger_website/index_thomisticus
    - Bonini [ma penso sia Brandolini] parameter file: /home/ilbuonme/voluminosi/ursus/lemma/parameter_files/from_treetagger_website/brandolini1