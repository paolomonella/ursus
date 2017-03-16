#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script turns my own 'ursusmarkdown' conventions into XML/TEI for the digital edition
# of manuscript Casanatensis 1086.
# It's written in Python 3.4, but also works with Python 2.7
#
# Warning: when writing in 'ursusmarkdown', note that every string at the beginning
# of the line that does not start with '<' or end with '>'
# will be substituted by this script with
# <w n="string">string</w>
# So, if this is not intended, every alphanumerical string that must not be substituted
# should start with whitespace, such as tab or space(s)

from __future__ import print_function
import datetime
import shutil
import zipfile
import os
import re
import xml.etree.ElementTree as ET


###################
# My own markdown #
###################

# Clear screen
os.system('clear')

# Set working files and folders

# Input
c       = '/home/ilbuonme/siti/paolo.monella/ursus/' # working directory for input file
inBaseFN='casanatensis.xml'    # input base file name
inFP    = c+inBaseFN    # input file path (folder + base file name)

# Output 
outBaseFN   = 'temp_'+inBaseFN      # Output Base File name
outFP       = c+outBaseFN           # (temporary) Output Filename Path (folder + base file name).

# Archive
t       = '/home/ilbuonme/voluminosi/ursus/old_versions_of_xml_source_file/' # directory where old versions are archived


outFH=open(outFP,'w')   # File Handler for the output file 

# These lists will include the lines not substituted because starting or
# ending with whitespace
startWList  = []    # not substituted because starting with whitespace
endWList    = []    # not substituted because ending   with whitespace
startEndWList = []  # not substituted because starting end ending with whitespace
nofitList   = []    # not substituted because not fitting my regexes

# Define patterns for my own 'markdown' conventions
abPatt  =   "(.*),(.*),(.*),(.*),(.*)" # Single abbreviation
dAbPatt  =   "(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)" # Double abbreviation
stPatt  =   "<.*" # Lines that [s]tart with a [t]ag
etPatt  =   ".*>" # Lines that [e]nd   with a [t]ag
#utPatt  =   ".*>_" # Lines that [e]nd   with a [t]ag and a final underscore (old version: no longer in use)
#wPatt   =   "[\wþŋ¢÷].*" # Regular word (no abbreviations), possibly starting with non-ASCII brevigraph/logograph
wPatt   =   "\w.*" # Regular word (no abbreviations)
sewPatt  =   "\s+\w*\s+" # It starts and ends with whitespace, and has chars in between
swPatt  =   "\s+\w*"    # The line starts with whitespace, then has characters
ewPatt  =   "\w*\s+"    # The line   ends with whitespace, and has chars before

# Different spellings between medieval and contemporary Latin
sd =    {
        'ae':'e',
        'oe':'e',
        }

def reSpell(stringToParse, spellingDict):
    for s in spellingDict:
        stringToParse = stringToParse.replace(s, spellingDict[s])
    return stringToParse

# Perform substitutions 
with open(inFP) as inFH:
    for line in inFH:
        # Clear variables
        nL = ''     # Clear the nL (newLine) variable
        #wSpace= '_' # Old version
        wSpace= '\n\t<pc n="space"> </pc>' # Reset the wSpace variable; maybe this was not necessary

        # Check if word has a space after it in the MSS
        if line[-2:-1] == "0":   # Words that don't have a space after them
            wSpace = ''
            line = line[:-2]  # Remove the final '0'
        else:
            wSpace= '\n\t<pc n="space"> </pc>'  # Words that have a space
            #wSpace = '_'    # Old version

        # Perform changes
        #if re.match(stPatt, line) or re.match(etPatt, line) or re.match(utPatt, line): # Old version
        if re.match(stPatt, line) or re.match(etPatt, line): # Starts or ends with XML tags
            if (line[-1]) != '>':   # This if/else is necessary b/c otherwise it will crop the final '>' in the last 
                                    # line, that normally is </TEI>
                nL = line[:-1]
            else:
                nL = line
            print(nL, file=outFH)
        elif re.match(dAbPatt, line): # Double abbreviations
            line = line.replace('v', 'u')   # This substitution must be applied to all layers (GL, AL, LL)
            line = line.replace('-', '¯')   # This allows me to insert ,st,-,sunt, (easier) instead of ,st,¯,sunt,
            #print('trovato doppio in:\t'+line)
            dAbM = re.match(dAbPatt, line)
            print(dAbM.group(4))
            abPre = dAbM.group(1)
            abBase1 = dAbM.group(2)
            abAm1 = dAbM.group(3)
            if abAm1 == '':
                abType1 = 'brevigraph'
                abAmTag1 = ''
            elif abAm1 == ';':
                abType1 = 'after'
                abAmTag1 = '<am>'+abAm1+'</am>'
            else:
                abType1 = 'superscription'
                abAmTag1 = '<am>'+abAm1+'</am>'
            abAlph1 = dAbM.group(4)
            abMiddle = dAbM.group(5)
            abBase2 = dAbM.group(6)
            abAm2 = dAbM.group(7)
            if abAm2 == '':
                abType2 = 'brevigraph'
                abAmTag2 = ''
            elif abAm2 == ';':
                abType2 = 'after'
                abAmTag2 = '<am>'+abAm2+'</am>'
            else:
                abType2 = 'superscription'
                abAmTag2 = '<am>'+abAm2+'</am>'
            abAlph2 = dAbM.group(8)
            abPost = dAbM.group(9)
            #abWordLL = abPre+abAlph1+abMiddle+abAlph2+abPost # (L)inguistic (L)ayer, old version
            #abWordLL = (abPre+abAlph1+abMiddle+abAlph2+abPost).replace('æ', 'ae') # (L)inguistic (L)ayer, old version
            abWordLL = abPre+abAlph1+abMiddle+abAlph2+abPost # (L)inguistic (L)ayer
            abWordLL = abWordLL.replace('æ', 'ae')          # E caudatum (medieval romæ → contemporary rome)
            #abWordLL = abWordLL.replace('þ', 'per').replace('ŋ', 'pro').replace('¢', 'qui') # Brevigraphs
            #abWordLL = abWordLL.replace('÷', 'est')         # Logographs
            nL='<w n="'+abWordLL+'">'+reSpell(abPre, sd)+'\n\t<choice>\n'
            nL=nL+'\t\t<abbr type="'+abType1+'">'+reSpell(abBase1, sd)+abAmTag1+'</abbr>\n'
            nL=nL+'\t\t<expan>'+reSpell(abAlph1, sd)+'</expan>\n\t</choice>\n\t'+reSpell(abMiddle, sd)+'\n\t<choice>\n'
            nL=nL+'\t\t<abbr type="'+abType2+'">'+reSpell(abBase2, sd)+abAmTag2+'</abbr>\n'
            nL=nL+'\t\t<expan>'+reSpell(abAlph2, sd)+'</expan>\n\t</choice>\n'+reSpell(abPost, sd)+'</w>'+wSpace
            print(nL, file=outFH)
        elif re.match(abPatt, line): # Single abbreviations
            line = line.replace('v', 'u')   # This substitution must be applied to all layers (GL, AL, LL)
            line = line.replace('-', '¯')   # This allows me to insert ,st,-,sunt, (easier) instead of ,st,¯,sunt,
            abM = re.match(abPatt, line)
            abPre = abM.group(1)
            abBase = abM.group(2)
            abAm = abM.group(3)
            if abAm == '':
                abType = 'brevigraph'
                abAmTag = ''
            elif abAm == ';':
                abType = 'after'
                abAmTag = '<am>'+abAm+'</am>'
            else:
                abType = 'superscription'
                abAmTag = '<am>'+abAm+'</am>'
            abAlph = abM.group(4)
            abPost = abM.group(5)
            #nL='<w n="'+abPre+abAlph+abPost+'">'+reSpell(abPre, sd)+'\n\t<choice>\n' old version
            abWordLL = abPre+abAlph+abPost # abbreviated word at Linguistic Layer
            abWordLL = abWordLL.replace('æ', 'ae')          # E caudatum (medieval romæ → contemporary rome)
            #abWordLL = abWordLL.replace('þ', 'per').replace('ŋ', 'pro').replace('¢', 'qui') # Brevigraphs
            #abWordLL = abWordLL.replace('÷', 'est')         # Logographs
            nL='<w n="'+abWordLL+'">'+reSpell(abPre, sd)+'\n\t<choice>\n'
            nL=nL+'\t\t<abbr type="'+abType+'">'+reSpell(abBase, sd)+abAmTag+'</abbr>\n'
            nL=nL+'\t\t<expan>'+reSpell(abAlph, sd)+'</expan>\n\t</choice>\n'+reSpell(abPost, sd)+'</w>'+wSpace
            print(nL, file=outFH)
        elif line == '\n':  # Empty line
            nL = line[:-1]
            print(nL, file=outFH)
        elif re.match(sewPatt, line[:-1]):    # Starts and ends with whitespace
            print('This line starts and ends with whitespace!')
            nL = line[:-1]
            startEndWList.append(nL)
            print(nL, file=outFH)
        elif re.match(swPatt, line[:-2]):    # Starts with whitespace
            nL = line[:-1]
            startWList.append(nL)
            print(nL, file=outFH)
        elif re.match(ewPatt, line[:-1]):    # Ends with whitespace
            nL = line[:-1]
            endWList.append(nL)
            print(nL, file=outFH)
        elif re.match(wPatt, line):     # Regular words (no abbreviations)
            line = line.replace('v', 'u')   # This substitution must be applied to all layers (GL, AL, LL)
            wM = re.match(wPatt, line)
            wWordGL = wWordLL = wM.group(0)  # (L)inguistic (L)ayer vs. (G)raphematic (L)ayer
            wWordGL = reSpell(wWordGL, sd)   # contemporary romae → medieval rome (et sim.)
            wWordLL = wWordLL.replace('æ', 'ae') # E caudatum (medieval romæ → contemporary rome)
            #wWordLL = wWordLL.replace('þ', 'per').replace('ŋ', 'pro').replace('¢', 'qui') # Brevigraphs
            #wWordLL = wWordLL.replace('÷', 'est')         # Logographs
            nL='<w n="'+wWordLL+'">'+wWordGL+'</w>'+wSpace
            print(nL, file=outFH)
        else:                           # Doesn't fit any regex
            nL = line[:-1]
            nofitList.append(nL)
            print(nL, file=outFH)

# Close file handers
outFH.close()
#nac.close()
inFH.close()

def outputListAsTable(disclaimer, listName):
    if len(listName) > 0:
        print(disclaimer)
        for x in listName:
            print('\t«'+x+'»')
        print() # This just inserts a blank line

# Output the lines that have not been substituted
outputListAsTable('Lines not substituted because they start with whitespace:', startWList)
outputListAsTable('ಠ_ಠ Lines not substituted because they start and end with whitespace:', startEndWList)
outputListAsTable('ಠ_ಠ Lines not substituted because they end with whitespace:', endWList)
outputListAsTable('ಠ_ಠ Lines not substituted because they do not fit any regex:', nofitList)

if len(startEndWList) == 0 and len(endWList) == 0 and len(nofitList) == 0:
    print('  ͡° ͜ʖ ͡°  No parsing errors')

#################
# Insert xml:id #
#################

# The namespaces
n    = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
nx   = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

# Parse the tree
tree = ET.parse(outFP)  # It works on the temp output file and adds it xml:ids

# The following code block makes a list of existing IDs so it checks that new IDs do not
# already exist in the file (to avoid duplicate IDs)
existing_w_ids = []
for word in tree.findall('.//' + n + 'w'):
    if word.get(nx + 'id'):
        existing_w_ids.append(word.get(nx + 'id'))

# The following variables will be useful later to check that there are no unordered IDs
last_existing_id = existing_w_ids[-1]
reached_last_id  = False

# If a word has no xml:id, set one
for word in tree.findall('.//' + n + 'w'):
    if word.get(nx + 'id'):
        idstring = word.get(nx + 'id')
        idcount  = int(idstring[1:])
        if idstring == last_existing_id:
            reached_last_id = True
    else:
        idcount  = idcount + 3
        idstring = 'w' + str(idcount)
        if idstring in existing_w_ids:  # If it's a duplicate ID, warn me and let me manage it
            idstring = idstring + '_duplicate'
            print('\nWARNING: DUPLICATE ID "' + idstring + '"')
        if not reached_last_id and idcount > int(last_existing_id[1:]):
            idstring = idstring + '_unordered'
            print('\nWARNING: UNORDERED ID "' + idstring + '"')
        #print(idstring + '_' + word.get('n'), end=' ')
        word.set(nx + 'id', idstring)
        existing_w_ids.append(idstring)

# Quando risolvo il problema, devo de-commentare la riga seguente:
tree.write(outFP, encoding="UTF-8", method="xml")

############################
# Zip and archive old file #
############################


def zipArchiveFile(inputFileName, outputFileName, workingFolder, archiveFolder):
    """ This function zips and archives the old input file.
        Then, it gives the output file the same name of the old input file.
        Arguments:
            inputFileName   = base file name (not complete path) of old input file, including extension
            outputFileName  = base file name (not complete path) of new output file, including extension
            workingFolder   = the folder where both the input file and the outpu file are
            archiveFolder   = the folder where the old input file will be archived
    """
    # Zip and store the old input file
    #dateTag = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S") # A string with current date and time
    # In next line, 'datetime...' generates a string with current date and time
    stored = archiveFolder + datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S") +'_'+inputFileName
    shutil.move(workingFolder+inputFileName, stored)
    zf = zipfile.ZipFile(stored+'.zip', mode='w')
    zf.write(stored, compress_type=zipfile.ZIP_DEFLATED)
    zf.close()
    os.remove(stored)
    # Give the output file the same filename as the original input file
    shutil.move(workingFolder+outputFileName,workingFolder+inputFileName)

zipArchiveFile(inBaseFN, outBaseFN, c, t)
