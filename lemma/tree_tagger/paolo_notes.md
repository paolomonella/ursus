>>> import pprint
>>> import treetaggerwrapper
>>> tagger = treetaggerwrapper.TreeTagger(TAGLANG='la')
>>> text = ['Gallia', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres']
>>> tags = tagger.tag_text(text, numlines=True, tagonly=True)
>>> pprint.pprint(tags)
['Gallia\t11B---A1---\tGallia',
 'est\t3-NA1--6---\tsum',
 'omnis\t11C---A2---\tomnis',
 'divisa\t2-LM41A2--1\tdivido',
 'in\t4-S--------\tin',
 'partes\t11C---M2---\tpars',
 'tres\t11C---M2--1\ttres'].

---

>>> for x in text:
...     print('Form: ', x, '\tTag:', tags[text.index(x)])
... 
Form:  Gallia 	Tag: Gallia	11B---A1---	Gallia
Form:  est 	Tag: est	3-NA1--6---	sum
Form:  omnis 	Tag: omnis	11C---A2---	omnis
Form:  divisa 	Tag: divisa	2-LM41A2--1	divido
Form:  in 	Tag: in	4-S--------	in
Form:  partes 	Tag: partes	11C---M2---	pars
Form:  tres 	Tag: tres	11C---M2--1	tres

# Però il codice non funzionerà sempre, perché index() trova il *primo* elemento della lista che ha quel valore. Che succederà quando ci saranno tanti 'in' nella lista? Bisogna trovare una strategia migliore, prendendo l'indice esatto 'y' della prima lista (magari con un counter) e usando un semplice tags[y] nella seconda lista. Probabilmente la cosa migliore è mettere degli xml:id nei <w>

La 'spiegazione' dei POS tag è in
/home/ilbuonme/ursus/lemma/tree_tagger_and_related_files/parameter_files/from_treetagger_website/index_thomisticus/Tagset_IT.pdf