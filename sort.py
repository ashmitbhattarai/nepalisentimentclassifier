#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import defaultdict
from words import text_to_list,list_to_dict,file_to_list,stemword
from plot import pieplot,plotdata
import os,sys,string,re,csv
reload(sys)
sys.setdefaultencoding('utf8')
path = os.path.realpath('.')
posfile = open("positive.csv",'a')
negfile = open("negative.csv",'a')
for each in os.listdir('train/'):
	print each
	textfile=open(os.path.join(path,'train',each),'rb')
	for each in textfile.readlines():
		words = each.split("\t")
		if words[1] == "1":
			posfile.write(words[2].replace(","," ").replace('"','').strip()+"\n")
		elif words[1] == "-1":
			negfile.write(words[2].replace(","," ").replace('"','').strip()+"\n")
posfile.close()
negfile.close()
os.system('python learn.py p')
os.system('python learn.py n')
print "Positive and Negative Words Fed to Database"