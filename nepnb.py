#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from words import text_to_list,stemword
from db import Db
import os,sys,string,re,csv
import sqlite3
reload(sys)
sys.setdefaultencoding('utf8')

class classify():
	min_freq = 2 # change the stats after taking avg of min vs max repeats
	less_freq_prob = 0.5
	max_freq_prob = 0.99

	def set_text(self,text): #just pass list here one line only
		self.text = text
		lines = [] # shorten this later
		words = text_to_list(line)
		if not len(words):
			raise ValueError ('Text doesnt contain valid keywords') ## sabb ma nepali message pass garnu
		else:
			for word in words:
				lines.append(word)

		self.lines = lines
		return self

	def find_values(self,word):
		word = stemword(word)
		db = Db()
		total_p = float(db.get_words_count('p'))
		total_n = float(db.get_words_count('n'))
		word_p = float(db.get_word_count('p',word))
		word_n = float(db.get_word_count('n',word))

		if word_p + word_n < self.min_freq:
			return self.less_freq_prob
		if word_p == 0:
			return 1-self.max_freq_prob
		elif word_n == 0:
			return self.max_freq_prob

		p_wp = float(word_p/total_p)
		p_wn = float(word_n/total_n)
		return p_wp/(p_wp+p_wn)

	def find_values_list(self,l):
		##find values of each word in the list :D##
		p_product         = reduce(lambda x,y: x*y, l) #multiply all
		p_inverse_product = reduce(lambda x,y: x*y, map(lambda x: 1-x, l)) # inverse multiply all

		return p_product / (p_product + p_inverse_product) #harmonic mean

	def execute(self,lines):
		polcount = 0
		prob_list = []
		db = Db()
		polwords=db.get_polwords()
		lines = lines.split('।')[0]
		for each in lines.split():
			if each.strip() not in polwords:
				prob_list.append(self.find_values(each.strip()))
			else:
				polcount += 1
		result = (self.find_values_list(prob_list))
		if polcount%2:
			result = 1-result
		return result
