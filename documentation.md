Top-level hierarchy of `<text>` in the  XML/TEI file
====================================================

1. `<text>` has only one child
    - `<body>`, and no other child elements
2. `<body>` has a number of
    - `<head>` (one only, at the beginning) or
    - `<ab>` children.
3. `<head>` has
	- there is only one `<head>`, at the beginning of the text, including 'word-level' children (see below)
4. Each `<ab>`
	- has one or more  `<ref>` children, and no other child elements
4. `<ref>`
	- Each `<ref>` includes a number of 'word-level' children, i.e. `<w>`, `<pc>`, `<lb>`, `<cb>` and `<pb>`
	    - It may also include 'above-the-word-level' children such as `<add>` or `<unclear>`, which, in their turn, include 'word-level' children

Graphemic Value
===============

An assumption of the present edition is that a graphic sign (e.g. a glyph) or a feature (e.g. the use of blank space on the page) of the graphic system of the manuscript has "graphemic value" if it has a distinctive function, that is if

1. it generates "minimal pairs" of words, i.e. in the manuscript there is at least a case in which these signs/features distinguish a a word from another OR

2. it marks a specific linguistic interpretation of the text. [This part is problematic]

Case 1 applies to those graphemes that have an alphabetic value, such as "a", "b", "c": grapheme "c" generates the minimal pair "como/homo". 

Case 2 applies to those paragraphematic signs that do not have an alphabetic meaning, such as punctuation, but do change the text in that they change its meaning (its  linguistic interpretation). For example, the "comma" makes a difference between "Amen dico tibi, hodie mecum eris in paradiso" and "Amen dico tibi hodie, mecum eris in paradiso". On the other side, the same manuscript might have two different glyphs for the same "comma" grapheme which do not make such a difference but are merely position-bound or decorative versions. In this case they would not have graphemic value, but would be considered allographs. 

[Altra ipotesi: considerare i segni paragrafematici come un 'layer' a sé, parallelo al Graphemic Layer.]




Graphic Layer (gL)
==================

The following additional markup refers to graphic signs and features of the graphic system of the manuscript that do not have graphemic value, such as dropcaps. Though they are programmatically set outside of the scope of this edition, they have temporarily been included.

2. `<hi>`
	- `<hi rend="dropcap">I</hi>lle`
		- A dropcap (also called initial, initial letter, or block initial letter
	- `<hi rend="larger">m</hi>inima`
		- The first letter is larger than the others, but not drawn as a dropcap


## Larger letters and dropcaps

After full stops letters are often written larger, and sometimes with a different shape. For example, in 1r line 4 ('Minime'), after the full stop the 'm' is written with a capital glyph (different from the Beneventan minuscule 'm'). However, in 1r line 5 ('differt'), the 'd' after another full stop is written with its regular Beneventan minuscule glyph, just larger.

For the time being, I am encoding them with `<hi>`. Another option could be to add a set of 'capital' graphemes in addition to the 'minuscule' ones. 



Graphemic Layer (GL)
====================

[The content of this section needs revision]

All textual content of the `<text>` (i.e. everything Unicode character descendant of `<text>` that is not markup), represents a grapheme, i.e. a glyph that has graphemic value as described above -- except for the textual content of those elements that are said to include alphabemes (not graphemes) in the "Alphabetic Layer (AL)" section of this documentation, such as `<expan>`.

All other textual content therefore refers to the graphemic system of the manuscript. Every Unicode character of this kind must be understood as a pointer referring to the grapheme identified by the same Unicode character in column "Graphemes" of the "Graphemic Table of Signs" (file GToS.csv).

No Unicode character is allowed within the `<text>` element of the file of the Graphemic Later transcription
if it does noet occur in column "Graphemes" of the GToS --
with the exception of markup and of the textual content of elements including alphabemes, such as `<expan>`, and markup.

Specific software functions as a "lint" to verify that this requirement is met. This assures that every Unicode character in the graphemic transcription points to a grapheme that has a full description in the GToS. In the code

    <w ana="ordinem">ordin
        <choice>
                <abbr type="superscription">e<am>2</am></abbr>
                <expan>em</expan>
        </choice>
    </w>

the "lint" software verifies that there is a line in the GToS with value "o" in column "Graphemes", then that there is a line with value "r" in that column etc. (for the whole sequence 'o', 'r', d', 'i', 'n', 'e', '2'). If it is not the case, it will warn the encoder.

The two Unicode characters 'e' and 'm' (the textual content of element `<expan>`), instead, should not be checked to match characters in column "Graphemes" of the GToS, but characters in column "Alphabemes" of the AToS (the "Alphabetic Table of Signs").

Note. The following hypothesis has not been applied so far
> In addition to the individual Unicode characters described in point 1 above, also `<g>` elements represent graphemes. Their @ref attribute also refers to the corresponding string (mostly, but not necessarily consitituted by one Unicode character) in column "Graphemes" of the GToS. To comply with the TEI standard schema, their @ref formally points to the @id of a `<char>` element in the `<charDecl>` section of the TEI header. Like in case 1 above, specific software verifies that all values of these @ref attributes correspond to a string in colume "Graphemes" of the GToS. In the example
`<text><body><ab>optim<g ref=#um></ab></body></text>`
the "lint" software will also verify that there is a line of the GToS with value "um" in column "Graphemes". If it is not the case, it will warn the encoder.
[Ipotesi: si potrebbe abolire il caso 2 se si usano un sacco di caratteri Unicode, però `<g>` è utile quando il valore alfabetico di un grafema (abbreviazione) non è standard]

Note that some graphemes in the GToS do not have an alphabetic meaning: these are "paragraphematic" signs, such as punctuation.

## Other elements belonging to the graphemic layer

In addition, the following also belongs to the graphemic layer:

1.  '_' Unicode character, representing the space between words
	- Note: at this point, I'm not using '_' but a simple Unicode space ' ' tagged as
		`<pc ana="space"> </pc>`
	- Note: this is problematic. Does it belong to the graphic or to the graphemic layer?
		- It's probably a paragraphematic sign, just like punctuation

[TBA]







Abbreviations
=============


## Type "superscription"

In this edition, the TEI `<abbr>`, `<am>` and `<expan>` elements are used with a semantics still compatible with that declared in the TEI P5 Guidelines, but more specific. In the following code:

    <w ana="quantum">quant
        <choice>
            <abbr type="superscription">u<am>`</am></abbr>
            <expan>um</expan>
        </choice>
    </w>

1. the content of `<abbr>` belongs to the GL (including the content of its child `<am>`);
2. the content of `<expan>` belongs to the LL;
3. any other content of `<w>` that is not included in `<choice>` belongs, as usual, to the GL.

The value "superscription" for attribute @type of `<abbr>` is suggested in the TEI Guidelines, but in the present edition it has a more specialized meaning. It means that the content of `<am>` (which is always a child of `<abbr>` in the present edition) is a grapheme that is written over all the graphemes included in `<abbr>` but not included in `<am>`. In the previous example, the grapheme ¯ (a macron) is written over the grapheme 'u'. This code also means that the alphabetic meaning of the abbreviation is constituted by the alphabemes 'u', 'm'.

Likewise, the following code:

    <w ana="quoniam">
            <choice>
                    <abbr type="superscription">qnm<am>¯</am><abbr>
                    <expan>quoniam</expan>
            </choice>
    </w>

means that the ¯ grapheme (a superscript line, like a macron) is written above three graphemes, namely 'q', 'n' and 'm', and that the alphabetic meaning of the abbreviation is constituted by the alphabemes 'q', 'u', 'o', 'n', 'i', 'a', 'm'

The following code:

    <w ana="sacerdos">sa
        <choice>
            <abbr type="superscription">c<am>2</am></abbr>
            <expan>cer</expan>
        </choice>
    dos</w>

means that the grapheme '2' is written only over the grapheme '2' in the middle of the word, and that the alphabetic meaning of the abbreviation is constituted by the alphabemes 'c', 'e', 'r'.

In the following code:

    <w ana="spiritum">
    	<choice>
    		<abbr type="superscription">sr<am>¯</am></abbr>
    		<expan>spiritu</expan>
    	</choice>
    m</w>

the grapheme ¯ is written over the graphemes 'sr' at the beginning of the word (not over the final grapheme 'm'), and the alphabemes 's', 'p', 'i', 'r', 'i', 't', 'u' are the alphabetic meaning of the whole abbreviation. As to the final grapheme 'm', it is not considered part of the abbreviation, so its alphabetical meaning is its standard one, i.e. the alphabeme 'm' (as encoded in the GToS).

## Type "after"

Abbreviation marks are not always written *above* other graphemes. The grapheme that I'm encoding with the Unicode character ';', for example, is written on the right, after the final grapheme of a word (mostly 'q;' for 'que' and 'b;' for 'bus'):

    <w ana="duabus">dua
        <choice>
                <abbr type="after">b<am>;</am></abbr>
                <expan>bus</expan>
        </choice>
    </w>

## Type "omission"

In very few cases (the first of which being word "correptum", with `xml:id` w32448, in folio 8v, column b, line 33), the abbreviation has no abbreviation mark, but only consists in the omission of some graphemes. In this case the encoding is:

    <w n="correptum" xml:id="w32448">
            <choice>
                    <abbr type="omission">cor</abbr>
                    <expan>correptum</expan>
            </choice>
    </w>
    

## Type "brevigraph" (brevigraphs and logographs)
    
Brevigraphs and logographs do not have abbreviation marks (such as the macron). 

Brevigraphs are defined here as individual graphemes meaning more than one alphabemes, such as the one encoded here at the GL as '¢' (a 'q' glyph with a horizontal trait crossing its descending trait). In the the "Graphemic Table of Signs" (file GToS.csv) such graphemes have 'Brevigraph' in column 'Type'.

Logographs are defined as individual graphemes meaning a whole word, and therefore a sequence of alphabemes. For example, grapheme '÷' for 'est', but only when it means the third person singular of present indicative of verb 'to be'.

In the code:

    <w n="quia" xml:id="w19080">
            <choice>
                    <abbr type="brevigraph">¢</abbr>
                    <expan>qui</expan>
            </choice>
    a</w>

'¢' represents the grapheme for the brevigraph grapheme whose alphabetical meaning is the sequence of alphabemes 'qui'. The element `<am>` (abbreviation mark) is not necessary here.

The following example has a logograph: the grapheme '÷' means a whole word, that is third person singular of present indicative of verb 'to be'. Its alphabetical meaning is therefore 'est', but only when these alphabemes, in their turn, mean that word:

    <w n="est" xml:id="w6270">
            <choice>
                    <abbr type="brevigraph">÷</abbr>
                    <expan>est</expan>
            </choice>
    </w>

I am currently making no distinction between brevigraphs and logographs in the encoding: both are encoded with `<abbr type="brevigraph">`. Up to folio 8v, the only logograph found is that encoded with the Unicode character '÷'.

Note that this type of abbreviation (`<abbr type="brevigraph">`) is different than that marked as `<abbr type="omission">` because+
- in the 'brevigraph'-type a special, individual grapheme, is involved (e.g. that encoded here as '÷', or the 'p' or 'q' with a horizontal trait crossing the descending line),
- while in the 'omission'-type a sequence of (more than one) 'regular' alphabetic graphemes (i.e. graphemes having a one-to-one standard correspondence with an alphabeme) are used (e.g. in the word 'correptum', encoded with `xml:id` w32448, written with the three 'regular' graphemes 'cor' with no abbreviation sign).

Up to folio 5 verso, column b, brevigraphs and logogoraphs had always proved to have each a fixed alphabetic meaning. For them, therefore, the `<expan>` element is not needed to provide the alphabemes meant by the brevigraph/logograph (which could be computed based on the content of column 'Alphabemes' in the "Graphemic Table of Signs", i.e. file GToS.csv). For these graphemes, the whole `<choice>` / `<abbr>` / `<expan>` structure is merely needed to align the sequence of graphemes with the sequence of alphabemes, i.e. to explicitly encode what alphabemes are meant by the brevigraph/logograph. In the example above, grapheme '÷' is aligned with / means the three alphabemes 'est'.

Again, the encoding convention for abbreviations in this edition complies with the TEI-all DTD and the TEI P5 Guidelines, but is fairly specific to this project and derives from the methodological principle of formally distinguishing the GL, the AL and the LL.

## Rationale of this encoding of abbreviations

This encoding convention is useful because:

1. abbreviation marks (like macrons) are often written not only over the last grapheme, but over the whole word or over specific graphemes in the middle of the word. With this encoding convention, it is possible to mark exactly over which graphems the abbreviation mark expands (a similar convention, with @type="underscription", could be use to mark other grapheme/abbreviation mark graphic combinations);

2. some graphemes, such as the abbreviation marks, do not have a fixed alphabetic value. Thus the alphabetic value of a combination of graphemes constituting an abbreviation is not always computable based on the implied rules of the manuscript writing system. See section _Is the explicit encoding of an Alphabetic Layer really necessary?_ for a more detailed discussion on this and some examples.

## Summary of values of @type in `<abbr>`

- superscription
- after
- omission
- brevigraph

## Summary of the distinction of GL and LL in the encoding of abbreviations

1. `<abbr>` 
	- Its content belongs to the GL.
	It has a @type attribute:
		-  @type="superscript" means that
			the grapheme(s) included in `<am>` are written
			above the other grapheme(s) included in `<abbr>`;
		-  @type="after" means that the grapheme(s) included in `<am>`
			are written after the other grapheme(s) included in `<abbr>`;
		-  @type="brevigraph" means that there is only one grapheme meaning
			more than one alphabetical letter: in this case 'abbr' has no 'am' child.

2. `<am>`
	- Its content also belongs to the GL. It includes a
		grapheme with the function of abbreviation mark. Note that the alphabetic
		meaning of the abbreviation is not assigned either to the content of
		`<am>`, or to the other graphemes included in 
		`<abbr>`, but to the whole content of `<abbr>`.

3. `<expan>`
	- Its content belongs to the LL.


## Abbreviations that might have alternative encodings

In 1r, column 2, line 6 and elsewhere, there is a peculiar abbreviation for 'quod': a 'q' is followed by a 'd' whose ascending trait is crossed by a horizontal stroke. This could be interpreted and encoded in two ways:

(a) the 'd with horizontal stroke' is a peculiar grapheme (that might be encoded with Unicode 'ð'), so the code would be:

    <w ana="quod">q
        <choice>
                <abbr type="brevigraph">ð</abbr>
                <expan>uod</expan>
        </choice>
    </w>

(b) the stroke is simply a macron put 'above' the 'd', however, since the 'd' has a long ascending trait, the macron intersects the ascending trait In this case, the code would be:

    <w ana="quod">q
        <choice>
                <abbr type="superscription">d<am>¯</am></abbr>
                <expan>uod</expan>
        </choice>
    </w>

Both interpretations would make sense, and in fact the problem itself is merely 'digital', i.e. arises from the desire of identifying discrete objects within the continuum of handwriting. I am accepting interpretation (b) in this edition.

The same issue arises for abbreviations such as 'uel', abbreviated as 'ul' with a horizontal stroke crossing the ascending trait of grapheme 'l', 'habet' or 'habent' abbreviated as 'hab' with a horizontal stroke crossing the ascending trait of 'b' and others. In these cases, how many graphemes are actually covered (i.e. marked) by the horizontal stroke, that might be interpreted as a macron? For example, in the case of 'ul', one could say that only the 'l', or that both 'ul, are covered/marked by the macron, as the latter often spans over a part of the 'u'. In fact, this is a conventional choice.







Alphabetic layer (AL)
=====================
 
## Case 1: the AL can be computed from the GL transcription
In the writing system of the manuscript, many graphemes have a standard alphabetic meaning, including some brevigraphs. For most of the text, therefore, the computer can generate the alphabetic layer by mapping the sequence of signs included in the Graphemic Layer transcription to the GToS. In the GToS, most graphemes have a standard corresponding (sequence of) alphabeme(s) on column "Alphabemes".


## Case 2: the AL cannot be computed from the GL transcription

Some graphemes do not have an alphabetic value at all. This is encoded in the GToS because the corresponding cell in the "Alphabemes" is blank.

Other graphemes, however, do not have a _standard_ alphabetic value in the GToS, although they do mean one or more alphabemes. For example:

- _Abbreviation marks_. Some of them (such as the macron) do not have
	have a standard alphabetic value, but they mean the omission of one ore more
	alphabemes. E.g., a macron over a final 
	letter in the Beneventan script may mark a general abbreviation:
	dic¯ = dicit (alphabemes 'i' and 't' are omitted here),
	while c¯ (c with macron above) normally means 'cen' or 'con'
	(alphabemes 'e' and 'n' or alphabemes 'o' and 'n' are omitted)
- _Brevigraphs_. Some might not always mean the same alphabetic sequence (TBA)

In this case, i.e. when the philologist/encoder thinks that the computer can/should not generate the alphabetic value of a grapheme from the grapheme/alphabeme mapping in the GToS, the alphabetic value is provided explicitly in the encoding.

This is mostly the case whith abbreviations (base grapheme plus an abbreviation mark such as a macron), so the explicit encoding of the AL here is done by means of `<choice>`, `<abbr>` and `<expan>`), as explained above in the _Abbreviations_ section.



## Is the explicit encoding of an Alphabetic Layer really necessary?

The very distinction of an Alphabetic Layer (AL) of the digital edition from the Graphematic Layer (GL) is based on the assumption that 'case 2' exists, i.e. that the alphabetic value of a grapheme is not always computable based on the implied rules of the manuscript writing system. These are some examples taken from the manuscript:


- The same abbreviation (graphemes 'oms' with a macron spanning over them) occurs twice in folio 3r, column a: in line 10 it has the alphabetic meaning of 'omnes', while in line 36 it has the alphabetic meaning of 'omnis'. It is therefore necessary to use the encoding convention explained in section _Abbreviations_ (use of tags `<choice>`, `<abbr>`, `<expan>` and `<am>`) to explicitly encode both the Graphemic Layer (GL) and the Alphabetic Layer (AL), thus providing the software with information on both layers.

- The abbreviation constituted by the graphemes 'hab' with a horizontal stroke crossing the ascending trait of 'b' (which may be considered a macron spanning over 'a' and 'b') may have the alpbabetic meaning 'habet' (e.g. in folio 5v, column b, line 21) or 'habent' (e.g. in folio 5v, column a, line 31).

- The abbreviation constituted by graphemes 'cor' with a macron over 'o' and 'r' has the alphabetic meaning 'correptum' (e.g. in folio 5v, column b, line 21) or the alphabetic meaning of 'correpta' (e.g. in folio 5r, column a, verse 20). In the latter case, in fact, the interpretation could be both 'correpta' or 'correptum' (as the name of alphabetic letters is sometimes feminine, sometimes neuter in the text), but the expression "ponunt 'e' correptam ante 'us'" occurring right before in the same sentence makes me decide for 'correpta' in this case. Anyways, I think it is clear that the specific alphabetic meaning of that abbreviation is not unambiguously determined by the sequence of graphemes at the GL.


## Possible encoding strategies for the AL

In my previous <a href="http://www1.unipa.it/paolo.monella/lincei/edition.html">Vespa Project</a>, I had used an extremely granular encoding strategy (at the grapheme level, by means of `<g>` elements each with an `@xml:id`) to explicitly encode the alphabetic meaning of every grapheme.

However, in the overwhelming majority of cases, 'case 1' applies, therefore from a practical viewpoint the encoding strategy of my Vespa Project seems excessive and unnecessary. For the same reason, also personalizing the XML/TEI to introduce tags to explicitly distinguish the two levels (a strategy similar to that applied by the <a href="http://m enota.org/tekstarkiv.xml">Menota Archive</a> for other purposes) seems unnecessary: software can compute and output a complete transcription at the Alphabetic Layer based on the mechanism described in 'case 1' (i.e. by using the XML/TEI transcription and the GToS file) and based on the markup described in 'case 2' above.







Linguistic Layer (LL)
=====================

At this layer, the constituting items of the text are 'words'. In the present edition, they are not only identified by their 'regularized' contemporary standard spelling, but by a code, constituted by three parts:

1. The lemma, identified by a reference to a standard dictionary;

2. Its morphological tagging (POS tagging) according to a lemmatizer/POS tagger such as [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/): case, number, gender, tense, diatesis etc.;

3. A standardized contemporary spelling of the inflected form, represented by a sequence of Unicode characters (this part is needed to identify univocally cases such as the genitive plural of Latin deus, -i (god), that can be either deum or deorum).

[Note: the tagset of the Index Thomisticus parameter file that I am currently using with TreeTagger yields some information on the "Formal-Variation", such as "I variation of wordform", "II variation of wordform" etc., and on the "Graphical-Variation", such as "Baseform", "Graphical variations of 1" etc.  I think that this is meant to account for the difference between the two forms of genitive plural of 'deus, -i', i.e. 'deum' or 'deorum'. In this case, #3 above would no longer be necessary]

## Ideally:

Instead of writing the LL transcription on a separate file, mapped to the GL transcription file by means of more complex TEI linking strategies, in this edition the sequence of 'words' at the LL is represented by a sequence of `<w>` elements typically having 3 values (one for the 3 parts listed above). The actual implementation of this feature is still under development. The following example is just meant to give an idea of what it should look like in the file:

    <w ana="2-LM41A2---" lemma="compono" n="composita">composita</w>

or, if I decide to substitute the components of the tagset string (2-LM41A2---) with its plain English correspondents:

    <w ana="Participial, III conjug, Pass/Dep Participle, Perfect, Positive, Singular Nominative, Feminine" lemma="compono" n="composita">composita</w>

- @lemma: #1 above
- @ana: #2 above
- @n: #3 above (while looking for a better solution)



## Tentatively:
I'm still working on the implementation of the 3-values system by using a lemmatizer/POS tagger such as [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/). For now, I'm just using the "standardized contemporary spelling" part, listed above under point 3, as follows:
    <w ana="constructae">cons<g ref="st"/>ructe</w>



## Elements that also belong to the LL:

1. `<ab>`
	- The use of `<ab>` is still tentative. For the time being, there is no `<div>` in the document, while the `<ab>` elements
	    mark parts of the text that have the same topic and normally refer back to the same ancient source(s) (Priscian and others).
	    Each `<ab>` has an @xml:id.
	- Each `<ab>` has an `@xml:id` and a `@n`. E.g.: `<ab xml:id="ab02" n="De dictione: definition of dictio">`
		- the `@n` includes a modern title for the section, that I decided
		- the division of the text in `<ab`> elements is arbitrary: I created it based on the content, though there are sometimes graphical
			distinctions in the manuscript

2. `<ref>`
	- It links to the source of a portion of text by means of a @cRef (canonical reference) attribute, whose value is a URN as for the CTS/CITE architecture (see <https://cite-architecture.github.io/>): see section _Linking the text with its sources with the CTS/CITE architecture_ below
	- Some `<ref>`s have a CRS/URN in @cRef, e.g. `<ref type="source" cRef="urn:cts:latinLit:stoa0234a.stoa001:2.53.8-2.53.12">`
	- Other `<ref>`s have @cRef="unknown":  `<ref type="source" cRef="unknown">`


## `<w>` elements for which the lemmatizer/POS tagger will need help (values of @type with `<w>`)

The possible values marking such cases are:

- @type="nonsense"
- @type="alphabemes"
- @type="ancientAbbreviation"
- @type="foreign"
- @type="numeral"

These are mostly meant to prevent the lemmatizer from trying to parse this type of words.


### @type="nonsense"

If I cannot understand what world is meant by a very unclear sequence of graphemes, I a using two markup strategies:

1. If the word is completely unclear or unreadable and I don't want to transcribe any of its graphemes, I'm using

    `<gap reason="illegible" quantity="1" unit="words"/>`

2. Starting from folio 2 recto, column b, line 8, if I cannot provide a value for the @ana attribute (since I don't recognize any dictionary word) but still want to transcribe at least some of its graphemes, I'm using @type="nonsense". In the following example, I quite distinctly recognize a sequence of four graphemes('p', 'u', 'p', 'u'), that could or could not be followed by two more graphemes:

        <w ana="dada" type="nonsense">dada
        <gap reason="illegible" quantity="2" unit="chars"/>
        </w>

In the following example, I think I recognize a sequence of graphemes, but they don't make sense:

        <w ana="uat" type="nonsense">uat
        <note type="script">There is a sign over the initial 'u'. This sign
        looks like a reuersed 'u' and occurs again later in the same line.</note>
        </w>

### @type="alphabemes"

If a sequence of graphemes constituting a 'graphical word' simple means a sequence of alphabemes (alphabetic letters), I'm using @type="alphabemes". For example, in folio 2r, column a, line 14, the sequence of letters 'ν', 'ο', 'μ', 'α' is said to be the archaic form of the Greek word ὄνομα ():

        <w ana="νομα" type="alphabemes">
    
If the alphabemes are in ancient Greek, the encoding is

        <w ana="α" type="alphabemes" xml:lang="grc">a</w>

### @type="ancientAbbreviation"

If a sequence of graphemes constituting a 'graphical word' is an ancient Roman abbreviation, I'm using @type="ancientAbbreviation", as in the two-letter abbreviation 'gn' for Latin praenomen Gnaeus (folio 2r, column b, line 15):

        <w ana="Gn" type="ancientAbbreviation">gn</w>

Please note that I'm distinguishing this case from the abbreviations of the medieval writing system, that I'm encoding with the `<choice>`, `<abbr>`, `<expan>` and `<am>` elements.

### @type="foreign"

If the word is Greek, I am encoding it as follows:

        <w ana="ὄνομα" type="foreign" xml:lang="grc">onoma</w>

So, the attribute `@xml:lang="grc"` may be associated with `@type="foreign"` if it is a complete word in Greek or with `@type="alphabemes"` if it is not.


### @type="numeral"

Example:

        <w ana="x" type="numeral">x</w>

With my first experiments with [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/), for this word I'm getting `@lemma="num.~rom."`







Linking the text with its sources with the CTS/CITE architecture
================================================================

## Markup strategy currently in use: use of 'ref'

To link a passage to its ancient source(s), I am using code such as:

    <ref type="source" cRef="urn:cts:latinLit:stoa0234a.stoa001:2.53.8-2.53.12">...</ref>

Where value(s) in the @cRef attribute are URNs (Universal Resouce Name) based on the CTS/CITE architecture (see <https://cite-architecture.github.io/> and particularly <http://cite-architecture.github.io/ctsurn/overview/> for the syntax of a CTS URN). The code above points to a passage of Priscian:

1. "urn" means that this is a URN;
2. "cts" means that this URN uses the CTS protocol;
3. "latinLit" is the "cts namespace", identifying the register that assigns an identifir to each "group work" and each "work". It transparently refers to Latin Literature;
4. stoa0234a is the identifier for the "group work" that the scholarly community considers written by Priscian, so in this case it can be understood as a code for "Priscian";
5. stoa001 is the identifier for the "work" within the "group work" stoa0234a (Priscian's works), namely for the "Institutio de arte grammatica".
6. "2" refers to Keil volume 2;
7. "53" refers to page 53 of that volume;
8. "8" refers to line 8 within that page.

The dash between "2.53.8" and "2.53.12", as for the CTS/CITE architecture, means that the URN refers to a whole passage, from line 8 to line 12.

Elements #4 and #5 of all URNs used in this edition derive from [list #2](https://docs.google.com/spreadsheets/d/1RHN6KBulDGbpKATLU6PtwU4o5xVsaBB6xbQRtKjMyWE/edit?usp=sharing) in the section "Lists of URNs" below.

The content of Elements #6, #7 and #8 of all URNs have been decided by me, although I am in contact with the Perseus and Leipzig Philology projects to discuss what the best internal identifiers for portions of text in these authors might be.

If more source passages are to be referenced for the same Ursus passage, they are separated by whitespace. E.g.:

    <ref type="source" cRef="urn:cts:latinLit:stoa0234a.stoa001:2.57.12-2.57.17 urn:cts:latinLit:stoa0110.stoa001:4.373.8-4.373.10">

[sgn: check if this is OK based on the Guidelines recommendations for the values of the @cRef and @ref-like attributes]

In addition to this, milestones such as

    <milestone n="urn:cts:latinLit:stoa0234a.stoa001:2.103" type="source" subtype="page"/>

are used, though not systematically, when the text of the manuscript follows the same source for a long passage. In these cases, this code might be useful to those trying to track down the specific source of a sentence in more detail. I started using `<milestone>` elements with this function from folio 7v, column b, line 34 on. These URNs end with the number of page of Keil's edition. In the example above, the milestone marks the point in which the manuscript's text corresponds to the source Priscian, Ars grammatica (`latinLit:stoa0234a.stoa001`), volume 2, first line of page 103 of Keil's reference edition.


## Lists of URNs

1. Thomas shared
<https://docs.google.com/spreadsheets/d/1VPdW_upQtP9voPq-fZW_McfyPTfR5Lr-jFGmSubffLA/edit?usp=sharing>
This spreadsheet only includes Latin authors. My understanding is that it is a working list of the Leipzig project.
2. Alison shared
<https://docs.google.com/spreadsheets/d/1RHN6KBulDGbpKATLU6PtwU4o5xVsaBB6xbQRtKjMyWE/edit?usp=sharing>
that includes Latin, Greek, inscriptions etc. and is the working list of the Perseus Project.
3. Most (but not all) the entries of list #2 have entered the Perseus Catalog in
<http://catalog.perseus.org/catalog/urn:cite:perseus:author.1179>


## My URNs short explanation

### Grammarians: main sources of Ursus

- Priscian Institutio
	- urn:cts:latinLit:stoa0234a.stoa001
- Priscian De figuris numerorum
	- urn:cts:latinLit:stoa0234a.stoa003
- Donatus (Ars Minor, pp. 367-392)
	- urn:cts:latinLit:stoa0110.stoa001
	- (Other minor works by Donatus, from "De barbarismo" on, i.e. from page 393,
    		have different URNs: see long explanation below)
- Seruius Commentarius
	- urn:cts:latinLit:stoa0259.stoa001
- Sergius Explanationes
	- urn:cts:latinLit:stoa0258a.stoa001
- Pompeius Inst
	- urn:cts:latinLit:stoa0233c.stoa001
	
### Classical sources of citations in those grammarians, in order of appearance in the manuscript

- Persius, Saturae
    - urn:cts:latinLit:phi0969.phi001
- Verg. Aen.
    - urn:cts:latinLit:phi0690.phi003
- Lucanus, Pharsalia
    - urn:cts:latinLit:phi0917.phi001
- Claudius Caesar Germanicus, Fragmenta Aratea
    - urn:cts:latinLit:phi0881.phi002



## My URNs long explanation

### Priscian from Caesarea, "Institutio de arte grammatica"
- List #1 and catalog #3 have the author, but not the work.
- List #2 has author and work. URN: stoa0234a.stoa001

### Priscian from Caesarea, "De figuris numerorum"
- List #1 and catalog #3 have the author, but not the work.
- List #2 has author and work. URN: stoa0234a.stoa003

### Pompeius, 5th/6th cent., "Commentum Artis Donati"
- List #1 and catalog #3 do not have the author.
- List #2 has author and work. URN: stoa0233c.stoa001

### Servius, 4th cent., "Commentarius in Artem Donati"
- List #1 does not have the author.
- List #3 has the author, but not the work.
- List # 2 has author and work. URN: stoa0259.stoa001

### Sergius, the Grammarian, fl. 515-517, "Explanationem in Artem Donati"
- List #1 and catalog #3 do not have the author.
- List #2 has author and work. URN: stoa0258a.stoa001

### Aelius Donatus
- List #1 and catalog #3 have the author, but not the work.
- List #2 has author and work, but Keil and list #2 divide this grammatical works differently. Keil has one big work ("Ars grammatica"), while list #2 divides it into smaller works, each with its own URN:
	- Aelius Donatus, "Ars Minor (De partibus orationis)". URN: stoa0110.stoa001 (pp. 367-392)
	- Aelius Donatus, "De Barbarismo". URN: stoa0110.stoa003 (pp. 392-393)
	- Aelius Donatus, "De ceteriis vitiis". URN: stoa0110.stoa004 (pp. 394-395)
	- Aelius Donatus, "De Metaplasmo". URN: stoa0110.stoa005 (pp. 395-397)
	- Aelius Donatus, "De Schematibus". URN: stoa0110.stoa006 (pp. 397-399)
	- Aelius Donatus, "De Solecismo". URN: stoa0110.stoa007 (pp. 393-394)
	- Aelius Donatus, "De Tropis". URN: stoa0110.stoa008 (pp. 399-402)




## Another possible markup strategy (not in use) to link text with source: use of 'link'

Another encoding convention that I might adopt in the future is the following:
Each `<link>` element connects an `<ab>` with one or more `<ptr>`/pointers. Each `<ptr>` has a @cRef attribute whose value is a CTS/CITE URN referencing a specific passage in Priscian (or another text being the source of Ursus' text). Example:

    <ab xml:id="ab001">
    <link type="source" target="#ab001 #ptr0001"/>
    <ptr xml:id="001.1" cRef="urn:cts:latinLit:phi0914.phi0011.perseus-lat1:4.2"/>
    ...

If one passage by Ursus points to two (or more) ancient sources, the code should look like this:

    <ab xml:id="ab001">
    <link type="source" target="#ab001 #ptr0001.1 #ptr0001.2"/>
    <ptr xml:id="ptr001.1" cRef="urn:cts:latinLit:phi0914.phi0011.perseus-lat1:4.2"/>
    <ptr xml:id="ptr001.2" cRef="urn:cts:latinLit:phi0914.phi0011.perseus-lat1:5.3"/>
    ...

A more precise encoding convention might use the XML/TEI P5 'intermediate pointers'. In the following example,  `<link>`  always has two targets only, where the first one represents Ursus' textual portion, the second one represents the source(s).

    <ab xml:id="ab001">
    <link type="source" target="#ab001 #ptr0001"/>
    <ptr xml:id="ptr001" target="#ptr0001.1 #ptr0001.2"/>
    <ptr xml:id="ptr001.1" cRef="urn:cts:latinLit:phi0914.phi0011.perseus-lat1:4.2"/>
    <ptr xml:id="ptr001.2" cRef="urn:cts:latinLit:phi0914.phi0011.perseus-lat1:5.3"/>

The following encoding convention, though simpler, is not a viable option because `<ab>` has no @cRef attribute:

    <ab xml:id="ab001" cRef="urn:cts:latinLit:phi0914.phi0011.perseus-lat1:4.2"> 



## CTS/CITE references

The CTS/CITE Architecture will be used to link sections of the manuscript to their ancient sources. These are some references.

- CTS/CITE Architecture
<http://www.homermultitext.org/hmt-doc/index.html>

- Perseus CTS API
<http://sites.tufts.edu/perseusupdates/beta-features/perseus-cts-api/>

- Groups of links
`<linkGrp>`
<http://www.tei-c.org/release/doc/tei-p5-doc/en/html/SA.html#SAPTLG>

- Pointing mechanisms
<http://www.tei-c.org/release/doc/tei-p5-doc/en/html/SA.html#SAXP>

- Bibl (extrema ratio)
<http://www.tei-c.org/release/doc/tei-p5-doc/de/html/ref-bibl.html>

- @cRef
<http://www.tei-c.org/release/doc/tei-p5-doc/de/html/ref-att.cReferencing.html>
(only allowed in `<gloss>`, `<ptr>`, `<ref>`, `<term>` (strangely, not in `<link>`!)







Markup not referring to a specific layer
========================================

1. `<unclear>`

	- See TEI P5 Guidelines, 11.3.3.1 Damage, Illegibility, and Supplied Texts <http://www.tei-c.org/release/doc/tei-p5-doc/en/html/PH.html#PHDA>
	- In this edition, `<unclear>` always has one child only, and that child can be <w> or <pc>.
	- Attributes used for element `<unclear>` in this edition:
		- @reason
    			- Possible values:
    				- "faded" (faded ink),
    				- "stain" (ink or another material),
    				- "script" (I find the script hard to understand in this point)
    				- "cropped" (the digital reproduction of the manuscript page cropped out this portion of the manuscript)
		- @cert
			- "The cert attribute on the `<unclear>` element may be used to 
				indicate the level of editorial confidence in the reading contained within it."
    				(TEI P5 Guidelines, 11.3.3.1 Damage, Illegibility, and Supplied Texts
    				<http://www.tei-c.org/release/doc/tei-p5-doc/en/html/PH.html#PHDA>).
    				Possible values are those of the TEI P5 "data.certainty"
				datatype, that is: "high" | "medium" | "low" | "unknown".
    			For example, "low" means that I am little sure 
				that my tentative transcription is correct.
		- @quantity
    			 - Possible values: an integer
		- @unit
			- Possible values:
				- "words"
				- "chars" (the latter value is recommended by TEI P5; see
        				<http://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-att.dimensions.html>)

2. `<gap>`
	- See TEI P5 Guidelines, 11.3.3.1 
		Damage, Illegibility, and Supplied Texts
		<http://www.tei-c.org/release/doc/tei-p5-doc/en/html/PH.html#PHDA>
	- Attributes used for `<gap>` in this edition:
		- @reason
			- Possible values:
				- "illegible" (this can be due to faded ink, to handwriting complicated to understand or to a combination of the two),
				- "hole" (a hole in the parchment)
				- "cancelled" (if the scribe erased the text)
		- @quantity
    			- Possible values: an integer
		- @unit
			- Possible values:
				- "words"
				- "chars" (the latter value is recommended by TEI P5; see
        				<http://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-att.dimensions.html>)

3. `<add>`
	- the code `<add place="above">...</add>` is put
		- either at the point
			of the text where the interlinear addition starts (i.e.: in the XML
			code, it comes right before the text above which it appears in the manuscript)
		- or at the point of the text in which a metamark glyph in the manuscript line points to the interlinear addition
			(e.g. in folio 9r, column a, line 35)
		- or, if the addition is meant to supply one or more missing word, in the point of the text where the supplied words logically belong.

	- it can be either
        - parent of one or more `<w>` and/or `<pc>`elements (in most cases), if one ore more full words were added above the line
        - or child of `<w>` and parent of plain text (in few cases), if individual graphemes (not full words) were added above the line.

	- possible values of attribute `@place` are:
		- "above" for interlinear additions (above the line)
		- "below" for intelinear additions (below the line)
		- "footnote" for an addition at the bottom of the column, connected with the text with a metamark
		
4. `<note>`
	- It has a @type attribute that can have the following values:
		- "tech" (on technological issues of this digital edition).
		- "script" (notes on palaeographical aspects or on illegible or hardly readable passages);
		- "graphic" (a more specific type than "script", used to informally add information about
			elements belonging not to the graphematic, but to the graphic layer, which is
			not systematically included in this edition; e.g.: a macron over a grapheme marking
			its long quantity),
		- "facsimile" (on the digital photos of the manuscript),
		- "source" (on the text sources),
		- "content" (on the text content);
		- "emendation" (a note proposing an emendation of the text clearly readable in the manuscript);







Punctuation
===========

If we created a modern 'readable' edition of the text, we would

1. ignore, accept or change the value of the manuscript puctuation marks (or 'ancient punctuation') and
2. add 'contemporary punctuation' not present in the manuscript.

The 'ancient punctuation' found in the manuscript is part of the Graphemic Layer (GL), while the 'contemporary punctuation' could be (tentatively) considered as part of the Alphabetic Layer (AL) and of the Linguistic Layer (LL).


## Case 1: manuscript punctuation (GL)

`<pc ana=".">.</pc>`

- means that the manuscript has a full stop and that we would 
	also use a full stop in a contemporary edition.
- In this code, the value of the @ana attribute records the contemporary 
	punctuation counterpart of the manuscript glyph and belonging to the LL, 
	while the content of the element ('.') represents the manuscript glyph and 
	belongs to the GL.

`<pc ana=",">.</pc>`

- means that the manuscript has a comma, but we would use a full stop in a contemporary edition.
- In this code, the ',' belongs to the GL and the 
	'.' (the value of the @ana attribute) belongs to the LL.

`<pc ana="0">·</pc>`

- means that the manuscript has a middle dot, but we would use 
	no punctuation sign in a contemporary edition.
- In this code, the '·' belongs to the GL and the '0
	' (the value of the @ana attribute) belongs to the LL.

`<pc ana="quote">·</pc>`

- means that the manuscript has a middle dot used as graphical markup 
	to surround a quoted element (for example: «letter "a"»).
	We would probably use quotes in a contemporary edition.
- In this code, the '·' belongs to the GL and the 
	string 'quote' (the value of the @ana attribute)
	refers to the LL. I'm using a string ('quote')
	because I cannot use the " quote sign as value of an 
	attribute in XML.


## Case 2: contemporary punctuation not present in the manuscript

For adding contemporary punctuation not present in the manuscript, I am tentatively inserting some 'contemporary punctuation' in the transcription, but clearly marking it as separate from the GL, as follows:

    <pc ana=","></pc>

where the value of the @ana attribute (belonging to the LL) records the contemporary punctuation, while the fact that the element is void (has no text content) means that there is no glyph in the GL.

This is a full example of markup of a word simply followed by a space (no ancient punctuation) in the manuscript, but after which we would insert a comma in a contemporary 'readable' edition:

    <w ana="orationis">orationis</w><pc ana=","></pc>

Note that in the code above the contemporary comma is placed before the underscore (meaning a space in the manuscript), but this is completely arbitrary and is just meant to simplify the further processing of the source file.


## Possible values for attribute @ana of `<pc>`

`<pc ana=","></pc>`

- Contemporary comma (short pause or syntactic distinction)


`<pc ana=".">.</pc>`

- Contemporary full stop (long/strong pause or syntactic distinction)


`<pc ana="quote">·</pc>`

- This marks the case in which a middle dot is used (before, after or before and after the word) by the scribe to mark that a word is quoted. This is often used for individual alphabetical letters ('alphabemes') or morphemes.


`<pc ana="question">~</pc>`

- Contemporary question mark


`<pc ana="0">·</pc>`

- In a contemporary edition, we would include no punctuation sign here. If the punctuation sign has a specific meaning not falling in the cases listed here, a `<note>` element is added next to the `<pc>` element to explain the specific value


Note that the ancient sign that I'm encoding as "," often has the value of a contemporary full stop. Generally, there is no easily predictable correspondance between the medieval punctuation and the contemporary one.


## Allographs and graphemes for punctuation

### Low dot
The punctuation sign that I am encoding with Unicode "." seems to have two allographs:

1. simple, just a dot (see fullstop.png)
2. a dot with a tail (see fullstopwithtail.png)

So I'm encoding both with the Unicode character "."

### Middle dot
The punctuation sign that I am encoding with Unicode "·" (middle dot) might also have two allographs:

1. simple, just a middle dot
2. a horizontal dash (see dash.png)

I'm encoding both with the Unicode character for the middle dot "·"

It is often hard to distinguish between the middle dot (encoded here with Unicode "·") and the full stop (encoded here with Unicode "."), however I'm still retaining this distinction.







Ligatures
=========

Ligatures pose a problem, in our edition model. Given the continuous (not discrete) nature of handwriting, it is extremely difficult (and quite arbitrary) to draw a line between

1. what can be considered two distinct graphemes connected by a trait in a handy ligature, such as 'st' in 1r, 1st line ('minima pars e*st*'), and

2. one peculiar grapheme originated by a ligature, such as 'ti' in 1r, 3rd line ('constructe ora*ti*onis').

Both can be considered ligatures, in case 2, the shape of the ligature differs from the shapes of the two original glyphs more than in case 1. However, in the present edition:

1. In the first case, I encode the two glyphs in the ligature as two separate graphemes and therefore with two Unicode characters (as in the following code) or two TEI P5 `<g>` elements:

         <w ana="est">est</w>

2. In the second case, I consider the ligature as one grapheme and encode it with one Unicode character (as in the following code) or one TEI P5 `<g>` element:

        <w ana="orationis">oraŧonis</w><pc>,</pc>

For a list of the ligatures that I encode as in case 1 and those that I encode as in case 2, see section 'Graphemes or not?' in this documentation.







Grapheme or not?
================

The glyphs that do not carry 'graphemic value' (as defined above) are not included in our transcription. This section discusses some encoding choices in this respect.

## Allographs

- i
	- It has two allographs: long (ascending) and short, plus specific glyphs in ligatures.
- t 
	- It has three allographs: see images t1.png, t2.png and t3.png.
- e
	- It has two allographs: one where the lower circle is open 
		on the right side (see image e1.png) and 
		one, looking like a '8', where both circles are 
		closed (image e2.png). The latter is very common 
		in ligatures such as the one for the Latin conjuction 'et'
		and when the 'e' is followed - and connected to - another glyph.


## Ligatures encoded as a sequence of two graphemes

- et
	- I initially encoded this ligature as one specific grapheme, but then 
		came to realize  that the 'closed e' resembling a
		'8' can be considered an allograph of 'e' and 
		that there is an allograph of 't' that consists in 
		one curved line going upwards, so the ubiquitous glyph representing
		'et' can be considered a simple ligature of those two allographs 
		'e' and 't'. I am therefore now encoding it 
		with two distinct Unicode characters: 'e' and 't'.
- st
	- Example: 1r, 3rd line ('minima pars est'). If 
		it apprears on its own, with both graphemes surrounded by a 
		macron/tilde, it is an abbreviation for 'sunt'
- fi
	- Ligature, encoded as two distinct graphemes (e.g. 1v, column a, line 8)
- ri
	- Ligature, encoded as two distinct graphemes
- ti
	- The 'ti' sequence is alwasy a ligature in the writing system of the manuscript. However:

		1. in some cases the 'ti' sequence is represented by a 't' glyph with its 'low' shape, followed by (and connected with) a descending 'i'. Example: 1r, line 6, last word: 'dictio'). See ti2_a.png (with short 'i') and ti2_b (with long 'i');
		2. in other cases, the 't' is written with a different shape, tightly connected with the following 'i'. In this case the 'i' is long (ascending and descending). Example: 1r, 3rd line, 1st word ('dic*ti*o est minima pars'). See ti1.png. According to a general rule in the Beneventan script, this allograph should be used when the pronunciation of the 't' is IPA /tsj/. This rule seems not to be always followed in this manuscript.

		I am choosing to encode both cases as a sequence of two distinct graphems (therefore with a sequence of two Unicode characters). I am thus assuming that

			- the 't' grapheme has two allographs: the 'regular' one used in case 1 and the peculiar shape used in case 2) and
			- also the 'i' grapheme has allographs: a long (ascendind and escending) allograph used in case 1 and a descending allograph used in case 2.
As stated in the 'Ligatures' section of this documentation, this choice is merely arbitrary. Another choice could have been to consider the two ligatures (case 1 and case 2) as two different single graphemes and encode them as such.

- te
	- Also in this case the 't' grapheme can be represented by two allographs (bot connected with the following 'e', which is written with its regular glyph):
		1. Ascending 't'. Example: 1r, line 3 ('constructe'). Code: <w ana="constructae">constructe</w>
		2. Non-ascending 't'. Example: 1r, line 4
		('composite'), but also the 'cte' that begins that line.
- tu
	- Always in ligature, where 't' has its short allograph (i.e. the shape of a reversed 3)
- ec
	- Ligature, encoded as two distinct graphemes
- ex
	- Ligature, encoded as two distinct graphemes
- is
	- Ligature, encoded as two distinct graphemes

...and others that I am not listing here.







Layer differentiation: encoding strategies
==========================================

*Note (sgn)*: this section needs to be re-written.

One of the key methodological innovations of this edition is the distinction between the different layers (graphic, graphemic, alphabetic and linguistic), as suggested by Tito Orlandi ("Informatica testuale").

As opposed to producing an XML transcription file for each layer, I am now producing one XML/TEI source code for the transcription, within which the distinction between the different layers is marked (explicitly or implicitly, yet non-ambiguously). In other words, the software parsing the source code should be able to assign each piece of information (text or markup) in the source code to a specific layer (graphic, graphemic, alphabetic and linguistic). For example, in the code

    <hi rend="dropcap">i</hi>lle

the software is instructed to assign the `<hi>` element and its content 'i' to the graphic layer because this documentation specifies that the `<hi>` element always carries information belonging to that layer. The software should then assign the following Unicode characters 'lle' to the graphematic layer because this documentation states that every Unicode character in the source code not explicitly assigned to another layer should be assigned to the graphematic layer.
In the code

    <w ana="constructae">con<g ref="st"/>ructe</w>

the Unicode characters 'con' and 'ructe' are assigned to the graphemic layer (as they are not explicitly marked as balonging to another layer), the `<g>` element is also assigned to the graphemic layer because this documentation states that 'g' elemnts belong to that layer, while the information belonging to the linguistic layer is included in the value of the @ana attribute, as also specified by this documentation (in the "Linguistic Layer" section).

To encode this differentiation explicitly (which would be ideal), one attribute such as @layer should be appended to all elements. However, there is no single attribute with this meaning in the TEI P5, so a schema customization would be required to introduce a @layer attribute. For the time being, however, this is not necessary because this documentation specifies what specific markup refers to a specific layer. For example, the `<hi>` element refers to the graphic layer, while the @ana attribute in the `<w>` element refers to the linguistic layer.







Boundaries between words
========================

1. Contemporary word boundaries: The `<w>` element marks the word boundaries defined by the encoder according to the contemporary linguistic model of Latin. They therefore belong to the LL, not to the gL.

2. Manuscript word boundaries: The word boundaries as conceived by the scribe and graphically marked in the manuscript are encoded in the present edition with 

        <pc ana="space"> </pc>

	[Note: they were previously encoded by means of underscores '_', but no longer now].

Note that the 'contemporary word boundaries' and the 'manuscript word boundaries' do not always coincide. For example, the source code

    <w ana="id">id</w>
    <w ana="est">est</w>

marks that the manuscript has 'idest' (with no space in between), while a contemporary edition would write 'id est'.

A 'diplomatic edition' output (representing the graphemic layer) therefore should show 'idest', while a 'readable edition' output (representing the linguistic layer) should show 'id est'.







Line breaks
===========

According to the common TEI practice, the
`<lb/>`
tag is put before the first line of a page, not after the first line.

When a word is broken up by the line break, the markup looks like

    <w ana="consonante">con
    <lb n="2r.b.16"/>
    sonante</w>
