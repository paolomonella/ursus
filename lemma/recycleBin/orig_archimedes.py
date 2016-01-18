#!/usr/bin/python
import xmlrpclib
server = xmlrpclib.ServerProxy("http://archimedes.mpiwg-berlin.mpg.de:8098/RPC2")
lang = "-LA"
wordlist  = ["est","fido","dog"]

print "lemma.help: get uri of documentation\n"
try:
    print server.lemma.help()
except xmlrpclib.Error, v:
    print "ERROR", v
print "\n---------\nlemma.supported: get list of supported langs\n"
try:
    print server.lemma.supported()
except xmlrpclib.Error, v:
    print "ERROR", v

print "\n=================================\n lemma method. parameters: (\"-LA\",[\"est\",\"fido\",\"dog\"]) NOTE:\"dog\" is not a latin word \n"
print "\n---------\nlemma: list without grammatical info: Note--only words for which hits ARE found are returned!\n"


try:
    print server.lemma(lang,wordlist)
except xmlrpclib.Error, v:
    print "ERROR", v
print "\n---------\nlemma: list with grammatical info\n"
try:
    print server.lemma(lang,wordlist,"full")
except xmlrpclib.Error, v:
    print "ERROR", v