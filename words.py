#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from db import Db
import os,sys,string,re,csv
reload(sys)
sys.setdefaultencoding('utf8')

stopwords = []

stopfile = open('/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/files/rev_stopwords.csv','rb')
for each in stopfile:
	each = each.replace('\t','').replace(' ','').strip()
	if each:
		stopwords.append(each)
stopfile.close()
db = Db()
polwords = db.get_polwords()
def clean_words(word):
	if len(word.strip()) < 6:
		return None
	elif re.findall(r'^(०|१|२|३|४|५|६|७|८|९)',word): ###letter bhako excluded
		return None
	elif word in stopwords:
		return None
	elif word in polwords:
		return None
	else:
		return word

###########################check for valid unigrams and stemming#############################
################################################################################
def stemword(word):
	x = re.findall(r'^((.*?)(लाई|ले|लागि|बाट|देखि|को|की|का|मा|माथि|कै|हरु|मै|न्ने|सँग))$', word)
	if x:
		y = re.findall(r'^((.*?)(लाई|ले|लागि|बाट|देखि|को|की|का|मा|माथि|कै|हरु|मै|न्ने|सँग))$', x[0][1])
		if y:	
			return y[0][1]
		else:
			return x[0][1]
	elif word.replace("'","").replace(" ",'').strip():
		return word.replace("'","").replace(" ",'').strip()
	else:
		return None
##################################################################################
def list_to_dict(l):
	d = defaultdict(int)
	for word in l:
		d[word] += 1
	return d

def file_to_list(text):
	words = []
	sent_words = []
	for sent in text:
		sent_words = text_to_list(sent.strip())
		for each in sent_words:
			words.append(each)
	return words

def text_to_list(text):
	words = []
	text = text.replace("।",' ').replace('-','').replace('.','').replace('?','').replace('"','').replace("'","").replace('\t','').replace(',','').replace(')','').replace('(','').strip()
	for word in text.split():
		word = word.replace(' ','')
		word = stemword(word)
		word = clean_words(word)
		if word and len(word.split())>0:
			word = word.replace(' ','')
			words.append(word.replace(' ','').replace('\x0b','').replace('\x0c','').replace('\x00','').strip())
	return words
