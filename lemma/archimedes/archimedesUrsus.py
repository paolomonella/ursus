#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To-do:
# - correct the 'except'
# - add 'if': only if w doesn't already have a @lemma and (and? or?) a @morph, do parsing
# - eventually, remove the 'mod' moderator
# - find correct attributes for @lemma and @morph
# - find out why it doesn't parse obvious words (such as 'ex')
# - possibly add 'clear' after each inflected form
# - report to DC list/wiki



# Import modules

from xml.dom.minidom import parse, parseString
import xmlrpclib
import codecs

# Set parameters for xmlrpclib

server = xmlrpclib.ServerProxy("http://archimedes.mpiwg-berlin.mpg.de:8098/RPC2")
lang = "-LA"

# Parse XML

xmldoc = parse('../../casanatensis.xml')
#xmldoc = parse('/home/ilbuonme/siti/paolo.monella/ursus/shorter_casanatensis.xml')
wordElementList = xmldoc.getElementsByTagName('w')


mod = 0
for w in wordElementList:
        # This 'mod' limits the number of words to be parsed
        if mod < 5:
            form = w.attributes['ana'].value
            # Parse the inflected word
            try:
                    results = server.lemma(lang, form, "full")
                    print('\n\n---\n\nForm: ' + form + '\n')
                    for fr in results:
                        lemmaOptions = results[fr]
                        count = 0
                        # Show the user all possible lemmas and morphological analysis
                        #print('\nPossible lemmas: ' + ', '.join(lemmaOptions))
                        for lemma in lemmaOptions:
                            morphAnaOptions  = lemmaOptions[lemma]
                            print('\tLemma: ' + lemma)
                            for i, m in enumerate(morphAnaOptions):
                                pass
                                count = count + 1
                                print('\t\t' + str(count) + ' ' + m)
                                morphAnaOptions[i] = {count: morphAnaOptions[i]}
                        # Prompt user for the right lemma/morphological analysis
                        answer = int(raw_input("Choose the number of the right lemma/morphological analysis: "))
                        # Retrieve the correct lemma/morphological analysis based on the user's answer
                        for lemma in lemmaOptions:
                            morphAnaOptions  = lemmaOptions[lemma]
                            for m in morphAnaOptions:
                                if m.keys()[0] == answer:
                                    correctMorph = m[m.keys()[0]]
                                    w.setAttribute('n', form)
                                    w.setAttribute('lemma', lemma)
                                    w.setAttribute('ana', correctMorph)
            except (xmlrpclib.Error, v):
                    print("ERROR", v)
            mod = mod + 1

                                     
f = open('output.xml', 'w')
#xmldoc.content.strip(codecs.BOM_UTF8)
#xmldoc.writexml(f).encode('utf-8').decode('utf-8')
f = codecs.lookup("utf-8")[3](f)
xmldoc.writexml(f, encoding="utf-8")
f.close()





"""
def cheeseshop(kind, *arguments, **keywords):
	print "Avete",kind,"?"
	print "Spiacente, niente",kind
	chiavi=keywords.keys()
	print "Le chiavi sono:",chiavi
	for k in keywords: print k,"ha come valore",keywords[k]
	print "In particolare, il contenuto di primo è",keywords['primo']
	print "Invece gli argomenti aggiuntivi sono:"
	for a in arguments: print a
	print "Il primoa rgomento è",arguments[1]
	#for a in arguments: print a

def magg(x):
	if x>20: return True

def filtra(L):
	a= filter(magg,L)
	#for x in a: print x
	return a

def doppio(x):
	return x*2

def mappa(L):
	a = map(doppio,L)
	#for x in a: print x
	#print a
	return a


# L = [12,39,52]
# listaMappa(L)

	

def concatenaListe():
	nomi = ['Paolo','Marilu','Laura']
	cognomi = ['Monella', 'Russo', 'Monella Russo']
	completi= [cognomi[i]+', '+nomi[i] for i in range(len(nomi))]
	
	belli=[]
	for i in range(len(nomi)):
		belli.append(cognomi[i]+', '+nomi[i])

	lung = map(len,nomi)
	lung = [len(a) for a in nomi]
	print lung

def dizionarioMacchina():
	testo = "Quel che è tuo è mio e quel che è mio è mio"
	stopw= set(['e','il'])
	lista=testo.split(' ')
	lista=set(lista)
	print 'Completa:',lista
	print 'Ripulita:',lista - stopw
	print 'Stop words rinvenute:',lista & stopw
	#print '\n Dizionario:'
	#for x in lista: print '\t'+x

def aprifile():
	a=open('ciao','r')
	for i in range(2):
		print a.readline()

def nomidefiniti():
	print "Spazio", __name__,":"
	for x in dir ():
		print x
	print '\n\n'
	print "Spazio cheeseshop:"
	for x in dir (cheeseshop):
		print x

def importaroba():
	import modulo1
	modulo1.bellicapelli('Mario')
	print modulo1.aax
	print dir(modulo1)

class myclass:
	def f(self,risposta):
		self.suoiDati = risposta
		

# x = myclass()
# x.f(42)
# myclass.f(x,42)
# print 'Risposta:',x.suoiDati

def ctrNum():
	while True:
		try:
			x = int(raw_input('Inserisci un numero: '))
		except ValueError:
			print 'Non è un numero valido!'
		else:
			print 'Ecco un numero valido!'
			break
def creaErr():
	try:
		raise Exception('primo', 'secondo')
	except Exception, istanza:
		print type(istanza)
		print istanza.args
		print istanza
		x, y = istanza
		print "x =",x,"\ny =", y

class numero:
	def __init__(self,valore,lingua,virgola):
		self._val = valore
		self._l = lingua
		self._v = virgola
	def potenza(self):
		return self._val ** 2
	def lunghezza(self):
		return self._val.repr.len()
	def scrivi(self):
		print str(self.valore)+self.v+"0 (lingua: "+self.l+")"


class nota:
	def __init__(self,testoAnnotato,testoAnnotazione,inizio,fine,tipoAnnotazione):
		self.t = testoAnnotato
		self.a = testoAnnotazione
		self.i = inizio
		self.f = fine
		self.tipo = tipoAnnotazione
	def porzione(self):
		return self.t[self.i:self.f]

#dante = "Nel mezzo del cammin di nostra vita"
#commento=[]
#commento.append(nota(dante,"Metafora",14,20,"Retorica"))
#commento.append(nota(dante,"Generalizzazione",24,30,"Retorica"))
#commento.append(nota(dante,"In the middle of the path of our life",0,50,"Traduzione"))
#print '\n'+dante+'\n\nCommento:'
#for i in commento:
#	print '"'+i.porzione()+'" ('+i.tipo+')'+': '+i.a
#print '\n'

class quantita():
	def __init__(self,ammontare):
		self.tot = ammontare
	def zeri(self):
		return len(str(self.tot))-1

class piccioli(quantita):
	curr = '' # Currency, cioè valuta (€, £ etc.)

class eredita(piccioli):
	def Quota(self,parentela):
		if parentela == "moglie":
			return self.tot/2
		if parentela == "fratello":
			return self.tot/3
		else:
			return 0

#eGino = eredita(50000)	# si tratta dell'eredità di gino
#eGino.curr = "€"
#print "Parliamo di un numero a",eGino.zeri(),"zeri!"
#print "La quota di Gennaro è", eGino.Quota("fratello"),eGino.curr
#print "La quota di Carmela è", eGino.Quota("moglie"),eGino.curr,"\n"

class mazzetta(piccioli):
	def Quota(self,persone):
		return self.tot/persone
	persone = 0

#Montedison = mazzetta(10000000000)
#Montedison.curr = "£"
#Montedison.persone = 19
#print "Parliamo di un numero a",Montedison.zeri(),"zeri!"
#print "Se siamo in "+str(Montedison.persone)+", la quota a persona è "+str(Montedison.Quota(Montedison.persone)),Montedison.curr
#
#print '\nDizionario di mazzetta:'
#for i in mazzetta.__dict__:
#	print '\t',i

def inV(dati):
	for i in range(len(dati)-1, -1, -1):
		yield dati[i]

#for x in range(len("sole")-1, -1, -1):
	#print "sole"[x]
	
def somma(a,b):
	return a+b

import doctest
doctest.testmod()

def imparaAlfabeto(a,b):
	return set(a)|set(b)
	#return set(a+b)
#lista = ["cacca", "acca", "caca"]
#print reduce(imparaAlfabeto,lista)
"""
