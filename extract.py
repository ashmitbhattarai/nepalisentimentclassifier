#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import defaultdict
from words import text_to_list,list_to_dict,file_to_list,stemword
from plot import pieplot,plotdata
from nepnb import classify
import os,sys,string,re

reload(sys)
sys.setdefaultencoding('utf8')

nepsent = classify()

sentlist = []
text2 = open('sentences.csv','rb')
sentlist = []
for each in text2.readlines():
	sentlist.append(each.strip())
text2.seek(0)
unilist = file_to_list(text2)
text2.close()

nounlist = []
nounpath = "/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/files/nounlist.txt"
nountext = open(nounpath,'rb')
for each in nountext.readlines():
	each = each.replace('(','').replace(')','').strip()
	nounlist.append(each)
nountext.close()

def analyzescore(wordlist,lineslist):
	scorelist = defaultdict(int)
	for each in lineslist:
		for words in wordlist:
			if words in each:
				scorelist[each.strip()] = nepsent.execute(each.strip())
	return sorted(scorelist.items(),key=lambda x : x[1],reverse = True)			

def nepunigrams():
	unidict = list_to_dict(unilist)
	#word_dict = collections.OrderedDict(sorted(newd.items()))
	#word_dict = sorted(newd,key=newd.__getitem__)
	finaldict = sorted(unidict.items(),key=lambda x : x[1],reverse = True)
	return finaldict

def nepbigrams(word,sentlist):
	bigrams = []
	dict_bigrams = defaultdict(int)
	for each in sentlist:
		each = each.strip()
		wlist  = each.split()
		for every in wlist:
			if word in every:
				if (wlist.index(every)!=len(wlist)-1):# and (wlist.index(every)!= 0):
					bigrams.append(word+" "+stemword(wlist[wlist.index(every)+1]).replace(" ",''))
					bigrams.append(stemword(wlist[wlist.index(every)-1]).replace(" ",'')+" "+word)
					break
	for each in bigrams:
		new = each.split()
		if len(new)>0:
			dict_bigrams[each] += 1
	return sorted(dict_bigrams.items(),key=lambda x : x[1],reverse = True)
###############################similar words in bigrams make up for same bigrams too#######################
def entitycount(sentlist,nounlist):
	###import from nouns####
	to_count = 0
	bigramsdict = {}
	finaldict = {}
	for each in nounlist:
		assortdict = defaultdict(int)
		nounwords = each.split()
		firstset=nepbigrams(nounwords[0],sentlist)
		if len(nounwords)>1:
			secondset=nepbigrams(nounwords[1],sentlist)
			for bigrams,count in secondset:
				for bigramms,counts in firstset:
					if bigrams in bigramms:
						bigramsdict[bigrams] = max(count,counts)
						assortdict['count'] += max(count,counts)
						break
			for bigrams,count in firstset:		
				if count > 5:
					bigramsdict[bigrams] = count
					assortdict['count'] += count
					break
			for bigramms,counts in secondset:
				if counts > 5:
					bigramsdict[bigramms] = counts
					assortdict['count'] += counts
					break
		if assortdict['count'] > 0:
			assortdict['bigrams'] = bigramsdict
			finaldict[each] = assortdict
	return finaldict

def piedata(word):
	files_path = []
	monthwise = defaultdict(int)
	months = {'असोज':"Asoj",'कार्तिक':"Kartik",'असार':"Ashar",'आश्विन':"Asoj",'जेष्ठ':"Jestha",'भाद्र':"Bhadra",'वैशाख':"Baiskhak",'श्रावण':"Shrawan"}
	path = '/home/ashmit/Legion/myproject/newproject/module/२०७१'
	for month,engmonth in months.items():
		pathlist = []
		filepath = os.path.join(path,month)
		for fpath in os.listdir(filepath):
			semipath = os.path.join(filepath,fpath)
			pathlist.append(semipath)
			for each in pathlist:
				for flpath in os.listdir(each):
					finalpath = os.path.join(each,flpath)
					files_path.append(finalpath)
	files_path = list(set(files_path))
	for each in files_path:
		datafile = open(each,'rb')
		totallist =  file_to_list(datafile)
		datafile.close()
		nepmonth = each.split("/")[8]
		engmonth = months[nepmonth]
		for alls in totallist:
			if word in alls:
				monthwise[engmonth] += 1
	return monthwise

def bishleshan(category,topic):
	unigrams = nepunigrams()
	countername = defaultdict(int)
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+topic.upper()+"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	for name,engnames in category.items():
		bigramslist = []
		bigrmsent = []
		for word,count in unigrams:
			if name in word:
				countername[engnames] += count
		nepalibigrm = nepbigrams(name,sentlist)
		for bigrams,count in nepalibigrm[:4]:
			bigramslist.append(bigrams)
			for sentence in sentlist:
				if bigrams in sentence:
					bigrmsent.append(sentence.strip())
		sentsscore = analyzescore(bigramslist,bigrmsent)
		print "\n++++++++++++++++++++++++++++++++++++++++++++++++SENTIMENT ANALYSIS OF WORD :"+name+"++++++++++++++++++++++++++++++++++++++++++++\n"
		print "In references to :",nepalibigrm[0][0]," OR ",nepalibigrm[1][0]
		print "==========================================================>>>>>>POSITIVE SENTENCES<<<<<<==========================================================\n"
		print "==========================================================>>>>>>>>>>>>>>><<<<<<<<<<<<<<<==========================================================\n"
		for line,score in sentsscore[:4]:
			print line,score,'\n'
		print "==========================================================>>>>>>NEGATIVE SENTENCES<<<<<<=========================================================\n"
		print "==========================================================>>>>>>>>>>>>>>><<<<<<<<<<<<<<<=========================================================\n"
		for line,score in sentsscore[-4:]:
			print line,score,'\n'
	topword = sorted(countername.items(),key=lambda x : x[1],reverse=True)[0][0]
	topname = category.keys()[category.values().index(topword)]
	namepie = piedata(topname)
	pieplot(namepie,"MONTHLY HITS ON WORD : "+category[topname])
	plotdata(countername,"TOP NAMES TOPICS")
	return 0

def finaldata():
	bigramslist = []
	topnames = {'ओली':"Oli",'प्रधानमन्त्री':"Pradhanmantri",'भट्टराई':"Bhattarai",'नेपाल':'Nepal','नेपाली':"Nepali"}
	topplace = {'नेपाल':'Nepal','भारत':"Bharat",'काठमाडौं':"Kathmandu",'दिल्ली':"Dehli",'प्रदेश':"Pradesh"}
	toporg = {'प्रहरी':"Police",'सरकार':"Government",'एमाओवादी':"U-Maoist",'एमाले':"CPN-UML",'अदालत':"Adalat"}
	topmisc = {'पार्टी':"Party(Political)",'निर्वाचन':"Election",'संविधान':"Constitution",'नेता':"Leader",'बैठक':"Meeting"}
	###now the processing begins ###barchart #inputword, piechart==>bigrams===>sentiment with sentences
	#####names########################
	bishleshan(topnames,'Names')
	bishleshan(topplace,'Place')
	bishleshan(toporg,'Organization')
	bishleshan(topmisc,'Miscellaneous')	
	return 0
finaldata()