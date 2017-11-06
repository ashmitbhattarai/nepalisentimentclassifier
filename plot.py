# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
import random

# The slices will be ordered and plotted counter-clockwise.
def pieplot(d,title):	
	labels = d.keys()
	total = sum(d.values())
	sizes = []
	for each in d.values()[:-1]:
		sizes.append(each*100/total)
	sizes.append(100-sum(sizes))
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','red',"green","white"]
	explode = (0, 0.1, 0,0,0,0,0) # only "explode" the 2nd slice (i.e. 'Hogs')
	plt.text(0.17,1.1,title,horizontalalignment="center",fontsize = 18)
	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
	        autopct='%1.1f%%', shadow=True, startangle=90)
	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')

	plt.show()
	return 0

def plotdata(d,title):
	N = 5
	words = d.keys()
	values = d.values()
	ind = np.arange(N)
	width = 0.35
	colors = ['r','b','g','y','m']
	p1 = plt.bar(ind,values,width,color=colors[random.randint(0,3)])
	plt.ylabel('Words Count')
	plt.xlabel('Words')
	plt.title(title)
	plt.xticks(ind+width/2.,d.keys())
	plt.ylim([0,250])
	plt.show()
	return 0