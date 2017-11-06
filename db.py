#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os,sys,string,re,csv
import sqlite3
reload(sys)
sys.setdefaultencoding('utf8')

'''db = sqlite3.connect('nepdb')
chandler = db.cursor()
chandler.execute('CREATE TABLE shabda(id INTEGER PRIMARY KEY, word TEXT, count INTEGER,doc_type TEXT)')
chandler.execute('CREATE TABLE sentis(id INTEGER PRIMARY KEY,type TEXT,count INTEGER )')
chandler.execute('CREATE TABLE polarity(id INTEGER PRIMARY KEY, word TEXT)')
db.close()'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "nepdb")
class Db:
	def __init__(self):
		self.conn = sqlite3.connect(db_path) ##self.conn ===> handler
	def update_word_count(self,c,word,doc_type,newcount):
		c.execute('select count from shabda where doc_type=? and word=?',(doc_type,word.decode('utf-8')))
		r = c.fetchone() # since euta matra huncha
		if r:
			c.execute('update shabda set count=? where doc_type=? and word=?',(r[0]+newcount,doc_type,word.decode('utf-8')))
		else:
			c.execute('insert into shabda(word,count,doc_type) values(?,?,?)',(word.decode('utf-8'),newcount,doc_type))

	def update_words_count(self,d,doc_type):
		c =self.conn.cursor()
		#try block since insertion migh fail due to multiple errors
		try:
			for word,count in d.items():# d here is dictionary
				self.update_word_count(c,word,doc_type,count)
		finally:
			c.close()
			self.conn.commit()
	def get_doctype_counts(self):
		counts = {}
		c = self.conn.cursor()
		try:
			for row in c.execute('select type, count from sentis'):
				counts[row[0]] = row[1]
		finally:
			c.close()
			self.conn.commit()
		return counts

	def get_word_count(self,doc_type,word):
		c =self.conn.cursor()
		try:
			c.execute('select count from shabda where doc_type=? and word=?',(doc_type,word.decode('utf-8')))
			r = c.fetchone()
			if r:
				return r[0]
			else:
				return 0
		finally:
			c.close()
			self.conn.commit()

	def get_words_count(self,doc_type):
		c =self.conn.cursor()
		try:
			c.execute('select sum(count) from shabda where doc_type=?',(doc_type))
			r = c.fetchone()
			if r:
				return r[0]
			else:
				return 0
		finally:
			c.close()
			self.conn.commit()

	def update_doctype_count(self,added,doc_type):
		c=self.conn.cursor()
		try:
			counts = self.get_doctype_counts()
			if counts.has_key(doc_type):
				current_count = counts[doc_type]
			else:
				current_count = 0
			if current_count:
				c.execute('update sentis set count=? where type=?',(current_count+added,doc_type))
			else:
				c.execute('insert into sentis(type,count) values(?,?)',(doc_type,added))
		finally:
			c.close()
			self.conn.commit()
	def update_polwords(self):
		c=self.conn.cursor()
		polfile = open("/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/files/f_polarity.csv",'rb')
		try:
			for each in polfile.readlines():
				each = each.strip()
				c.execute('insert into polarity(word) values(?)',(each.decode('utf-8'),))
		finally:
			c.close()
			self.conn.commit()

	def get_polwords(self):
		c =self.conn.cursor()
		polwords = []
		try:
			c.execute('select * from polarity')
			r = c.fetchall()
			for each in r:
				polwords.append(each[1])
		finally:
			c.close()
			self.conn.commit()
		return polwords

	def printall(self):
		c = self.conn.cursor()
		try:
			c.execute("select * from shabda where doc_type = ?",('p'))
			r = c.fetchall()
			for each in r:
				print each[1],each[2],each[3]
		finally:
			c.close()
			self.conn.commit()

	def reset(self):
		c =self.conn.cursor()
		try:
			c.execute('delete from shabda')
			c.execute('delete from sentis')
			#c.execute('delete from polarity')
		finally:
			c.close()
			self.conn.commit()