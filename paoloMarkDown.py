#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script turns my own 'paolomarkdown' conventions into XML/TEI for the digital edition
# of manuscript Casanatensis 1086.
# It's written in Python 3.4, but also works with Python 2.7
#
# Warning: when writing in 'paolomarkdown', note that every string at the beginning
# of the line that does not start with '<' or end with '>'
# will be substituted by this script with
# <w ana="string">string</w>
# So, if this is not intended, every alphanumerical string that must not be substituted
# should start with whitespace, such as tab or space(s)

from __future__ import print_function
import datetime
import shutil
import zipfile
import os
import re


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
outBaseFN   = 'temp_'+inBaseFN   # output base file name
outFP       = c+'temp_'+inBaseFN  # output file name path (folder + base file name)

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
wPatt   =   "\w.*" # Regular word (no abbreviations)
sewPatt  =   "\s+\w*\s+" # It starts and ends with whitespace, and has chars in between
swPatt  =   "\s+\w*"    # The line starts with whitespace, then has characters §
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
        wSpace= '\n\t<pc ana="space"> </pc>' # Reset the wSpace variable; maybe this was not necessary

        # Check if word has a space after it in the MSS
        if line[-2:-1] == "0":   # Words that don't have a space after them
            wSpace = ''
            line = line[:-2]  # Remove the final '0'
        else:
            wSpace= '\n\t<pc ana="space"> </pc>'  # Words that have a space
            #wSpace = '_'    # Old version

        # Perform changes
        #if re.match(stPatt, line) or re.match(etPatt, line) or re.match(utPatt, line): # Old version
        if re.match(stPatt, line) or re.match(etPatt, line): # Starts or ends with XML tags
            nL = line[:-1]
            print(nL, file=outFH)
        elif re.match(dAbPatt, line): # Double abbreviations
            line = line.replace('v', 'u')   # This substitution must be applied to all layers (GL, AL, LL)
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
            abWordLL = (abPre+abAlph1+abMiddle+abAlph2+abPost).replace('æ', 'ae') # (L)inguistic (L)ayer §
            nL='<w ana="'+abWordLL+'">'+reSpell(abPre, sd)+'\n\t<choice>\n'
            nL=nL+'\t\t<abbr type="'+abType1+'">'+reSpell(abBase1, sd)+abAmTag1+'</abbr>\n'
            nL=nL+'\t\t<expan>'+reSpell(abAlph1, sd)+'</expan>\n\t</choice>\n\t'+reSpell(abMiddle, sd)+'\n\t<choice>\n'
            nL=nL+'\t\t<abbr type="'+abType2+'">'+reSpell(abBase2, sd)+abAmTag2+'</abbr>\n'
            nL=nL+'\t\t<expan>'+reSpell(abAlph2, sd)+'</expan>\n\t</choice>\n'+reSpell(abPost, sd)+'</w>'+wSpace
            print(nL, file=outFH)
        elif re.match(abPatt, line): # Single abbreviations
            line = line.replace('v', 'u')   # This substitution must be applied to all layers (GL, AL, LL)
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
            #nL='<w ana="'+abPre+abAlph+abPost+'">'+reSpell(abPre, sd)+'\n\t<choice>\n' old version
            abWordLL = abPre+abAlph+abPost # abbreviated word at Linguistic Layer
            nL='<w ana="'+abWordLL.replace('æ', 'ae')+'">'+reSpell(abPre, sd)+'\n\t<choice>\n'
            nL=nL+'\t\t<abbr type="'+abType+'">'+reSpell(abBase, sd)+abAmTag+'</abbr>\n'
            nL=nL+'\t\t<expan>'+reSpell(abAlph, sd)+'</expan>\n\t</choice>\n'+reSpell(abPost, sd)+'</w>'+wSpace
            print(nL, file=outFH)
        elif line == '\n':  # Empty line
            nL = line[:-1]
            print(nL, file=outFH)
        elif re.match(sewPatt, line[:-1]):    # Starts and ends with whitespace
            print('start and end!')
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
            wWordLL = wWordLL.replace('æ', 'ae') # medieval romæ → contemporary rome §
            nL='<w ana="'+wWordLL+'">'+wWordGL+'</w>'+wSpace
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
        count = 0
        for x in listName:
            if count < 3:
                myEnd = '\t\t\t'
            else:
                myEnd = '\n'
                count = 0
            print('«'+x+'»', end=myEnd)
            count = count + 1
        print()


#print(startWList)
#print(endWList)
#print(startEndWList)
#print(nofitList)

# Output the lines that have not been substituted
outputListAsTable('Lines not substituted because they start and end with whitespace:', startEndWList)
outputListAsTable('Lines not substituted because they start with whitespace:', startWList)
outputListAsTable('Lines not substituted because they end with whitespace:', endWList)
outputListAsTable('Lines not substituted because they do not fit any regex:', nofitList)


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
