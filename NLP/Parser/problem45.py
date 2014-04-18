import math
import json
import sys
#problem 4
Dict={}
rarecount=0
count=0
def replace(x):#replace all rare items in a tree x
    global rarecount
    global count
    if len(x)==3:
        replace(x[1])
        replace(x[2])
    elif len(x)==2:
        count+=1
        if x[1] in Dict and Dict[x[1]]<5:
            x[1]="_RARE_"
            rarecount+=1
def dfs(x):#deep first traverse the tree x to calculate counts of words
    if not isinstance(x,list):
        if x in Dict:
            Dict[x]+=1
        else:
            Dict[x]=1
    else:
        for i in x[1:]:
            dfs(i)
#count words in all trees
f1=open("parse_train.dat","r")
l=f1.readline()
while l:
    l1 = json.loads(l)
    #l1=eval(l.strip())
    dfs(l1)
    l=f1.readline()
f1.close()
#replace rare words
f1=open("parse_train.dat","r")
f2=open("parse_train2.dat","w")
l=f1.readline()
while l:
    l1=eval(l.strip())
    replace(l1)
    f2.write(json.dumps(l1)+"\n")
    l=f1.readline()
f1.close()
f2.close()
#problem 5
#count frequency for all rules and nonterminals
DictX={}
DictXw={}
DictXYZ={}
f1=open("cfg2.counts","r")
l=f1.readline()
#count nonterminals
while l:
    l1=l.strip()
    l1=l1.split()
    if l1[2] in DictX:
        DictX[l1[2]]+=l1[0]
    else:
        DictX[l1[2]]=l1[0]
    if l1[1]!='NONTERMINAL':
        break
    l=f1.readline()

#count unary rules
while l:
    l1=l.strip()
    l1=l1.split()
    rule=tuple(l1[2:])
    if rule in DictXw:
        DictXw[rule]+=l1[0]
    else:
        DictXw[rule]=l1[0]
    if l1[1]!='UNARYRULE':
        break
    l=f1.readline()
#count binary rules
while l:
    l1=l.strip()
    l1=l1.split()
    rule=tuple(l1[2:])
    if rule in DictXYZ:
        DictXYZ[rule]+=l1[0]
    else:
        DictXYZ[rule]=l1[0]
    if l1[1]!='BINARYRULE':
        break
    l=f1.readline()
f1.close()
Xlist=DictX.keys()
Xwlist=DictXw.keys()
XYZlist=DictXYZ.keys()
f1=open("parse_dev.dat","r")
f2=open("parse_dev2.key","w")
#probability of binary rules
def q(X,Y1,Y2):
    if not (X,Y1,Y2) in DictXYZ:
        return 0
    else:
        return float(DictXYZ[(X,Y1,Y2)])/float(DictX[X])
#probability of unary rules
def q1(X,w):
    if not (X,w) in DictXw:
        return 0
    else:
        return float(DictXw[(X,w)])/float(DictX[X])
#CKY algorithm
def DPP(sentence):   
    l=len(sentence)
    l1=len(DictX)
    Pi=[[[-100000 for x in range(l1)] for y in range(l)]for z in range(l)]#probability
    Bp=[[[None for x in range(l1)] for y in range(l)]for z in range(l)]#backpointer
    def buildtree(i,j,x):#small subfunction used to build trees
        if i==j:#unary rules
            return [Xlist[x],sentence[i]]
        else:#binary rule, build subtrees recursively and then build the main tree
            return [Xlist[x],buildtree(i,Bp[i][j][x][0],Xlist.index(Bp[i][j][x][1][1])),buildtree(Bp[i][j][x][0]+1,j,Xlist.index(Bp[i][j][x][1][2]))]
    for i in range(l):
        for j,X in enumerate(Xlist):
            if (X,sentence[i]) in DictXw:
                Pi[i][i][j]=math.log(q1(X,sentence[i]))
            else:
                Pi[i][i][j]=-100000
    for i in range(1,l):
        for j in range(0,l-i):
            for k,X in enumerate(Xlist):
                Xyz=filter(lambda x:x[0]==X,XYZlist)#all rules in X-YZ form
                Prob=-100000
                Back=None
                for Rule in Xyz:
                    for m in range(i):
                        Prob1=math.log(q(X,Rule[1],Rule[2]))+Pi[j][j+m][Xlist.index(Rule[1])]+Pi[j+m+1][j+i][Xlist.index(Rule[2])]
                        if Prob1>Prob:
                            Prob=Prob1
                            Back=(j+m,Rule)
                Pi[j][i+j][k]=Prob
                Bp[j][i+j][k]=Back
    if Pi[0][i-1][Xlist.index("S")]>-100000:
        
        return buildtree(0,l-1,Xlist.index("S"))
    else:
        Maxp=max(Pi[0][l-1])
        MaxPos=Pi[0][l-1].index(Maxp)
        return buildtree(0,l-1,MaxPos)
l=f1.readline()
def replace1(string):#replace all infrequent words in a sentence to '_RARE_'
    for i,X in enumerate(string):
        if  not X in Dict or Dict[X]<5:
            string[i]='_RARE_'
while l:
    l1=l.strip().split()
    replace1(l1)
    Tree=DPP(l1)
    print json.dumps(Tree)
    f2.write(json.dumps(Tree).replace('\x04',''))
    f2.write("\n")
    l=f1.readline()
f1.close
f2.close
            
