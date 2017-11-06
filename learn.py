#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from words import text_to_list,list_to_dict,file_to_list
from db import Db
import os,sys,string,re,csv
import collections
reload(sys)
sys.setdefaultencoding('utf8')
if sys.argv[1].lower() == 'p':
	textname = 'positive.csv'
	text = open(textname,'rb')
elif sys.argv[1].lower() == 'n':
	textname = 'negative.csv'
	text = open(textname,'rb')
else:
	print "Invalid Entry"
	sys.exit(True)
newl = file_to_list(text)
newd = list_to_dict(newl)
#word_dict = collections.OrderedDict(sorted(newd.items()))
#word_dict = sorted(newd,key=newd.__getitem__)
for word,count in sorted(newd.items(),key=lambda x: x[1],reverse=True): ###########################need to sort the list according to count here
	print word,count
#########pos or neg lai db ma rakhnu paryo#################
db = Db()
counts = db.get_doctype_counts()
#poscount = counts['p']
#negcount = counts['n']
if sys.argv[1].lower() == "p":
	db.update_words_count(newd,'p')
	db.update_doctype_count(len(newd),'p')
elif sys.argv[1].lower() == 'n':
	db.update_words_count(newd,'n')
	db.update_doctype_count(len(newd),'n')
else:
	print "invalid entry"
#############################################################################################################################