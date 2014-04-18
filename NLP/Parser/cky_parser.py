import sys,re,math,time

negInf = -100000
#recursion for generating tree
def genTree(tree):
        if len(tree) == 2:
                return '[\"' + tree[0] + '\", \"' + tree[1] + '\"]' 
        elif len(tree) == 3:
                return '[\"' + tree[0] + '\", ' + genTree(tree[1]) + ', ' + genTree(tree[2]) + ']'
        return ''
#function for generating probability for unary and binary rules 
def genProb(inputf):
        f_in = open(inputf, 'r')
        ntp = re.compile('(\d+)\sNONTERMINAL\s(\S+)')
        up = re.compile('(\d+)\sUNARYRULE\s(\S+)\s(\S+)')
        bip = re.compile('(\d+)\sBINARYRULE\s(\S+)\s(\S+)\s(\S+)')
        ntd = {}
        ud = {}
        bid = {}
        tset = set()
        for line in f_in:
                ntm = ntp.match(line)
                if ntm:
                        ntd[ntm.group(2)] = float(ntm.group(1))
                        continue
                um = up.match(line)
                if um:
                        x = um.group(2)
                        w = um.group(3)
                        tset.add(w)
                        cnt = float(um.group(1))
                        ud[x, w] = math.log(cnt/ntd[x])
                        continue
                bim = bip.match(line)   
                if bim:
                        x = bim.group(2)
                        y = bim.group(3)
                        z = bim.group(4)
                        cnt = float(bim.group(1))
                        if x in bid:
                                bid[x][y,z] = math.log(cnt/ntd[x])
                        else:
                                bid[x] = {(y,z):math.log(cnt/ntd[x])}
        f_in.close()                    
        return (ud, bid, ntd.keys(), tset)

#the cky parsing algorithm 
#s: the input sentence
#unAry: the unary rules prob 
#binAry: the binary rules prob 
#noTerm: the non-terminal set 
#term: the terminal set 
def cky(s, unAry, binAry, noTerm, term):
        w = re.compile('\s+').split(s)
        #initialization for the DP
        n = len(w)
        pi = {}
        bp = {}
        for i in range(0, n):
                wi = w[i]
                if wi not in term:
                        wi = '_RARE_'
                for X in noTerm:
                        if (X,wi) in unAry:
                                pi[i,i,X] = unAry[X,wi]
                        else:
                                pi[i,i,X] = negInf
                        bp[i,i,X] = [X, w[i]]
        trace = {}
        for l in range(1, n):
                for i in range(0, n-l):
                        j = i + l
                        for X in noTerm:
                                score = negInf
                                tbp = []
                                if X in binAry:
                                        for (Y, Z) in binAry[X]:
                                                for k in range(i, j):
                                                        tmpScore = binAry[X][Y,Z] + pi[i,k,Y] + pi[k+1,j,Z]
                                                        if tmpScore > score:
                                                                score = tmpScore
                                                                tbp = [X, bp[i,k,Y], bp[k+1,j,Z]]
                                pi[i,j,X] = score
                                bp[i,j,X] = tbp
        if pi[0,n-1,'S'] != negInf:
                return genTree(bp[0,n-1,'S'])
        else:
                score = negInf
                tr = []
                for X in noTerm:
                        tmpScore = pi[0, n-1, X]
                        if tmpScore > score:
                                score = tmpScore
                                tr = bp[0, n-1, X]
                return genTree(tr)
        return '' 

#arg1: count file for the nonterminals and rules        
#arg2: targeting sentences 
#arg3: output tree file 
if __name__ == "__main__":
        (unAry, binAry, noTerm, term) = genProb(sys.argv[1])
        passage = open(sys.argv[2], 'r')
        f_out = open(sys.argv[3], 'w')
        start = time.clock()
        for line in passage:
                line=line.strip('\n')
                        #run the cky algorithm
                f_out.write(cky(line, unAry, binAry, noTerm,term) + '\n')
        end = time.clock();
        print 'Processing Time:' + str((end - start)) + 'sec'
        passage.close()
        f_out.close()
