/*###########################################
#      LL LAYER: VISUALIZED OR NOT?         #
###########################################*/
// Most 'title' attributes (with the exception of those used for gaps in the
// manuscript) have the function of visualizing
// the Linguistic Layer (LL) for each word, on hover.
// While I am still reviewing the lemmatization, the 'title' attributes should
// not be added to the HTML elements including words.
// 	If you want the LL to be visualized, set variable viewLL to true;
// 	If you want it not to be visualized, set variable viewLL to false.
// I am today setting viewLL to false. When I'll be finished reviewing the
// lemmatization, I'll set it back to true to
// restore the visualization of the Linguistic Layer for words.
// March 1, 2017.
var viewLL = true;


/*###########################
#      HTML CLASSES         #
###########################*/
//
// In the HTML DOM returned by this script, each text portion is assigned to one
// of the three layers, i.e.
// 	LL (Linguistic Layer), 
// 	AL (Alphabetic Layer),
// 	GL (Graphemic Layer),
// through @class values. These are the values and their meaning:
//
//
// A) General values for the "class" HTML attribute:
// 	LL: everything (word or word fragment) belonging to the LL
// 	AL: everything (word of word fragment) belonging to the AL
// 	LL: everything (word of word fragment) belonging to the LL
// 	word: for a span including a full linguistic word (always combined with LL)
// 	wordTable: for a table including a full linguistic word 
//
//
// B) List: Word table and its rows
//
// <table class="wordTable">: A table including a word. Each row (TR) has one cell (TD) representing a layer:
// <td class="LLCell"> is the 1st row (index=0), for the LL (Linguistic Layer);
// <td class="ALCell"> is the 2nd row (index=1), for the AL (Alphabetic Layer);
// <td class="GLCell"> is the 3rd row (index=2), for the GL (Graphemic Layer).
//
// Variants of <td class="ALCell">:
// 	<td class="ALCell alphabemes"> (when in the XML we have <w type="alphabemes">
// 	<td class="ALCell nonsense"> (when in the XML we have <w type="nonsense">
// 	<td class="ALCell foreign"> (when in the XML we have <w type="foreign">
//
//
// C) List: Div/Span elements children of <w> in the XML/TEI source file including medieval text
//
// <span class="LL word"> is child of <td class="LLCell">:
// 	value "LL" means that it belongs to the LL;
// 	value "word" means that it includes a complete (linguistic) word.
// 	The hierarchy in the DOM will therefore be:
//	<table class="wordTable">
//		<tr>
//			<td class="LLCell">
//				<span class="LL word">
// <span class="LL word triform"> is the same, but is used if I choose the visualization of the LL
// 	in the form
// 	"artis": [ars] Nominal, Positive, III decl, Singular Genitive, Feminine,
// <span class="AL larger">: it marks a word initial letter that,
// 	on the GL, is written with a larger grapheme (not quite a dropcap).
// 	It is always a child of <td class="ALCell">
// <span class="GL larger"> is a child of <td class="GLCell">: it marks a word initial grapheme larger
// 	than the rest of graphemes at the GL.
// 	It may occur ad different points of the XML tree, so possible hierarchies are: 
// 		<td class="ALCell"> / <span class="AL larger">
// 		<td class="ALCell"> / <span class="base_abbreviation"> / <span class="AL larger">
// 		<td class="ALCell"> / <span class="base_after"> / <span class="AL larger">
// 		<td class="ALCell"> / <span class="base_brevigraph"> / <span class="AL larger">
// <span class="AL dropcap"> and
// <span class="GL dropcap">: same as "Al larger" and "GL larger", however this is a real dropcap.
// <span class="LL gap"> is a child of <td class="LLCell">: a gap in the manuscript (resulting in alphebemes
// 	missing from the AL of the edition).
// <span class="AL gap"> is a child of <td class="ALCell">: a gap in the manuscript (resulting in alphebemes
// 	missing from the AL of the edition).
// <span class="GL gap"> is a child of <td class="GLCell">: a gap in the manuscript (resulting in graphemes
// 	missing from the GL of the edition).
// <span class="AL space"> marks a situation when there is a space between graphical words in the manuscript
// 	(child of <td class="ALCell")
// <span class="GL space"> marks a situation when there is a space between graphical words in the manuscript.
// 	(child of <td class="GLCell")
// <span class="GL base_superscription">: in an abbreviation of type "superscription", like re² for "rem",
// 	(where a 2-like "abbreviation mark" is written above the "base grapheme" e),
// 	this <span> marks the "e" base grapheme.
// 	So, it marks the base grapheme(s) in an abbreviation of type "superscription".
// 	(child of <td class="GLCell")
// <span class="GL am superscription">: it marks the abbreviation mark in an abbreviation
// 	of type "superscription".
// 	(child of <td class="GLCell")
// <span class="GL base after">: in an abbreviation of type "after", like quib; for "quibus"
// 	(where a semicolon-like "abbreviation mark" is written after the "base grapheme" b),
// 	this <span> marks the "b" base grapheme.
// 	(child of <td class="GLCell")
// <span class="GL am after">: it marks the abbreviation mark in an abbreviation of type "after".
// 	(child of <td class="GLCell")
// <span class="GL base brevigraph">: in an abbreviation of type "brevigraph", like ¢a for "quia"
// 	(where an individual grapheme - a brevigraph - represents many letters and there is no
// 	"abbreviation mark"), this <span> marks the "¢" brevigraph.
// 	(child of <td class="GLCell")
// <span class="GL am brevigraph">: it marks the abbreviation mark in an abbreviation of type "brevigraph".
// 	(child of <td class="GLCell")
// <span class="GL am omission">: it marks the abbreviation mark in an abbreviation of type "omission".
// 	(child of <td class="GLCell")
// <span class="AL abbrExpansion">: it marks a group of alphabemes (alphabetic letters) that are
// 	abbreviated in the manuscript (so they don't have a one-to-one alphabeme/grapheme correspondence).
// 	(child of <td class="ALCell")
// <span class="AL notAbbreviated>: it marks a group of alphabemes (alphabetic letters) that are
// 	not abbreviated in the manuscript (so they have a one-to-one alphabeme/grapheme correspondence).
// 	(child of <td class="ALCell")
// <span class="GL notAbbreviated>: it marks a group of graphemes that are not part of an
// 	abbreviation  in the manuscript (so they have a one-to-one GLphabeme/grapheme correspondence).
// 	(child of <td class="GLCell")
// 
// D) List: Other tables not including words
//
// <table class="lbTable">: its third (bottom) row includes the line numbers when they occur outside of
// 	a word. It has three rows, so that the line numbers can be displayed
// 	in the third row and are thus at the same height of the GL in the browser.
// <table class="spaceTable">: it includes the graphical spaces found in the manuscript.
// 	It has three rows, so that the graphical spaces can be displayed
// 	in the third row and are thus at the same height of the GL in the browser.
// <table class="punctTable">: it includes the punctuation found in the manuscript. It has three rows:
// 	The top row shows the modern correspondent punctuation mark.
// 	The second and third row show the punctuation grapheme found in the manuscript.
//
// E) List: Span elements NOT children of <w> in the XML/TEI source file including medieval text
//
// <span class="LL space">: Space (i.e. delimitator) between linguistic words at the LL. Hierarchy:
// 	<table class="spaceTable"> / <tr> / <td class="LLCell" / <span class="LL space">
// <span class="AL space">: Space (i.e. delimitator) between words at the AL. Hierarchy:
// 	<table class="spaceTable"> / <tr> / <td class="ALCell" / <span class="AL space">
// <span class="GL space">: Space (i.e. delimitator) between graphical words at the GL.
// 	Note that <span class="GL space"> can occur within an XML/TEI <w> element (representing
// 	a linguistic word) or outside it:
// 		In the first case (within <w> in XML/TEI), the hierarchy is
// 			<table class="spaceTable"> / <tr> / <td class="GLCell"> / <span class="GL space">
// 		In the second case (outside of <w> in XML/TEI), the hierarchy is
// 			<table class="wordTable"> / <tr> / <td class="GLCell"> / <span class="GL space">
//
//
// F) List: Div/Span elements that do not include medieval text
//
// <div class="note withinWord"> shows a note by the editor. It occurs inside a XML/TEI <w> element
// 	and refers to that word.
// 	It is a child of <td class="ALCell"> because it is displayed
// 	in the AL row/cell but does not have class="AL", since it does not belong to the medieval text.
// 	The type of the note (value of @type of XML element <note>) is also displayed in the HTML @class:
//	<div class="note withinWord tech">. Substitutes for "tech" may be: "script", "graphic", "source",
//	"content", "emendation".
// <div class="note outsideWord">: same as above, but the note occurs outside of a <w> element.
// 	Like "note withinWord", this is also not a child of <td class="ALCell">, but of the  HTML <div id="MSText">.
// 	Specific values for @class include <div class="note outsideWord tech"> (or "script", "graphic", etc.).
// <div class="note withinWord containerDiv"> or
// <div class="note outsideWord containerDiv">
// 	mark the div that includes the "show/hide note" link and the content of the note
// <a class="note noteToggleLink">: the "show/hide note" link
// <div class="note withinWord contentDiv"> or
// <div class="note outsideWord contentDiv">: the content of the note
// 	
// <span class="lb lbWithinWord"> shows the line number (value 'lb'), when it occurs within a word
// 	(value 'lbWithinWord'). This happens when a graphical word is split between two lines in the
// 	manuscript. It is a child of <td class="GLCell"> because it is displayed
// 	in the GL row/cell but does not have class="GL", since it does not belong to the medieval text.
// <span class="lb lbOutsideWord"> same as above, when the line number occurs outside of a word
// 	This happens when the line break in the manuscript happens between a
// 	word and another. It is a child of <td class="GLCell"> because it is displayed
// 	in the GL row/cell but does not have class="GL", since it does not belong to the medieval text.
// <div class="pb">: it marks the beginning of a new folio  and provides its number.
// <div class="cb">: it marks the beginning of a new column and provides its number.
//
//
// G) List: HTML Elements including words
//
// <span class="unclear wholeword certlow"> normally includes one <table class="wordTable">
// 	or one such table plus one <table class="spaceTable" (but it could include more than one)
// 	and marks that the word is unclear in the manuscript. @class="certlow" means that the
// 	certainty of my reading of the word is low.
// <span class="unclear wholeword certmedium">: same as above, but the certainty is medium.
// <span class="unclear wholeword certhigh">:   same as above, but the certainty is high.
// <span class="add wholeword placeabove">: includes one or more of the following tables:
// 	<table class="wordTable">, 
// 	<table class="punctTable">, 
//	<table class="spaceTable">,
// 	and marks that those words, spaces and punctuation signs have been added above the line in the manuscript.
// <span class="add withinword placeabove">: includes characters (part of a word) that have been added
// 	above the line in the manuscript (so this should not belong in letter G of this list).
// <span class="head">: head of the work (no longer in use)
// <div class="source start containerDiv"> or
// <div class="source end containerDiv">
// 	mark the div that includes the "show/hide source note" link and the content of the source note
// <a class="source sourceToggleLink">: the "show/hide source" link
// <div class="source start contentDiv"> or
// <div class="source end contentDiv">: the content of the note marking the start or end
// 	of a passage imitating a source
// <div class="apparatus corr">: includes words, punctuation signs or gaps that were in the <corr>
// 	element in the XML source.
// <div class="apparatus sic">: includes words, punctuation signs or gaps that were in the <sic>
// 	element in the XML source.
// <td class="apparatus apparatusNote">: the full hierarchy is:
// 	<div class="note outsideWord contentDiv"> / <table> / <tr> / <td class="apparatus apparatusNote">,
//	where the latter <td> includes the textual content of element <note type="emendation"> in the XML
//
//
// H) Summary for LL and AL
//
// To sum up (and not considering punctuation for now):
// 	1) text or space belonging to the LL may be included in:
// 		<span class="LL word">
// 		<span class="LL space">
// 	2) text or space belonging to the AL may be included in one of the following:
// 		<span class="AL notAbbreviated">
// 		<span class="AL abbrExpansion">
// 		<span class="AL larger">
// 		<span class="AL dropcap">
// 		<span class="AL space">
// 	3) for the text belonging to the GL, refer to the list above.

/*##############################
#     GENERAL VARIABLES        #
##############################*/

// I'm using an underscore as value for a space until I'll find a way to effectively insert a &nbsp; through JS
var space = '|';
var noteLikeCounter = 0;
var gtos = importTableOfSigns('GToS.csv');

/*#############################
#   URN INTERPRETATION TABLE  #
##############################*/

var URNArray = [
	['-', ' - '],
	['urn:cts:latinLit:', ''],
	['stoa0234a.stoa001:', 'Priscian from Caesarea, "Ars grammatica", '],
	['stoa0234a.stoa003:', 'Priscian from Caesarea, "De figuris numerorum", '],
	['stoa0110.stoa001:', 'Aelius Donatus, "Ars Minor (De partibus orationis)", '],
	['stoa0110.stoa003:', 'Aelius Donatus, "De Barbarismo", '],
	['stoa0110.stoa004:', 'Aelius Donatus, "De ceteriis vitiis", '],
	['stoa0110.stoa005:', 'Aelius Donatus, "De Metaplasmo", '],
	['stoa0110.stoa006:', 'Aelius Donatus, "De Schematibus", '],
	['stoa0110.stoa007:', 'Aelius Donatus, "De Solecismo", '],
	['stoa0110.stoa008:', 'Aelius Donatus, "De Tropis", '],
	['stoa0233c.stoa001:', 'Pompeius, "Commentum Artis Donati", '],
	['stoa0259.stoa001:', 'Servius, "Commentarius in Artem Donati", '],
	['stoa0258a.stoa001:', 'Sergius, "Explanatio in Artem Donati", '],
	['stoa0290a.stoa001.opp - lat1:',
		'Virgilius Grammaticus, "Opera" (Huemer, Johann, ed., "Virgilii Maronis grammatici opera", Leipzig, 1886), '],
		// I don't know why, but if I don't put spaced around the "-" in "opp-lat1", it doesn't work
		// For the origin of those URNs, see documentation.md
];

/*##############################
# TAGSET INTERPRETATION TABLE #
##############################*/

// This 'explanation' of the PoS tags is based on
// ~/ursus/lemma/tree_tagger_and_related_files/parameter_files/from_treetagger_website/index_thomisticus/Tagset_IT.pdf

var tagsetlist = [
			[
				//'1 Flexional-Type',
				'Flexional-Type',
				[
					[ ['1'], ['Nominal'] ],
					[ ['2'], ['Participial'] ],
					[ ['3'], ['Verbal'] ],
					[ ['4'], ['Invariable'] ],
					[ ['5'], ['Pseudo-lemma'] ]
				]
			],
			[
				//'2 Nominals-Degree',
				'Nominals-Degree',
        			[
					[ ['1'], ['Positive'] ],
					[ ['2'], ['Comparative'] ],
					[ ['3'], ['Superlative'] ],
					[ ['4'], ['Not stable composition'] ],
					[ ['-'], ['None'] ]
				]
			],
        		[
				//'3 Flexional-Category',
				'Flexional-Category',
				[
					[ ['A'], ['I decl'] ],
					[ ['B'], ['II decl'] ],
					[ ['C'], ['III decl'] ],
					[ ['D'], ['IV decl'] ],
					[ ['E'], ['V decl'] ],
					[ ['F'], ['Regularly irregular decl'] ],
					[ ['G'], ['Uninflected nominal'] ],
					[ ['J'], ['I conjug'] ],
					[ ['K'], ['II conjug'] ],
					[ ['L'], ['III conjug'] ],
					[ ['M'], ['IV conjug'] ],
					[ ['N'], ['Regularly irregular conjug'] ],
					[ ['O'], ['Invariable'] ],
					[ ['S'], ['Prepositional (always or not) particle'] ],
					[ ['-'], ['None'] ]
				]
            		],
        		[
				//'4 Mood',
				'Mood',
				[
					[ ['A'], ['Active indicative'] ],
					[ ['J'], ['Pass/Dep indicative'] ],
					[ ['B'], ['Active subjunctive'] ],
					[ ['K'], ['Pass/Dep subjunctive'] ],
					[ ['C'], ['Active imperative'] ],
					[ ['L'], ['Pass/Dep imperative'] ],
					[ ['D'], ['Active participle'] ],
					[ ['M'], ['Pass/Dep Participle'] ],
					[ ['E'], ['Active gerund'] ],
					[ ['N'], ['Passive Gerund'] ],
					[ ['O'], ['Pass/Dep gerundive'] ],
					[ ['G'], ['Active supine'] ],
					[ ['P'], ['Pass/Dep supine'] ],
					[ ['H'], ['Active infinitive'] ],
					[ ['Q'], ['Pass/Dep infinitive'] ],
					[ ['-'], ['None'] ]
				]
            		],
        		[
				//'5 Tense',
				'Tense',
				[
					[ ['1'], ['Present'] ],
					[ ['2'], ['Imperfect'] ],
					[ ['3'], ['Future'] ],
					[ ['4'], ['Perfect'] ],
					[ ['5'], ['Plusperfect'] ],
					[ ['6'], ['Future perfect'] ],
					[ ['-'], ['None'] ]
				]
			],
			[
				//'6 Participials-Degree',
				'Participials-Degree',
				[
					[ ['1'], ['Positive'] ],
					[ ['2'], ['Comparative'] ],
					[ ['3'], ['Superlative'] ],
					[ ['-'], ['None'] ]
				]
			],
			[
				//'7 Case/Number',
				'Case/Number',
				[
					[ ['A'], ['Singular Nominative'] ],
					[ ['J'], ['Plural Nominative'] ],
					[ ['B'], ['Singular Genitive'] ],
					[ ['K'], ['Plural Genitive'] ],
					[ ['C'], ['Singular Dative'] ],
					[ ['L'], ['Plural Dative'] ],
					[ ['D'], ['Singular Accusative'] ],
					[ ['M'], ['Plural Accusative'] ],
					[ ['E'], ['Singular Vocative'] ],
					[ ['N'], ['Plural Vocative'] ],
					[ ['F'], ['Singular Ablative'] ],
					[ ['O'], ['Plural Ablative'] ],
					[ ['G'], ['Adverbial'] ],
					[ ['H'], ['Casus "plurimus"'] ],
					[ ['-'], ['None'] ]
				]
            		],
			[
				//'8 Gender/Number/Person',
				'Gender/Number/Person',
				[
					[ ['1'], ['Masculine'] ],
					[ ['2'], ['Feminine'] ],
					[ ['3'], ['Neuter'] ],
					[ ['4'], ['I singular'] ],
					[ ['5'], ['II singular'] ],
					[ ['6'], ['III singular'] ],
					[ ['7'], ['I plural'] ],
					[ ['8'], ['II plural'] ],
					[ ['9'], ['III plural'] ],
					[ ['-'], ['None'] ]
				]
			],
			[
				//'9 Composition',
				'Composition',
				[
					[ ['A'], ['Enclytic -ce'] ],
					[ ['C'], ['Enclytic -cum'] ],
					[ ['M'], ['Enclytic -met'] ],
					[ ['N'], ['Enclytic -ne'] ],
					[ ['Q'], ['Enclytic -que'] ],
					[ ['T'], ['Enclytic -tenus'] ],
					[ ['V'], ['Enclytic -ve'] ],
					[ ['H'], ['Ending homographic with enclytic'] ],
					[ ['Z'], ['Composed with other form'] ],
					[ ['W'], ['As lemma'] ],
					[ ['-'], ['None'] ]
            			]
			],
			[
				//'10 Formal-Variation',
				'Formal-Variation',
				[
					[ ['A'], ['I variation of wordform'] ],
					[ ['B'], ['II variation of wordform'] ],
					[ ['C'], ['III variation of wordform'] ],
					[ ['X'], ['Author mistake, or bad reading?'] ],
					[ ['-'], ['None'] ]
				]
			],
			[
				//'11 Graphical-Variation',
				'Graphical-Variation',
				[
					[ ['1'], ['Baseform'] ],
					[ ['2'], ['Graphical variation A'] ],
					[ ['3'], ['Graphical variation B'] ],
					[ ['4'], ['Graphical variation C'] ],
					[ ['5'], ['Graphical variation D'] ],
					[ ['6'], ['Graphical variation E'] ],
					[ ['-'], ['None'] ]
				]
            		]
        ];


/*##############################
#         MY FUNCTIONS         #
##############################*/

function showMe (it, box) {
	// This function lets the user choose which layer (GL and/or AL) to visualize
	var vis = (box.checked) ? 'visible' : 'hidden';
	[].forEach.call(document.querySelectorAll('.' + it), function (el) {
		el.style.visibility = vis;
		});
	/*
	// Uncomment this code block to 
	// make the interlinear space vary when only one layer is visible.
	if ( it == 'GL' && vis != 'visible' )
	{
	alert('Reducing interlinear space');
	[].forEach.call(document.querySelectorAll('.ALCell'), function (elx) {
		elx.style.paddingTop = '0em';
		});
	}
	else
	{
	alert('Increasing interlinear space');
	[].forEach.call(document.querySelectorAll('.ALCell'), function (ilx) {
		ilx.style.paddingTop = '1.5em';
		});
	}
	*/
}

function translateAnaString(inputAnaString) {
	var anaList = [];	 // trasforma § write in append (push) to list
	for (var i = 0; i < tagsetlist.length; i++) {
		for (var h = 0; h < tagsetlist[i].length; h++) {
			if ( anaValue[i] == tagsetlist[i][h][0] && anaValue[i] != '-' ) {
				document.write(tagsetlist[i][h][1] + '<br/>');
			}
		}
	}
}

function importTableOfSigns(csvFile) {
	// Import the Table of Signs. It parses a csv with tabs as delimitators
	// and returns an array where every element is an array. In the latter array:
	// 	element 0 is the character representing a grapheme
	// 	element 1 is the character representing the corresponding alphabeme
	// 	element 2 is the character to use to visualize the grapheme in an browser
	// 	element 3 is  the 'type'  (Alphabetic, punctuation etc.)
	// 	element 4 are the 'notes'
	// 	element 5 are the JPG images of the allographs 
	var xmlhttp;
	xmlhttp=new XMLHttpRequest();
	xmlhttp.open('GET', csvFile, false);
	//xmlhttp.open('GET', csvFile, true); // With 'true' I don't get Firefox's warning, but the CSV file is not parsed
	xmlhttp.send();
	var ToSLines = xmlhttp.responseText.split('\n');
	var ToS   	= [];
	var ToSCells	= [];
	for (var igl = 0; igl < ToSLines.length; igl++) {
		ToSCells = ToSLines[igl].split('\t');
		ToS[igl] = [];
		ToS[igl][0] = ToSCells[0];
		ToS[igl][1] = ToSCells[1];
		ToS[igl][2] = ToSCells[2];
		ToS[igl][3] = ToSCells[3];	// Only used when showing the GToS in an HTML table
		ToS[igl][4] = ToSCells[4];	// Only used when showing the GToS in an HTML table
		ToS[igl][5] = ToSCells[5];	// Only used when showing the GToS in an HTML table
		}
	return ToS;
}

function tableOfSignsToHTMLTable() {
	// This function transforms the table of sign into an HTML table.
	// It should be called by a gtos.html file
	for (var igx = 0; igx < gtos.length; igx++) {
		gtosTr = document.createElement('tr');
		document.getElementById('gtosHtmlTable').appendChild(gtosTr);
		for (var igy = 0; igy < gtos[igx].length; igy++) {

			// Create THs for first row, TDs for the next rows
			if ( igx == 0 ) { gtosTd = document.createElement('th'); }
			else {
				gtosTd = document.createElement('td');
				gtosTd.setAttribute('class', 'td'+igy);
			}

			// Set column width
			if ( igy == 4 ) { gtosTd.setAttribute('width', '400px'); }
			else if (igy == 2) { gtosTd.setAttribute('width', '10px') }

			// Insert <img>s
			if ( igy == 5 && typeof(gtos[igx][igy]) != 'undefined' && igx != 0) {
				var imagesList = gtos[igx][igy].split(' '); // Filenames in the CSV cell are separated by spaces
				var gtosTdString = '';
				for (var imgx = 0; imgx < imagesList.length; imgx++) {	// For each filename in the image list
					if ( imagesList[imgx] ) {
						var imgElem = document.createElement('img');
						imgElem.setAttribute('src', 'glyph_images/' + imagesList[imgx]);
						//imgElem.setAttribute('height', '50px');
						imgElem.setAttribute('alt', imagesList[imgx]);
						imgElem.setAttribute('title', imagesList[imgx]);
						gtosTd.appendChild(imgElem);
					}
				}
			}


			// ...else, create a simple text node and append it
			else if ( typeof(gtos[igx][igy]) != 'undefined' ) {
				gtosTdTextNode  = document.createTextNode(gtos[igx][igy]);
				gtosTd.appendChild(gtosTdTextNode);
			}
			gtosTr.appendChild(gtosTd);
		}
	}
}

function graph(myString) {
	// This function inputs a string of characters representing graphemes
	// in the XML/TEI source file and returns a string of characters
	// that will be used to display the graphemes in the browser
	for (var igr = 0; igr < gtos.length; igr++) {
		// gtos[igr][0] (value of first column of GToS.csv):
		// 	character representing the grapheme in the XML/TEI file
		// gtos[igr][1] (value of second column of GToS.csv):
		// 	character representing the alphabeme
		if (gtos[igr][0] != '' && gtos[igr][2] != '') {
			myString = myString.replace(gtos[igr][0], gtos[igr][2]);
		}
	}
	return myString;
}

function alph(myString) {
	// This function inputs a string of characters representing graphemes (myString)
	// and returns a string of characters representing alphabemes, mapping the graphemes
	// to their standard alphabetical meaning as encoded in the first and second column
	// of the "Graphemic Table of Signs" (GToS).
	for (var ialph = 0; ialph < gtos.length; ialph++) {
		// gtos[ialph][0] (value of first column of GToS.csv):
		// 	character representing the grapheme in the XML/TEI file
		// gtos[ialph][1] (value of second column of GToS.csv):
		// 	character representing the alphabeme
		//if (gtos[ialph][0] != '' && gtos[ialph][1] != '') { // The next line should be more efficient
		if ( gtos[ialph][0] != '' && gtos[ialph][1] != '' && gtos[ialph][0] != gtos[ialph][1] ) {
			//alert(gtos[ialph][0] + "→" + gtos[ialph][1]);
			myString = myString.replace(gtos[ialph][0], gtos[ialph][1]);
		}
	}
	return myString;
}

function URNToCitation(URNToParse) {
	for (var iurn = 0; iurn < URNArray.length; iurn++) {
		URNToParse = URNToParse.replace(URNArray[iurn][0], URNArray[iurn][1]);
	}
	return URNToParse;
}

function toggle_visibility(id) {
   var e =document.getElementById(id);
   //var label = document.getElementById("x");

   if(e.style.display == 'none')
    {
      //label.innerHTML = label.innerHTML.replace("[+]","[-]");
      e.style.display = 'block';
      //col.innerHTML=valu;
    }
   else
   {
      //label.innerHTML = label.innerHTML.replace("[-]","[+]");
      e.style.display = 'none';

   }
}

function classyElem(elementName, classForElement, textToWrap) {
	// This wraps some text in an element with a specific HTML @class attribute
	// and returns one value, being a HTML element.
	// For example, if elementName='span' and classForElement='lb', it returns:
	// 	<span class="lb">textToWrap</span>
	outputElement = document.createElement(elementName);		// Create the <span> element
	outputElement.setAttribute('class', classForElement);		// Set attribute
	classyText  = document.createTextNode(textToWrap.trim());	// The text node
	outputElement.appendChild(classyText);				// Append the text inside the span
	return outputElement;
}

function classySpanWithLayers(textToWrap, classForSpan) { //
	// This wraps some text in a span with a specific HTML @class attribute
	// and returns an array with three values, being HTMl elements <span>.
	// For example, if classForSpan='hi':
	// 	value 0 is a <span> HTML object for the LL, e.g. <span class="LL hi">
	// 	value 1 is a <span> HTML object for the AL, e.g. <span class="AL hi">
	//      value 2 is a <span> HTML object for the GL, e.g. <span class="GL hi">
	var editionLayers = ['LL', 'AL', 'GL'];
	var outputSpan = [];
	var classyText = [];
	for (var xy = 0; xy < editionLayers.length; xy++) {	//Iterates through the three layers
		outputSpan[xy] = document.createElement('span');    // Create the <span> element
		outputSpan[xy].setAttribute('class', editionLayers[xy]+' '+classForSpan); // Set attribute
		classyText[xy]  = document.createTextNode(textToWrap.trim()); // The text node
		outputSpan[xy].appendChild(classyText[xy]);      // Append the text inside the span
	}
	return outputSpan;
}
  
function expandableDiv(parentElement, divClasses, anchorClasses, anchorString, divContentString) {
	var containerDiv = classyElem('div', divClasses+' containerDiv', '');
	parentElement.appendChild(containerDiv);
	// Create and append <a> 
	// ntl = noteToggleLink
	var ntl = classyElem('a', anchorClasses, anchorString);
	containerDiv.appendChild(ntl);
	ntl.setAttribute('href', '#');
	// Create the note content <div>, give it an @id and append it
	var contentDiv = classyElem('div', divClasses+' contentDiv', divContentString);
	noteLikeCounter++;
	var noteLikeId = 'noteLike'+ noteLikeCounter;
	contentDiv.setAttribute('id', noteLikeId);
	containerDiv.appendChild(contentDiv);
	contentDiv.style.display = 'none';
	// Tell <a> to toggle visibility of note content <div>
	ntl.setAttribute('onclick', 'toggle_visibility("' + noteLikeId + '");return false;');
	return contentDiv;
}

function makeTable(whereToAppendTable, tableClass) {
	// Create a table with three rows (one for each layer: LL, AL, GL)
	// The fist argument is the element into which the table must be appended. E.g., one could provide
	// 	document.getElementById('MSText')
	// The second argument is a string that will be the value of the @class attribute. if 'string' is
	// provided, the table will have:
	// 	<table class="tableClass">
	var table = document.createElement('table');                 // Create a word <table> node
	table.setAttribute('class', tableClass);				// Set attribute
	// Append 3 rows with 1 cell each, indexed as 0, 1 and 2
	cellClasses = ['LLCell', 'ALCell', 'GLCell'];
	rows  = [];
	cells = [];
	for (var y = 0; y < 3 ; y++) {	// Create 3 rows: 0=LL; 1=AL; 2=GL
		rows[y] = table.insertRow(y);
		cells[y] = rows[y].insertCell(0);
		cells[y].setAttribute('class', cellClasses[y]);		// Set attribute class (LL, AL or GL)
	}
	// document.getElementById('MSText').appendChild(table);
	whereToAppendTable.appendChild(table);
	return cells;
}

function computeAddLikeChildren(xmlUnclearLikeElem, htmlParentElem, unclearLikeElemClass) {
	// Argument xmlUnclearLikeElem is an element like <unclear>,
	// <add>, <sic> and <corr>, i.e. an element that can include
	// a number of <w>s, <pc>s or <gap>s.
	for (var zy = 0; zy < xmlUnclearLikeElem.childNodes.length; zy++) {
		// If <add> or <unclear> include <w>.
		// In the case of <choice>/<sic>+<corr>, this 'for' cycle
		// visualized the content of <corr>
		if (xmlUnclearLikeElem.childNodes[zy].tagName == 'w') {
			// xmlUnclearLikeElem is <add> or <unclear>
			// xmlUnclearLikeElem.childNodes[zy]) is a <w> child of <add> or <unclear>
			// The next lines transform the XML/TEI <w> into
			// an HTML <table> and appends the table
			// to the <span class="add"> or <span class="unclear"> HTML element.
			auSpan = document.createElement('span'); //Create the <span> element that
				//will be parent of a <table>. A <span> should not be parent of
				// <table> in HTML, but I have no choice. If I chose <div>, it
				// would not appear inline with the other portions of text in the browser.
			auSpan.setAttribute('class', unclearLikeElemClass);
			auSpan.appendChild(wordify(xmlUnclearLikeElem.childNodes[zy]));
			htmlParentElem.appendChild(auSpan);
			//document.getElementById('MSText').appendChild(auSpan);
			//alert('"'+xmlUnclearLikeElem.childNodes[zy].textContent+'"')
		}
		else if (xmlUnclearLikeElem.childNodes[zy].tagName=='pc') { // If <add> or <unclear> include <pc>
			auSpan = document.createElement('span');
			auSpan.setAttribute('class', unclearLikeElemClass);
			auSpan.appendChild(punctify(xmlUnclearLikeElem.childNodes[zy]));
			htmlParentElem.appendChild(auSpan);
			document.getElementById('MSText').appendChild(auSpan);
		}
		else if (xmlUnclearLikeElem.childNodes[zy].tagName == 'gap') {
			// <gap> within <add> or <unclear>
			gapify(xmlUnclearLikeElem.childNodes[zy]);
		}
	}
}

function computeWordLikeElements(refElement) {
	// This function accepts a <ref> element as parameter and iterates
	// over the wordLike children of each <ref>

	// Start of source
	// At the opening tag of <ref>, 
	// if XML/TEI @cRef is not "unknown", mention that a new source reference is starting
	if (refElement.attributes.getNamedItem('cRef').nodeValue != 'unknown') {
		var URNList = refElement.attributes.getNamedItem('cRef').nodeValue.split(' ');
		if (URNList.length == 1) {
			var sourceStartString = 'Start of source: '+URNToCitation(URNList[0]);
		}
		else {
			var sourceStartString = 'Start of sources: ';
			for (var qi = 0; qi < URNList.length; qi++) {	// For each URN in the URN list
				var sourceStartString = sourceStartString + URNToCitation(URNList[qi]);
				if (qi < URNList.length-2) {
					sourceStartString += '; ';
				}
				else if (qi == URNList.length-2) {
					sourceStartString += ' and ';
				}
			}
		}
		sourceStartString += ' →';

		expandableDiv(
				document.getElementById('MSText'),
				'source start',
				'source sourceToggleLink',
				'Source start',
				sourceStartString
				);

	}


	for (var j = 0; j < refElement.childNodes.length; j++) {  // 
		// Iterate all elements children of <ref> (all wordLike elements).
		// They may be: <w>, <lb>, <pc>, <note> etc.
		var e = refElement.childNodes[j]; // 'e' is alement such as <w>, <lb>, <pc> etc.
		
		if (e.tagName == 'w') {
			// Words (<w>)
			// Function wordify() returns an HTML <table> element. It is now appended to 
			// <div id="MSText">
			document.getElementById('MSText').appendChild(wordify(e));
		}

		else if (e.tagName == 'lb') {
			// <lb> outside <w>
			var myCells = makeTable(document.getElementById('MSText'), 'lbTable');
			var lbTextString = '['+e.attributes.getNamedItem('n').nodeValue+']';
			// I'm populating all three rows of the table (the first two, with space spans 
			myCells[0].appendChild(classySpanWithLayers(space, 'space')[0]);
			myCells[1].appendChild(classySpanWithLayers(space, 'space')[1]);
			// The next table cell (in the bottom row) has a space plus the line number (the space
			// 	is needed to make the line number appear underneath (i.e. as a 'subscript').
			// 	Since this space must look invisible (white font color on white
			// 	background), I'm using 
			// 	classySpanWithLayers(space, 'space')[1]
			// 	for it. This function returns: <span class="AL space">_</space>,
			// 	and the "AL space" class in the CSS file has white font on white background.
			myCells[2].appendChild(classySpanWithLayers(space, 'space')[1]);
			//Append lb span inside the <td>
			myCells[2].appendChild(classyElem('span', 'lb lbOutsideWord', lbTextString)); 
		}

		// New code
		else if (e.tagName == 'pb' || e.tagName == 'cb') {
			// <pb> or <cb> (they always occur outside <w>)
			pbCbN = e.attributes.getNamedItem('n').nodeValue;
			var divPbCb  = classyElem('div', e.tagName, ''); // Create a <div class="pb"> or class="cb"
			var divPbCbAIcon = document.createElement('img'); // Create an <img> element
			divPbCbAIcon.setAttribute('src', 'icons/'+e.tagName+'.png'); //Add src="icons/pb.png" or src="icons/cb.png"
			if (e.tagName == 'pb') {
				var pbCbTextString = 'Start of folio '+pbCbN;
				divPbCbAIcon.setAttribute('title', pbCbTextString); // Add title="Start of folio..." to <img>
				// Check if the folio number has one digit only
				var patt = /^\d\D/g;	// 2 digit chars followed by a non-digit char. E.g.: '12r'
				if (patt.test(pbCbN)) {		// Like '2r'
					pbCbN = '0' + pbCbN	// If folio is like '2r' (1 digit), make it like '02r'
				}
				// Create link to image file
				var imgURL = 'manuscript_images/C_' + pbCbN + '.JPG';
				var divPbCbA = document.createElement('a');
				divPbCbA.setAttribute('href', imgURL);
				divPbCbA.appendChild(divPbCbAIcon); // Insert <img> into <a>
				divPbCb.appendChild(divPbCbA);	// Insert <a> into <div>
			}
			else if (e.tagName == 'cb') {
				var pbCbTextString = 'Column '+pbCbN.split('.')[1]+' of folio '+pbCbN.split('.')[0];
				divPbCbAIcon.setAttribute('title', pbCbTextString); // Add title="Start of column..." to <img>
				divPbCb.appendChild(divPbCbAIcon); // Insert <img> into <div>
			}
			document.getElementById('MSText').appendChild(divPbCb); //Insert <div> into the main <div> of the page
		}

		else if (e.tagName == 'pc') {
			// <pc type="space"> (spaces) or punctuation signs outside of <w>
			punctify(e)
		}

		else if (e.tagName == 'gap') {
			// <gap> outside of <w>
			var myCells = makeTable(document.getElementById('MSText'), 'gapTable');
			gapify(e);
		}

		else if (e.tagName == 'add') {
			var auClass = 'add wholeword place'+e.attributes.getNamedItem('place').nodeValue;
			// The resulting content of auSpan will be "placeabove". If XML/TEI has
			// <add place="above">, the HTML DOM will have <span class="add placeabove">.
			computeAddLikeChildren(e, document.getElementById('MSText'), auClass)
		}

		else if (e.tagName == 'unclear') {
			var auClass = 'unclear wholeword cert'+e.attributes.getNamedItem('cert').nodeValue;
			// The resulting content of auSpan will be "certlow", "certmedium" or "certhigh"
			// If XML/TEI has <unclear cert="medium">, the HTML DOM will have
			// <span class="unclear wholeword certmedium">
			computeAddLikeChildren(e, document.getElementById('MSText'), auClass)
		}

		else if (e.tagName == 'choice') {
			sic = e.getElementsByTagName('sic')[0]; 
			corr = e.getElementsByTagName('corr')[0];

			if (corr.attributes.getNamedItem('cert')) {
				var corrCert = corr.attributes.getNamedItem('cert').nodeValue; // eg.: cert="medium"
				}

			if (corr.getElementsByTagName('note')[0]) {
				// If <corr> has a <note type="emendation">, store its content in
				// variable emendNoteString.
				emendNote = corr.getElementsByTagName('note')[0];
				emendNoteString = emendNote.childNodes[0].nodeValue.trim();
			}

			else {
				// If <corr> has no <note type="emendation">, then <corr> has a @type.
				// Find in <correction>/<p>/<list> the <item> whose @n corresponds
				// to the @type of <corr>, and store the textual content of that
				// <item> in variable emendNoteString
				if (corr.attributes.getNamedItem('type')) {
					corrType = corr.attributes.getNamedItem('type').nodeValue; // eg.: type="ub"
					correction = xmlDoc.getElementsByTagName('correction')[0];
					correctionList = correction.getElementsByTagName('p')[0].getElementsByTagName('list')[0];
					correctionItems = correctionList.getElementsByTagName('item')
					for (var icl = 0; icl < correctionItems.length; icl++) {
						item = correctionItems[icl];
						if (item.attributes.getNamedItem('n').nodeValue == corrType) {
							emendNoteString = item.childNodes[0].nodeValue.trim();
						}
					}
				}
				else {
					alert('This choice/sic/corr emendation has no <note type="emendation" or <corr type="...">');
				}
			}

			computeAddLikeChildren(corr, document.getElementById('MSText'), 'apparatus corr ' + corrCert); // Result:
				//for each <w>, <pc> or <gap>, this is created:
				// <span class="apparatus corr medium"> <table>[three rows]</table></span>
				// (or: class="apparatus corr high", or: class="apparatus corr low")
				
			sicDiv = expandableDiv( // sicDiv is <div class="note apparatus contentDiv">
							// including a text Node with '' as textual content
					document.getElementById('MSText'),
					'note emendation',
					'note noteToggleLink',
					'*',
					'The MS has:'
					);
			computeAddLikeChildren(sic, sicDiv, auClass + 'apparatus sic'); // Result: for each <w>, <pc> or <gap>
				// this is appended inside <div class="note apparatus contentDiv">:
				// <span class="apparatus sic"> <table>[three rows]</table></span>
			emendNoteTable = document.createElement('table');    // Create a table inside which I'll put the
				// textual content of <note type="emendation">
			emendNoteTR = document.createElement('tr');
			emendNoteTD = document.createElement('td');
			emendNoteTD.setAttribute('class', 'apparatus apparatusNote');
			emendNoteText = document.createTextNode(emendNoteString);
			emendNoteTD.append(emendNoteText);
			emendNoteTR.append(emendNoteTD);
			emendNoteTable.append(emendNoteTR);
			sicDiv.append(emendNoteTable); // Result:
				//<table><tr><td>[textual content of <note type="emendation"]</td></tr></table>
		}

		else if (e.tagName == 'note') {
			// <note> outside of <w>, i.e. note to section
			expandableDiv(
					document.getElementById('MSText'),
					'note outsideWord '+e.attributes.getNamedItem('type').nodeValue,
					'note noteToggleLink',
					//'Note to section (' + e.attributes.getNamedItem('type').nodeValue + ')',
					'*',
					e.childNodes[0].nodeValue.trim()
					);
		}

	}	// End of iteration over all children of <ref> (=all wordLike elements)


	// End of source
	// We are now just before </ref> (the end tag of <ref>).
	// Write that the source mentioned in @cRef finishes here.
	if (refElement.attributes.getNamedItem('cRef').nodeValue != 'unknown') {
		var URNList = refElement.attributes.getNamedItem('cRef').nodeValue.split(' ');
		if (URNList.length == 1) {
			var sourceEndString = '← End of source: '+URNToCitation(URNList[0]);
		}
		else {
			var sourceEndString = '← End of sources: ';
			for (var qi = 0; qi < URNList.length; qi++) {	// For each URN in the URN list
				var sourceEndString = sourceEndString + URNToCitation(URNList[qi]);
				if (qi < URNList.length-2) {
					sourceEndString += '; ';
				}
				else if (qi == URNList.length-2) {
					sourceEndString += ' and ';
				}
			}
		}
		expandableDiv(
				document.getElementById('MSText'),
				'source end',
				'source sourceToggleLink',
				'Source end',
				sourceEndString
				);
	}
}	// End of function iterateOverRefs

function wordify(word) {
	// This function takes a <w> HTML element as parameter
	// and returns an HTML <table> element including three <tr>, each including one <td>. Each <td>
	// refers to one layer (LL, AL and GL) and includes one ore more <span> elements
		
	// Append word table
	var table = document.createElement('table');                 // Create a word <table> node
	table.setAttribute('class', 'wordTable');				// Set attribute class="word"
	// Append 3 rows with 1 cell each, indexed as 0, 1 and 2
	cellClasses = ['LLCell', 'ALCell', 'GLCell'];
	rows  = [];
	cells = [];
	for (var y = 0; y < 3 ; y++) {	// Create 3 rows: 0=LL; 1=AL; 2=GL
		rows[y] = table.insertRow(y);
		cells[y] = rows[y].insertCell(0);
		cells[y].setAttribute('class', cellClasses[y]);		// Set attribute class (LL, AL or GL)
	}

	/*
	// Extract the LL: old version (visualizing the modern spelling)
	var LLString = word.attributes.getNamedItem('n').nodeValue;
	var LLText = document.createTextNode(LLString);
	var LLSpan = document.createElement('span');    // Create a <span> node. The hierarchy in the DOM
		// will be: <table class="wordTable"><tr><td class="LLCell"><span class="LL word">
	LLSpan.setAttribute('class', 'LL word spelling');        // Set attribute class
	LLSpan.appendChild(LLText);             	// Append the text inside the LL span
	cells[0].appendChild(LLSpan);                   // Append the span inside the <td class="LLCell">
	*/

	// Extract the LL: new version (visualizing 1. modern spelling; 2. lemma; 3. morphological analysis)
	var LLform = word.attributes.getNamedItem('n').nodeValue;
	if ( word.hasAttribute('type') ) {
		// If word type is "nonsense", "alphabemes" or "foreign",
		// so the word most probably was not lemmatized and <w> doesn't have @ana or @lemma
		var LLString = '"' + LLform + '" (word type: ' + word.attributes.getNamedItem('type').nodeValue + ')';
		// The following lines visualize words with type "nonsense", "alphabemes" or "foreign" differently
		// at the AL
		var wordType = word.attributes.getNamedItem('type').nodeValue; // Value of 'type' in the XML
		oldCells1Attr = cells[1].attributes.getNamedItem('class').value; // Old value of 'class' in the DOM
		newCells1Attr = oldCells1Attr + ' ' + wordType;
		cells[1].setAttribute('class', newCells1Attr); // cells[1]: AL. The result will be like: class="ALCell foreign"
	}
	else { 
		var LLtagsetAna = word.attributes.getNamedItem('ana').nodeValue;
		var LLexpandedAna = tagsetify(LLtagsetAna);
		var LLlemma = word.attributes.getNamedItem('lemma').nodeValue;
		var LLString = '"'+LLform+'": ['+LLlemma+'] '+LLexpandedAna;
	}
	var LLText = document.createTextNode(LLString);
	var LLSpan = document.createElement('span');    // Create a <span> node. The hierarchy in the DOM
		// will be: <table class="wordTable"><tr><td class="LLCell"><span class="LL word">
	LLSpan.setAttribute('class', 'LL word triform');        // Set attribute class
	LLSpan.appendChild(LLText);             	// Append the text inside the LL span
	cells[0].appendChild(LLSpan);                   // Append the span inside the <td class="LLCell">

	//Iterate all children of <w>
	for (var x = 0; x < word.childNodes.length; x++) {
		var n = word.childNodes[x];

		if (n.tagName == 'hi' && (
					n.attributes.getNamedItem('rend').nodeValue == 'larger' ||
					n.attributes.getNamedItem('rend').nodeValue == 'dropcap'
					)
		   )
		{
			var hiRendAttrValue = n.attributes.getNamedItem('rend').nodeValue;
			// Larger initial grapheme, encoded with <hi rend="larger"> in XML/TEI.
			var hiText = n.childNodes[0].nodeValue.trim();
			// AL of larger (span).
				// The result will be <span class="AL larger"
				//                or  <span class="AL dropcap":
			cells[1].appendChild(classySpanWithLayers(alph(hiText), hiRendAttrValue)[1]);
			if (viewLL == true)
			{
				cells[1].setAttribute('title', LLString);//The 'title' will make lemma/morph/spelling appear on hover
			}
			// GL of larger grapheme (span).
				// The result will be <span class="GL larger"
				//                or  <span class="GL dropcap":
			cells[2].appendChild(classySpanWithLayers(hiText, hiRendAttrValue)[2]);
				// Value "GL" comes from function classySpanWithLayers()
				// classySpanWithLayers(...)[2] includes class="GL"
		}

		else if (n.tagName == 'gap') {
			// <gap> within <w>
			gapify(n);
		}

		else if (n.tagName == 'unclear' || n.tagName == 'add') {
			// <add> or <unclear> within <w>
			auSpanAL = document.createElement('span');		// Create the <span> element
			auSpanGL = document.createElement('span');		// Create the <span> element

			// If XML/TEI has <add place="above">, the HTML DOM will have
			// <span class="add placeabove">.
			if (n.tagName == 'add') {
				var auClass = 'add wordpart place'+n.attributes.getNamedItem('place').nodeValue;
				// The resulting content of auSpan will be "placeabove"
				// If XML/TEI has <add place="above">, the HTML DOM will have
				// <span class="add wordpart placeabove">
			}
			if (n.tagName == 'unclear') {
				var auClass = 'unclear wordpart cert'+n.attributes.getNamedItem('cert').nodeValue;
				// The resulting content of auSpan will be "certlow", "certmedium" or "certhigh"
				// If XML/TEI has <unclear cert="medium">, the HTML DOM will have
				// <span class="unclear wordpart certmedium">
			}

			auSpanAL.setAttribute('class', 'AL '+auClass);	// Set attribute
			auSpanGL.setAttribute('class', 'GL '+auClass);	// Set attribute


			var auTextAL = document.createTextNode(n.textContent); // Text node
			var auTextGL = document.createTextNode(n.textContent); // Text node

			auSpanAL.appendChild(auTextAL);
			auSpanGL.appendChild(auTextGL);

			cells[1].appendChild(auSpanAL); //In the AL cell
			if (viewLL == true)
			{
				cells[1].setAttribute('title', LLString);//The 'title' will make lemma/morph/spelling appear on hover
			}
			cells[2].appendChild(auSpanGL); //In the GL cell
		}

		else if (n.tagName == 'note') {
			// <note> inside <w>
			expandableDiv(
					// cells[0], // Old version, with which I appended notes-to-word to the LL cell row
					cells[1], // Now notes to word are appended to the AL cell row
					'note withinword '+n.attributes.getNamedItem('type').nodeValue,
					'note noteToggleLink',
					//'Note to word (' + n.attributes.getNamedItem('type').nodeValue + ')',
					'*',
					n.childNodes[0].nodeValue.trim()
					);
		}

		else if (n.tagName == 'lb') {
			// <lb> inside <w>
			var lbTextString = '['+n.attributes.getNamedItem('n').nodeValue+']';
			//Append lb span inside the <td>
			cells[2].appendChild(classyElem('span', 'lb lbWithinWord', lbTextString));
		}
	
		else if (n.tagName == 'pc' && n.attributes.getNamedItem('type').nodeValue == 'space') {
			// <pc type="space"> (spaces) within <w>
			// 	Yes, sometimes there is a (graphical) space within a (linguistic) word.
			// 	This means that the scribe considers it to be two words, while contemporary
			// 	conventions consider it one word. Example:
			// 	  Contemporary convention: unicuique
			// 	  Scribe's     convention: uni cuique
			//cells[1].appendChild(classySpanWithLayers(space, 'space')[1]); // Put it in the AL cell
			cells[2].appendChild(classySpanWithLayers(space, 'space')[2]); // Put it in the GL cell
		}

		else if (n.tagName == 'choice') {
			// Abbreviations
			var abbr = n.getElementsByTagName('abbr')[0];

			// Extracts the GL of abbreviations
			var GLBaseGraphemes = '';
			for (var z = 0; z < abbr.childNodes.length; z++) {
				
				// This loop Iterates all children of 'abbr' and extracts the
				// graphemes under the abbreviation mark and the abbreviation
				// mark itself
				
				// GL: Base graphemes
				if (abbr.childNodes[z].tagName != 'am') {
					// Sometimes <abbr> includes a <hi>
					if (abbr.childNodes[z].tagName == 'hi') {
						var hiText = abbr.childNodes[z].childNodes[0].nodeValue.trim();
						var hiText = graph(hiText); // This will make '¢' show as ̲q etc.
						// The content of CLBaseGraphemesContent is a
						// <span class="GL larger"> element
						var GLBaseGraphemesContent =
							classySpanWithLayers(hiText, 'larger')[2];
					}
					else {
						GLBaseGraphemes = ''
						GLBaseGraphemes = abbr.childNodes[z].nodeValue.trim();	
						GLBaseGraphemes = graph(GLBaseGraphemes); // This will make '¢' show as ̲q etc.

						// The content of the 'base graphemes' is a text node.
						// Create text node
 						var GLBaseGraphemesContent  =
							document.createTextNode(GLBaseGraphemes);
					}
				// GL: Create a span to include whatever is the content of the 'base graphemes'
				// (either it's a <span class="larger"> or a text node)
				var GLBaseGraphemesSpan = document.createElement('span');
				GLBaseGraphemesSpan.setAttribute('class', 'GL base '+
						abbr.attributes.getNamedItem('type').nodeValue);
				GLBaseGraphemesSpan.appendChild(GLBaseGraphemesContent);      
				}
				
				// GL: The abbreviation mark
				else {
					// The textual content of <span class="GL am">:
					var GLAbbrMark = abbr.childNodes[z].childNodes[0].nodeValue.trim();
					// I'm using function graph() to show the content of column
					// "Grapheme visualization" of the GToS:
					var GLAbbrMark = graph(GLAbbrMark);
					//Create text node
 					var GLAbbrMarkText  = document.createTextNode(GLAbbrMark); 
					var GLAbbrMarkSpan = document.createElement('span');
					// The values of @class for the Abbreviation Mark <span> in HTML
					// are "GL am" plus the value of @type in XML/TEI, i.e.:
					// "GL am superscription", "GL am after", "GL am brevigraph"
					// or "GL am omission"
					GLAbbrMarkSpan.setAttribute('class', 'GL am '+
							abbr.attributes.getNamedItem('type').nodeValue);
					// Append GL abbreviation mark to the span (if any)
					GLAbbrMarkSpan.appendChild(GLAbbrMarkText);      
				}
			}

			// Append GL span for base grapheme(s)
			cells[2].appendChild(GLBaseGraphemesSpan);      
			// Append GL span for abbreviation mark, if the abbreviation type is not 'brevigraph'
			// or 'omission' (brevigraphs and omission-only abbreviations have no abbreviation mark)
			abbrType = abbr.attributes.getNamedItem('type').nodeValue;
			if (abbrType != 'brevigraph' && abbrType != 'omission') {
				cells[2].appendChild(GLAbbrMarkSpan);      
			}

			// Extract the AL of abbreviations
			var ALTextString = n.getElementsByTagName('expan')[0].childNodes[0].nodeValue.trim();
			ALTextString = alph(ALTextString);
			ALTextSpan = classySpanWithLayers(ALTextString, 'abbrExpansion')[1];
			cells[1].appendChild(ALTextSpan);
			if (viewLL == true)
			{
                        	cells[1].setAttribute('title', LLString);//The 'title' will make lemma/morph/spelling appear on hover
			}
		}	// End of 'choice', i.e. of the processing of abbreviations

		else if (n.tagName != 'choice') {
			// Graphemes outside abbreviations
			// AL
			var ALTextString = n.nodeValue.trim();
			ALTextString = alph(ALTextString); //Compute the AL based on the graphemes and the GToS
			cells[1].appendChild(classySpanWithLayers(ALTextString, 'notAbbreviated')[1]);
			if (viewLL == true)
			{
				cells[1].setAttribute('title', LLString);//The 'title' will make lemma/morph/spelling appear on hover
			}
			// GL
			var GLTextString = n.nodeValue.trim();
			var GLTextString = graph(GLTextString); // This will make 'æ' show as ̹e etc.
			cells[2].appendChild(classySpanWithLayers(GLTextString, 'notAbbreviated')[2]);
		}
	} 	// End of inner 'for' (<w>'s children)
	return table;
}	// End of function 'wordify'


function punctify(pchar) {
	// This function takes a <pc> HTML element as parameter	
	// and returns an HTML <table> element including three <tr>, each including one <td>. Each <td>
	// refers to one layer (LL, AL and GL) and includes one ore more <span> elements
	
	// Append pc table
	var table = document.createElement('table');                 // Create a word <table> node
	table.setAttribute('class', 'wordTable');				// Set attribute class="word"
	// Append 3 rows with 1 cell each, indexed as 0, 1 and 2
	cellClasses = ['LLCell', 'ALCell', 'GLCell'];
	rows  = [];
	cells = [];
	for (var y = 0; y < 3 ; y++) {	// Create 3 rows: 0=LL; 1=AL; 2=GL
		rows[y] = table.insertRow(y);
		cells[y] = rows[y].insertCell(0);
		cells[y].setAttribute('class', cellClasses[y]);		// Set attribute class (LL, AL or GL)
	}
		
	if (pchar.attributes.getNamedItem('type').nodeValue == 'space') {
		// <pc type="space"> (spaces) outside of <w> 
		// Graphical spaces occurring outside a <w> element
		var myCells = makeTable(document.getElementById('MSText'), 'spaceTable');
		cells[0].appendChild(classySpanWithLayers(space, 'space')[0]);
		cells[1].appendChild(classySpanWithLayers(space, 'space')[1]);
		cells[2].appendChild(classySpanWithLayers(space, 'space')[2]);
	}

	else if (pchar.attributes.getNamedItem('type').nodeValue != 'space') {
		// <pc> for punctuation
	
		// Corresponding modern punctuation (for the LL)
		var modernPunctString = pchar.attributes.getNamedItem('type').nodeValue;
		modernPunctString = modernPunctString.replace('quote', space).replace('question', '?').replace('0', space);
		//modernPunctString = modernPunctString.replace('quote', space).replace('question', '?');
		//modernPunctString = modernPunctString.replace('question', '?');

		// Manuscript punctuation (for AL and GL)
		if (pchar.childNodes[0]) {
			// If <pc> has text content (i.e. there is punctuation in the manuscript here)
			var GLPunctString = graph(pchar.childNodes[0].nodeValue);
			//alert(graph(pchar.childNodes[0].nodeValue));
			var GLPunctClass = 'punct';
		}
		else {
			// If <pc> is a void element (i.e. there is no punctuation in the manuscript here)
			var GLPunctString = space;
			var GLPunctClass = 'space';
		}

		if (pchar.attributes.getNamedItem('type').nodeValue=='0' || pchar.attributes.getNamedItem('type').nodeValue=='quote') {
			// If <pc> is has textual content (i.e. there is punctuation in the manuscript here),
			// but no punctuation should be visualized at the LL or AL. E.g.: <pc type="0">·</pc>
			var ALPunctString = space;
			var ALPunctClass = 'space';
		}
		else {
			// if typen is not "0", i.e. if some punctuation should be visualized at the LL or AL.
			// E.g.: <pc type=",">·</pc>
			var ALPunctClass = 'punct';
		}

		// Append to table cells
		var myCells = makeTable(document.getElementById('MSText'), 'punctTable');
		cells[0].appendChild(classySpanWithLayers(modernPunctString, 'punct')[0]);
		cells[1].appendChild(classySpanWithLayers(modernPunctString, ALPunctClass)[1]);
		//cells[1].appendChild(classySpanWithLayers(GLPunctString, GLPunctClass)[1]); // old
		cells[2].appendChild(classySpanWithLayers(GLPunctString, GLPunctClass)[2]);
	}
	return table;
}


function gapify(gapElement) {
	var gapTextString = '[…]';
	var gapQuantity = gapElement.attributes.getNamedItem('quantity').nodeValue;
	var gapReason = gapElement.attributes.getNamedItem('reason').nodeValue;
	var gapUnit = gapElement.attributes.getNamedItem('unit').nodeValue;
	var gapExplanationString = gapQuantity + ' ' + gapUnit + ' missing (reason: ' + gapReason + ')';
	cells[1].appendChild(classySpanWithLayers(gapTextString, 'gap')[1]); //In the AL cell
	cells[1].setAttribute('title', gapExplanationString); // The 'title' will appear on hover
	cells[2].appendChild(classySpanWithLayers(gapTextString, 'gap')[2]); //In the GL cell
	cells[2].setAttribute('title', gapExplanationString); // The 'title' will appear on hover
}

function tagsetify(tagsetAna) {
	var expandedAna = '';
	for (var i = 0; i < tagsetlist.length; i++) {
		tagCode  = tagsetAna[i];	// Each character in the @ana value. E.g.: in "11B---F3--1" it may be "B"
		category = tagsetlist[i][0] // E.g.: "11 Graphical-Variation"
		for (var k = 0; k < tagsetlist[i][1].length; k++) {
			if ( tagsetlist[i][1][k][0] == tagCode && tagsetlist[i][1][k][0] != "-" ) {
				expandedAna += tagsetlist[i][1][k][1] + ", ";
			}
		}
	}
	//alert('"' + myN + '": ' + '[' + myLemma + '] ' + expandedAna);
	return expandedAna;
}


/*#######################################
#    FUNCTION READING EXTERNAL XML FILE #
#######################################*/

/* The following code reads the external XML file, depending on the browser. */

function loadxml() {
	if (window.XMLHttpRequest) {
	    // Code for modern browsers
	    xmlhttp = new XMLHttpRequest();
	    xmlhttp.open('GET', 'lemmatized_casanatensis.xml', false);
	    xmlhttp.setRequestHeader('Content-Type', 'text/xml');
	    xmlhttp.send('');
	    xmlDoc = xmlhttp.responseXML;
	    readXML();
	 } else {
	    // Code for old IE browsers
	    // var xmlDoc=new ActiveXObject('Microsoft.XMLDOM'); // Old code, from http://www.w3schools.com/xml/loadxmldoc.asp
	    xmlDoc = new ActiveXObject("Microsoft.XMLHTTP"); // New code, from https://www.w3schools.com/xml/xml_http.asp
	    xmlDoc.async=false;
	    xmlDoc.load('lemmatized_casanatensis.xml');
	}
}




/*############################
#    FUNCTION PARSING XML    #
############################*/

function readXML() {

	// The next lines define the trim() function for older browsers (IE 8 and older)
	// that use an older version of JS with no predefined trim() function
	if(typeof(String.prototype.trim) === "undefined") {
		String.prototype.trim = function() {
			return String(this).replace(/^\s+|\s+$/g, '');
		};
	}

	/* // Old code
	// Manage the (one) initial <head> in the file
	var MSHead = xmlDoc.getElementsByTagName('head')[0];
	for (var zy = 0; zy < MSHead.childNodes.length; zy++) { // If <head> includes <w>
		if (MSHead.childNodes[zy].tagName == 'w') {
			var headSpan = document.createElement('span');
			headSpan.setAttribute('class', 'head');
			headSpan.appendChild(wordify(MSHead.childNodes[zy]));
			document.getElementById('MSText').appendChild(headSpan);
			//alert('"'+MSHead.childNodes[zy].textContent+'"')
		}
		if (MSHead.childNodes[zy].tagName=='pc') { // If <head> includes <pc>
			//headSpan.appendChild(punctify(MSHead.childNodes[zy]));
			document.getElementById('MSText').appendChild(punctify(MSHead.childNodes[zy]));
			//alert('"'+MSHead.childNodes[zy].textContent+'"')
		}
	}
	document.getElementById('MSText').appendChild(headSpan);
	*/
			
	// For each <ab>
	var abList = xmlDoc.getElementsByTagName('ab');
	for (var ac = 0; ac < abList.length; ac++) {
		var abDivString = abList[ac].attributes.getNamedItem('n').nodeValue;
		var abDiv = classyElem('div', 'abTitle', abDivString);
		document.getElementById('MSText').appendChild(abDiv);
		var refList = [];
		var abChildren = abList[ac].childNodes;
		for (var acc = 0; acc < abChildren.length; acc++) {
			//abChildren[acc] is a <ref> element that will be passed as argument to
			// the function 'computeWordLikeElements'.
			if (abChildren[acc].tagName == 'ref') {		
				// All <ab>'s children except for the first <head> should be <ref>, but I'm checking anyway
				computeWordLikeElements(abChildren[acc]);
			}
		} // End of 'for each child of <ab>
	} // End of 'for each <ab>'

// The next line makes sure that at the first load of the page, the GL is not visualized (if I did not set checked="checked" in the .html file)
//showMe('GL', document.getElementsByName('cGL'));

}	// End of function readXML()
