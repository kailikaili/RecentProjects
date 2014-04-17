#!/usr/bin/python

from Document import Document
import cPickle as pickle
from IDF import IDF
from os import system
import sqlite3
import time
import sys, os, tarfile, math
class Index:
	'''build up invert Index'''

	def __init__(self):
		self.wordList = dict()
		self.num_doc = 0
		pass


	def buildIndex(self, doc):

		self.num_doc += 1

		doc_no = int(doc.DOC_NO)
		words = doc.words
		loc= 1
		for word in words:
			item = (doc_no, loc)
			if self.wordList.has_key(word):
				self.wordList[word].append(item)
			else:
				itemList = [item]
				self.wordList[word] = itemList
			loc+=1

	def seldomWords(self):
		self.seldomWordsList = dict()

		for word in self.wordList.keys():
			if len(word) < 20:
				self.seldomWordsList[word] = self.wordList[word]

	def wordsVector(self):
		self.documentList = [[0 for x in range(len(self.seldomWordsList.keys()))] for y in range(self.num_doc)]
		i=-1
		for word in self.seldomWordsList.keys():
			i += 1
			for (doc_no, loc) in self.seldomWordsList[word]:
				self.documentList[doc_no][i] = 1

	def cosineSimilarity(self):

		self.cosinePair = [[0 for x in range(self.num_doc)] for y in range(self.num_doc)]

		self.documentLength = [0 for x in range(self.num_doc)]
		for m in range(self.num_doc):
			sums = 0
			for s in range(len(self.seldomWordsList.keys())):
				sums = sums + self.documentList[m][s]
			self.documentLength[m] = math.sqrt(sums)


		for i in range(self.num_doc):
			print i
			for j in xrange(i+1, self.num_doc):
				sums = 0
				for k in range(len(self.seldomWordsList.keys())):
					sums = sums + self.documentList[i][k]*self.documentList[j][k]

				self.cosinePair[i][j] = float(1.0+sums)/float(1.0+self.documentLength[i]*self.documentLength[j])

				if self.cosinePair[i][j] > 0.7:
					print "doc: %d, doc: %d : %f"%(i,j,self.cosinePair[i][j])

print "start indexing..."
system("rm ./mydb.db3")
con = sqlite3.connect('./mydb.db3')
cur = con.cursor()

cur.execute('CREATE TABLE document(did INTEGER PRIMARY KEY, title VARCHAR(100),author VARCHAR(100), biblio VARCHAR(200), content VARCHAR(9999999))')
con.commit()

start_time = time.time()
idf = IDF(sys.argv[1])
index = Index()
i = 1
size = len(idf.files)
tf = dict()
wordLoc = dict()
t = 0
for f in idf.files:
    try:
	    temp = time.time()
	    doc = Document(f)
	    index.buildIndex(doc)
	    tf[doc.DOC_NO] = doc.TF
	    wordLoc[doc.DOC_NO] = doc.wordLoc
	    idf.buildDF(doc)
	    t=t + (time.time()-temp)
	    doc.write2DB(cur)
	    i +=1
	    if i%10==0:
	    	if i%300==0:
	    		con.commit()
	    	percent = i*100/size
	    	t = time.time() - start_time
	    	sys.stdout.write('\r indexing...\033[92m%2d\033[0m%%   \033[92m%2.0f\033[0ms'%(percent,t))
	    	sys.stdout.flush()
    except:
        print " some file format is not correct!"
        continue
con.commit()
idf.buildIDF()
index.seldomWords()
index.wordsVector()
index.cosineSimilarity()
print "\n\n\n\rindex complete!\n"
print "total index time : \033[92m%3.2f\033[0ms"%t


indexStore = open('index.my','wb')
#picklist = [index.wordList,idf.DF,tf,wordLoc]
#pickle.dump(picklist,indexStore,0)
pickle.dump(index.wordList,indexStore,0)
pickle.dump(idf.DF,indexStore,0)
pickle.dump(tf,indexStore,0)
pickle.dump(wordLoc,indexStore,0)
indexStore.close()
print "start compressing the index"
compress_time = time.time()
tar = tarfile.open("index.tar.gz","w:gz")
tar.add('index.my','index.my')
tar.close()
os.remove('index.my')
print "compress complete"
print "total time to compress %.0fs"%(time.time()-compress_time)
filestat = os.stat('index.tar.gz')
file_size = filestat.st_size
file_size = file_size/1024
print "total index size : \033[92m%.0f\033[0mKB"%file_size
