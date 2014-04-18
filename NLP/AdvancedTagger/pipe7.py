"""
This is an example of how to call the CL "servers" in python.
"""

from itertools import *
from subprocess import PIPE
from hisGen import HisGen
import sys, subprocess, time, re

def process(args):
        "Create a 'server' to send commands to."
        return subprocess.Popen(args, stdin=PIPE, stdout=PIPE)

def call(process, stdin):
        "Send command to a server and get stdout."
        output = process.stdin.write(stdin.strip() + '\n\n')
        line = "" 
        while 1: 
                l = process.stdout.readline()
                if not l.strip(): break
                line += l
        return line

if __name__ == "__main__":
        startT = time.clock()
        sentence = ''
        gd = ''
        hisGen = HisGen(sys.argv[1], 'fea5.dat') 
        enum_server = process(["python", "tagger_history_generator.py", "ENUM"])
        his_server = process(["python", "tagger_decoder.py",  "HISTORY"])
        trF = open(sys.argv[2], 'r')
        gdF = open(sys.argv[3], 'r')
        for l, lg in izip(trF, gdF):
                if not l: break
                if l.strip() == '':
                        history = call(enum_server, sentence) 
                        score = hisGen.genScore(sentence, history) 
                        pred = call(his_server, score)
                        hisGen.update(pred, gd, sentence)
                        #print pred
                        sentence = ''
                        gd = ''
                else:
                        sentence += l 
                        gd += lg
                        #print gd
        hisGen.genModel(sys.argv[1])    
        endT = time.clock()