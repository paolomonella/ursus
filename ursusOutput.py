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
import xml.etree.ElementTree as ET


###################
# My own markdown #
###################

# Clear screen
os.system('clear')

#################
# Insert xml:id #
#################

# The namespaces
n    = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
nx   = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

# Parse the tree
tree = ET.parse('casanatensis.xml')

for word in tree.findall('.//' + n + 'w'):
    if word.get(nx + 'id'):
        idstring = word.get(nx + 'id')
        idcount  = int(idstring[1:])
        # § vd. se copiare tutta questa funzione così com'è, dato che funziona.
    else:
        idcount  = idcount + 3
        idstring = 'w' + str(idcount)
        word.set(nx + 'id', 'w' + str(idcount))

# Quando risolvo il problema, devo de-commentare la riga seguente:
tree.write('output.xml', encoding="UTF-8", method="xml")

############################################
# Check that all IDs are sequential so far #
############################################

# ... and if there are words without an ID still

# Parse the tree
tree = ET.parse('output.xml')

idcount = 0
for word in tree.findall('.//' + n + 'w'):
    if word.get(nx + 'id'):
        idstring = word.get(nx + 'id')
        old_idcount  = idcount
        idcount  = int(idstring[1:])
        if idcount > old_idcount:
            #print(str(idcount) + ' > ' + str(old_idcount))
            pass
        else:
            print('Nuovo counter: ' + str(idcount) + '. Counter precedente: ' + str(old_idcount))



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

#zipArchiveFile(inBaseFN, outBaseFN, c, t)
