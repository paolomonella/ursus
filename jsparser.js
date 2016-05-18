// HTML CLASSES
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
// 	It is a child of <td class="LLCell"> because it is displayed
// 	in the LL row/cell but does not have class="LL", since it does not belong to the medieval text.
// <div class="note outsideWord">: same as above, but the note occurs outside of a <w> element.
// 	It is not a child of <td class="LLCell">, but of the  HTML <div id="MSText">
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
// <span class="unclear certlow"> normally includes one <table class="wordTable"> table
// 	or one such table plus one <table class="spaceTable" and marks that
// 	the word is unclear in the manuscript. @class="certlow" means that the certainty of
// 	my reading of the word is low.
// <span class="unclear certmedium">: same as above, but the certainty is medium.
// <span class="unclear certhigh">:   same as above, but the certainty is high.
// <div class="source start containerDiv"> or
// <div class="source end containerDiv">
// 	mark the div that includes the "show/hide source note" link and the content of the source note
// <a class="source sourceToggleLink">: the "show/hide source" link
// <div class="source start contentDiv"> or
// <div class="source end contentDiv">: the content of the note marking the start or end
// 	of a passage imitating a source
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


// GENERAL VARIABLES
// I'm using an underscore as value for a space until I'll find a way to effectively insert a &nbsp; through JS
var space = '_';
var noteLikeCounter = 0;
var gtos = importTableOfSigns('GToS.csv');
var URNArray = [
	['-', ' - '],
	['urn:cts:latinLit:', ''],
	['stoa0234a.stoa001:', 'Priscian from Caesarea, "Institutio de arte grammatica", '],
	['stoa0110.stoa001:', 'Aelius Donatus, "Ars Minor (De partibus orationis)", '],
	['stoa0110.stoa003:', 'Aelius Donatus, "De Barbarismo", '],
	['stoa0110.stoa004:', 'Aelius Donatus, "De ceteriis vitiis", '],
	['stoa0110.stoa005:', 'Aelius Donatus, "De Metaplasmo", '],
	['stoa0110.stoa006:', 'Aelius Donatus, "De Schematibus", '],
	['stoa0110.stoa007:', 'Aelius Donatus, "De Solecismo", '],
	['stoa0110.stoa008:', 'Aelius Donatus, "De Tropis", '],
	['stoa0233c.stoa001:', 'Pompeius, "Commentum Artis Donati", '],
	['stoa0259.stoa001:', 'Servius, "Commentarius in Artem Donati", '],
	['stoa0258a.stoa001:', 'Sergius, "Explanationem in Artem Donati", '],
];

// MY OWN FUNCTIONS


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
	// 		(as of 06.01.2015, I'm not using element 2)
	var xmlhttp;
	xmlhttp=new XMLHttpRequest();
	xmlhttp.open('GET', csvFile, false);
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
		}
	return ToS;
}

function graph(myString) {
	// This function inputs a string of characters representing graphemes
	// in the XML/TEI source file and returns a string of characters that will be used to
	// display the graphemes in the browser
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
		if (gtos[ialph][0] != '' && gtos[ialph][1] != '') {
			myString = myString.replace(gtos[ialph][0], gtos[ialph][1]);
		}
	}
	return myString;
}

function URNToCitation (URNToParse) {
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
	// This wraps some text in an element a specific HTML @class attribute
	// and returns one value, being a HTML element.
	// For example, if elementName='span' and classForElement='lb', it returns:
	// 	<span class="lb">textToWrap</span>
	outputElement = document.createElement(elementName);		// Create the <span> element
	outputElement.setAttribute('class', classForElement);		// Set attribute
	classyText  = document.createTextNode(textToWrap.trim());	// The text node
	outputElement.appendChild(classyText);				// Append the text inside the span
	return outputElement;
}

function classySpanWithLayers(textToWrap, classForSpan) {
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
		var e = refElement.childNodes[j]; // 'e' includes an alement such as <w>, <lb>, <pc> etc.
		
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
			// 	is needed to make the line number appear underneath. Since this space must
			// 	look invisible (white font color on white background), I'm using 
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
			if (e.tagName == 'pb') {
				var pbCbTextString = '[Start of folio '+pbCbN+']';
				var divPbCb  = classyElem('div', e.tagName, '');
				// Check if the folio number has one digit only
				var patt = /^\d\D/g;	// 2 digit chars followed by a non-digit char. E.g.: '12r'
				if (patt.test(pbCbN)) {		// Like '2r'
					pbCbN = '0' + pbCbN
				}
				// Create link to image file
				var imgURL = 'manuscript_images/C_' + pbCbN + '.JPG';
				var divPbCbA = document.createElement('a');
				divPbCbA.setAttribute('href', imgURL);
				var divPbCbAText = document.createTextNode(pbCbTextString);
				divPbCbA.appendChild(divPbCbAText);
				divPbCb.appendChild(divPbCbA);
				document.getElementById('MSText').appendChild(divPbCb);
			}
			else if (e.tagName == 'cb') {
				var pbCbTextString = '[Start of column ' + pbCbN.split('.')[1];
				pbCbTextString += ' of folio ' + pbCbN.split('.')[0] + ']';
				document.getElementById('MSText').appendChild(
						classyElem('div', e.tagName, pbCbTextString)
						);
			}
		}

		else if (e.tagName == 'pc' && e.attributes.getNamedItem('n').nodeValue == 'space') {
			// <pc n="space"> (spaces) outside of <w>
			// Graphical spaces occurring outside a <w> element
			var myCells = makeTable(document.getElementById('MSText'), 'spaceTable');
			myCells[0].appendChild(classySpanWithLayers(space, 'space')[0]);
			myCells[1].appendChild(classySpanWithLayers(space, 'space')[1]);
			myCells[2].appendChild(classySpanWithLayers(space, 'space')[2]);
		}

		else if (e.tagName == 'pc' && e.attributes.getNamedItem('n').nodeValue != 'space') {
			// <pc> including punctuation
			
			// Corresponding modern punctuation (for the LL)
			var modernPunctString = e.attributes.getNamedItem('n').nodeValue;
			modernPunctString = modernPunctString.replace('quote', '"').replace('question', '?');
			modernPunctString = modernPunctString.replace('0', '');

			// Manuscript punctuation (for AL and GL)
			if (e.childNodes[0]) {
				var GLPunctString = graph(e.childNodes[0].nodeValue);
				var GLPunctClass = 'punct';
			}
			// If <pc> is a void element (i.e. there is no punctuation in the manuscript here:
			else {
				var GLPunctString = space;
				var GLPunctClass = 'space';
			}

			// Append to table cells
			var myCells = makeTable(document.getElementById('MSText'), 'punctTable');
			myCells[0].appendChild(classySpanWithLayers(modernPunctString, 'punct')[0]);
			myCells[1].appendChild(classySpanWithLayers(GLPunctString, GLPunctClass)[1]);
			myCells[2].appendChild(classySpanWithLayers(GLPunctString, GLPunctClass)[2]);
		}

		else if (e.tagName == 'gap') {
			// <gap> outside of <w>
			var myCells = makeTable(document.getElementById('MSText'), 'gapTable');
			var gapTextString = '[…]';
			myCells[0].appendChild(classySpanWithLayers(gapTextString, 'gap')[1]); //In the AL cell
			myCells[1].appendChild(classySpanWithLayers(gapTextString, 'gap')[1]); //In the AL cell
			myCells[2].appendChild(classySpanWithLayers(gapTextString, 'gap')[2]); //In the GL cell

		}
		
		else if (e.tagName == 'unclear') {
			// <unclear> outside of <w>
			// <unclear> always has one child only, and that child can be <w> or <pc>
			unclearSpan = document.createElement('span');		// Create the <span> element

			// If XML/TEI has <unclear cert="medium">, the HTML DOM will have
			// <span class="unclear certmedium">
			var cert = e.attributes.getNamedItem('cert').nodeValue;
			unclearSpan.setAttribute('class', 'unclear cert'+cert);	// Set attribute

			for (var zy = 0; zy < e.childNodes.length; zy++) {
				if (e.childNodes[zy].tagName == 'w') {
					// e is <unclear>
					// e.childNodes[zy]) is the <w> child of <unclear>
					// The next line transforms the XML/TEI <w> into
					// an HTML <table> and appends the table
					// to the <span class="unclear> HTML element.
					unclearSpan.appendChild(wordify(e.childNodes[zy]));
				}
				if (e.childNodes[zy].tagName=='pc' &&
						e.childNodes[zy].attributes.getNamedItem('n')
						.nodeValue=='space') {
					// Graphical space occurring inside a XML/TEI <unclear> element
					// In this case, the <table class="spaceTable"> will be appended
					// to unclearSpan, that is <span class="unclear">:
					var myCells = makeTable(unclearSpan, 'spaceTable');
					myCells[0].appendChild(classySpanWithLayers(space, 'space')[0]);
					myCells[1].appendChild(classySpanWithLayers(space, 'space')[1]);
					myCells[2].appendChild(classySpanWithLayers(space, 'space')[2]);
				}
			document.getElementById('MSText').appendChild(unclearSpan);
			}
		} // End of 'unclear'

		else if (e.tagName == 'note') {
			// <note> outside of <w>
			expandableDiv(
					document.getElementById('MSText'),
					'note outsideWord',
					'note noteToggleLink',
					'Note to section',
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
	// This function iterates all words in the xml file. It takes a <w> HTML element as parameter
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

	// Extract the LL
	var LLText = document.createTextNode(word.attributes.getNamedItem('n').nodeValue);
	var LLSpan = document.createElement('span');    // Create a <span> node. The hierarchy in the DOM
		// will be: <table class="wordTable"><tr><td class="LLCell"><span class="LL word">
	LLSpan.setAttribute('class', 'LL word');        // Set attribute class
	LLSpan.appendChild(LLText);             	// Append the text inside the LL span
	cells[0].appendChild(LLSpan);                   // Append the span inside the <td class="LLCell">

	//Iterate all children of <w>
	for (var x = 0; x < word.childNodes.length; x++) {
		var n = word.childNodes[x];

		//if (n.tagName == 'hi' && n.attributes.getNamedItem('rend').nodeValue == 'larger') {
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
			// GL of larger grapheme (span).
				// The result will be <span class="GL larger"
				//                or  <span class="GL dropcap":
			cells[2].appendChild(classySpanWithLayers(hiText, hiRendAttrValue)[2]);
				// Value "GL" comes from function classySpanWithLayers()
				// classySpanWithLayers(...)[2] includes class="GL"
		}

		else if (n.tagName == 'gap') {
			// <gap> within <w>
			// GL
			var gapTextString = '[…]';
			cells[1].appendChild(classySpanWithLayers(gapTextString, 'gap')[1]); //In the AL cell
			cells[2].appendChild(classySpanWithLayers(gapTextString, 'gap')[2]); //In the GL cell
		}

		else if (n.tagName == 'note') {
			// <note> inside <w>
			expandableDiv(
					cells[0],
					'note withinword',
					'note noteToggleLink',
					'Note to word',
					n.childNodes[0].nodeValue.trim()
					);
		}

		else if (n.tagName == 'lb') {
			// <lb> inside <w>
			var lbTextString = '['+n.attributes.getNamedItem('n').nodeValue+']';
			//Append lb span inside the <td>
			cells[2].appendChild(classyElem('span', 'lb lbWithinWord', lbTextString));
		}
	
		else if (n.tagName == 'pc' && n.attributes.getNamedItem('n').nodeValue == 'space') {
			// <pc n="space"> (spaces) within <w>
			// 	Yes, sometimes there is a (graphical) space within a (linguistic) word.
			// 	This means that the scribe considers it to be two words, while contemporary
			// 	conventions consider it one word. Example:
			// 	Contemporary convention: unicuique
			// 	Scribe's     convention: uni cuique
			cells[1].appendChild(classySpanWithLayers(space, 'space')[1]); // Put it in the AL cell
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
						// The content of CLBaseGraphemesContent is a
						// <span class="GL larger"> element
						var GLBaseGraphemesContent =
							classySpanWithLayers(hiText, 'larger')[2];
					}
					else {
						GLBaseGraphemes = ''
						GLBaseGraphemes = abbr.childNodes[z].nodeValue.trim();	

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
					var GLAbbrMark = abbr.childNodes[z].childNodes[0].nodeValue.trim();
					//Create text node
 					var GLAbbrMarkText  = document.createTextNode(GLAbbrMark); 
					var GLAbbrMarkSpan = document.createElement('span');
					// The values of @class for the Abbr. Mark <span> in HTML
					// are "GL am" and the value of @type in XML/TEI,
					// so "GL am superscription", "GL am after", "GL am brevigraph"
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
			cells[1].appendChild(classySpanWithLayers(ALTextString, 'abbrExpansion')[1]);
		}	// End of 'choice', i.e. of the processing of abbreviations

		else if (n.tagName != 'choice') {
			// Graphemes outside abbreviations
			// AL
			var ALTextString = n.nodeValue.trim();
			ALTextString = alph(ALTextString); //Compute the AL based on the graphemes and the GToS
			cells[1].appendChild(classySpanWithLayers(ALTextString, 'notAbbreviated')[1]);
			// GL
			var GLTextString = n.nodeValue.trim();
			cells[2].appendChild(classySpanWithLayers(GLTextString, 'notAbbreviated')[2]);
		}
	} 	// End of inner 'for' (<w>'s children)
	return table;
}	// End of function 'wordify'







// FUNCTIONS PARSING XML

var xmlDoc;
function loadxml() {
  xmlDoc = document.implementation.createDocument('','',null);
  xmlDoc.load('casanatensis.xml');
  xmlDoc.onload = readXML;
}

function readXML() {

	// The next lines define the trim() function for older browsers (IE 8 and older)
	// that use an older version of JS with no predefined trim() function
	if(typeof(String.prototype.trim) === "undefined") {
		String.prototype.trim = function() {
			return String(this).replace(/^\s+|\s+$/g, '');
		};
	}

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
				// All <ab>'s children should be <ref>, but I'm checking anyway
				computeWordLikeElements(abChildren[acc]);
			}
		}
	}	// End of 'for each <ab>'
	
}	// End of function readXML()



/*##############################
# TAGSET INTERPRETATION TABLE #
#############################*/

// This 'explanation' of the PoS tags is based on
// /home/ilbuonme/ursus/lemma/tree_tagger_and_related_files/parameter_files/from_treetagger_website/index_thomisticus/Tagset_IT.pdf

var tagsetlist = [
        //1 Flexional-Type
        [
            [ ['1'], ['Nominal'] ],
            [ ['2'], ['Participial'] ],
            [ ['3'], ['Verbal'] ],
            [ ['4'], ['Invariable'] ],
            [ ['5'], ['Pseudo-lemma'] ]
            ],
        //2 Nominals-Degree
        [
            [ ['1'], ['Positive'] ],
            [ ['2'], ['Comparative'] ],
            [ ['3'], ['Superlative'] ],
            [ ['4'], ['Not stable composition'] ],
            [ ['-'], ['None'] ]
            ],
        //3 Flexional-Category
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
            ],
        //4 Mood
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
            ],
        //5 Tense
        [
            [ ['1'], ['Present'] ],
            [ ['2'], ['Imperfect'] ],
            [ ['3'], ['Future'] ],
            [ ['4'], ['Perfect'] ],
            [ ['5'], ['Plusperfect'] ],
            [ ['6'], ['Future perfect'] ],
            [ ['-'], ['None'] ]
            ],
        //6 Participials-Degree
        [
            [ ['1'], ['Positive'] ],
            [ ['2'], ['Comparative'] ],
            [ ['3'], ['Superlative'] ],
            [ ['-'], ['None'] ]
            ],
        //7 Case/Number
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
            ],
        //8 Gender/Number/Person
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
            ],
        //9 Composition
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
            ],
        //10 Formal-Variation
        [
            [ ['A'], ['I variation of wordform'] ],
            [ ['B'], ['II variation of wordform'] ],
            [ ['C'], ['III variation of wordform'] ],
            [ ['X'], ['Author mistake, or bad reading?'] ],
            [ ['-'], ['None'] ]
            ],
	//11 Graphical-Variation
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

