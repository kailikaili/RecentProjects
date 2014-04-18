"""
This is an example of how to call the CL "servers" in python.
"""

from subprocess import PIPE
from hisGen import HisGen
import sys, subprocess, time, re

def process(args):
    "Create a 'server' to send commands to."
    return subprocess.Popen(args, stdin=PIPE, stdout=PIPE)

def call(process, stdin):
    "Send command to a server and get stdout."
    output = process.stdin.write(stdin.strip() + "\n\n")
    line = ""
    while 1: 
        l = process.stdout.readline()
        if not l.strip(): break
        line += l
    return line

if __name__ == "__main__":
# Create a history server.
    gold_server = process(["python", "tagger_history_generator.py", "GOLD"])
    enum_server = process(["python", "tagger_history_generator.py", "ENUM"])
    his_server = process(["python", "tagger_decoder.py", "HISTORY"])

    start_time = time.clock()
    hisGen = HisGen(sys.argv[2], 'fea.dat')
    sentence = ''
    while 1:
        l = sys.stdin.readline()
        if not l: break
        if l.strip() == '':
            history = call(enum_server, sentence.strip())
            #print sentence
            score = hisGen.genScore(sentence, history)
            #print score
            out = call(his_server, score.strip())
            out = out.strip().split('\n')
            sent = sentence.strip().split('\n')
            i = 0
            for line in out[:-1]:
                line = line.strip().split(' ')

                newline = sent[i] + ' ' + line[2]
                i = i+1

                print newline
            print ''
            sentence = ''
        else:
            sentence += l
    end_time = time.clock()
    print >> sys.stderr, 'Processing Time:' + str((end_time - start_time)) + 'sec'
