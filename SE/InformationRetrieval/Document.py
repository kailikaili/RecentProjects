#!/usr/bin/python
#filename: Document.py
import sqlite3
import xml.etree.ElementTree as et
import re
from stemming.porter2 import stem
import time
class Document:
    
    def __init__(self,filename):
        try:
            self.filename = filename
            self.parseFile()
            self.splitDocument()
            self.trackLoc()
            self.buildTF()
        except:
            print "input file format error, please check it"

    def parseFile(self):
        try:
            tree = et.parse(self.filename)
            doc = tree.getroot()
            self.DOC_NO = int(doc.find('DOCNO').text)
            self.DOC_TITLE = doc.find('TITLE').text
            self.DOC_TITLE = self.DOC_TITLE.strip()
            self.DOC_AUTHOR = doc.find('AUTHOR').text
            self.DOC_AUTHOR = self.DOC_AUTHOR.strip()
            self.DOC_BIBLIO = doc.find('BIBLIO').text
            self.DOC_BIBLIO = self.DOC_BIBLIO.strip()
            self.DOC_TEXT = doc.find('TEXT').text
            self.DOC_TEXT = self.DOC_TEXT.strip()
        except:
            print "input file format error, please check it"

        #self.fileContent = self.DOC_TITLE + self.DOC_AUTHOR + self.DOC_BIBLIO + self.DOC_TEXT
        #print self.fileContent

    def splitDocument(self):
        self.words = re.split('\W+',self.DOC_TEXT)
        self.words = filter(None,self.words)
        self.words = [stem(word.lower()) for word in self.words]
        #print self.words

    def trackLoc(self):
        pre = ' '
        loc = 0
        word = 1
        self.wordLoc = dict()
        for c in self.DOC_TEXT:
            if (re.match('\w',c,0) and not re.match('\w',pre,0)):
                self.wordLoc[word] = loc
                word +=1
            loc+=1
            pre = c


    def buildTF(self):
        self.TF = dict()
        for word in self.words:
            if(self.TF.has_key(word)):
                self.TF[word] += 1
            else:
                self.TF[word] = 1
        return self.TF

    def write2DB(self,cu):
        cu.execute('''insert into document values( %d,"%s","%s","%s","%s")'''%(self.DOC_NO,self.DOC_TITLE, self.DOC_AUTHOR, self.DOC_BIBLIO, self.DOC_TEXT))

