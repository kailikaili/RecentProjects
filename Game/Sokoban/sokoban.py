'''
Created on Oct 19, 2013

@author: Hebo
'''

import sys
import os
import time
from array import array
from collections import deque

puzzleMap = []
maxRowLen = 0
px = py = 0
sdata = ""
ddata = ""
deadLockCheck = 0
# python sokoban puzzle1.txt 1 1 00000 0

def main(argv):
    global deadLockCheck
    init(argv[0])
    print '\n'
    [numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime] = list(argv[3])
    deadLockCheck = argv[4]
    if argv[1] == '1':
        solve_bfs(numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime)
    elif argv[1] == '2':
        solve_dfs(numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime)
    elif argv[1] == '3':
        solve_ucs(numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime)
    elif argv[1] == '4':
        if argv[2] == '1':
            solve_greedy1(numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime)    
        if argv[2] == '2':
            solve_greedy2(numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime)  
    elif argv[1] == '5':
        if argv[2] == '1':
            solve_aStar1(numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime)    
        if argv[2] == '2':
            solve_aStar2(numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime)  
        
def init(puzzleName):
    global puzzleMap, maxRowLen, sdata, ddata, px, py
    path = (os.getcwd())+'/'
    f = open(path + 'puzzles/' + puzzleName, 'rb')
    puzzleMap = f.read().splitlines()
    maxRowLen = max(len(r) for r in puzzleMap)
    nofLines = int(puzzleMap[0])
    puzzleMap = puzzleMap[1:nofLines+1]
    maps = {' ':' ', '.': '.', '@':' ', '#':'#', '$':' ', '*':'.', '+':'.'}
    mapd = {' ':' ', '.': ' ', '@':'@', '#':' ', '$':'*', '*':'*', '+':'@'}

    for r, row in enumerate(puzzleMap):
        for c, ch in enumerate(row):
            sdata += maps[ch]
            ddata += mapd[ch]
            if ch == '@':
                px = c
                py = r
        for i in xrange(maxRowLen-len(row)):
            sdata += ' '        
            ddata += ' '
                
def push(x, y, dx, dy, puzzleMap):
    if sdata[(y+2*dy) * maxRowLen + x+2*dx] == '#' or \
       puzzleMap[(y+2*dy) * maxRowLen + x+2*dx] != ' ':
        return None

    data2 = array("c", puzzleMap)
    data2[y * maxRowLen + x] = ' '
    data2[(y+dy) * maxRowLen + x+dx] = '@'
    data2[(y+2*dy) * maxRowLen + x+2*dx] = '*'
    return data2.tostring()

def is_solved(puzzleMap):
    for i in xrange(len(puzzleMap)):
        if (sdata[i] == '.') != (puzzleMap[i] == '*'):
            return False
    return True

def printstats(flagList,statList):
    nameList = ['Number of Nodes in Total', 'Number of Nodes Generated Previously', 'Number of Nodes on Fringe', 
     'Number of Nodes Explored', 'Run Time']
    for i, flag in enumerate(flagList):
        if flag=='1':
            print nameList[i]+':', statList[i]
    
def checkDeadlock(x, y, dx, dy, puzzleMap):
    if deadLockCheck == '1':
        ddx = int(not(dx))
        ddy = int(not(dy))
        dirs = ((ddx,ddy),(-ddx,-ddy))
        c = 0
        if sdata[(y+2*dy) * maxRowLen + x+2*dx] != '.':
            if sdata[(y+3*dy) * maxRowLen + x+3*dx] == '#' or \
                puzzleMap[(y+3*dy) * maxRowLen + x+3*dx] != ' ':
                for di in dirs:
                    ddx, ddy = di[0], di[1]
                    if sdata[(y+2*dy+ddy) * maxRowLen + x+2*dx+ddx] =='#' or \
                        puzzleMap[(y+2*dy+ddy) * maxRowLen + x+2*dx+ddx] != ' ':
                        c += 1
        #if sdata[(y+2*dy) * maxRowLen + x+2*dx]
         
        if c:
            return False
    #no deadlock
    return True
 

def solve_bfs(numNodeTotal = None, numNodesGenPre = None, numNodesFringe = None, \
              numNodesExplored = None, runTime = None):
    
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    tic = time.clock()
    
    openQue = deque([(ddata, "", px, py)])
    visited = set([ddata])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))

    lmaxRowLen = maxRowLen
    while openQue:
        cur, csol, x, y = openQue.popleft()

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lmaxRowLen + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and checkDeadlock(x, y, dx, dy, temp):
                    nodesTotal += 1
                    if temp not in visited:
                        visited.add(temp)
                        nodesExpl = len(visited)
                        if is_solved(temp):
                            toc = time.clock()
                            print csol + di[2]
                            nodesRem = len(openQue)
                            printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                            return True
                        openQue.append((temp, csol + di[2], x+dx, y+dy))
                    else:
                        nodesPrev += 1
            else:
                if sdata[(y+dy) * lmaxRowLen + x+dx] == '#' or \
                   temp[(y+dy) * lmaxRowLen + x+dx] != ' ':
                    continue
                
                nodesTotal += 1

                data2 = array("c", temp)
                data2[y * lmaxRowLen + x] = ' '
                data2[(y+dy) * lmaxRowLen + x+dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_solved(temp):
                        nodesRem = len(openQue)
                        
                        toc = time.clock()
                        print csol + di[2]
                        printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                        return True
                    openQue.append((temp, csol + di[2], x+dx, y+dy))
                else:
                    nodesPrev += 1
    toc = time.clock()
    print "No solution"
    printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
    return False
    
def solve_dfs(numNodeTotal = None, numNodesGenPre = None, numNodesFringe = None, \
              numNodesExplored = None, runTime = None):
    
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    tic = time.clock()
        
    openStack = [(ddata, "", px, py)]
    visited = set([ddata])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))

    lmaxRowLen = maxRowLen
    while openStack:
        cur, csol, x, y = openStack.pop()

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lmaxRowLen + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and checkDeadlock(x, y, dx, dy, temp):
                    nodesTotal += 1 
                    if temp not in visited:
                        visited.add(temp)
                        nodesExpl = len(visited)
                        if is_solved(temp):
                            toc = time.clock()
                            print csol + di[2]
                            nodesRem = len(openStack)
                            printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                            return True
                        openStack.append((temp, csol + di[2], x+dx, y+dy))
                    else:
                        nodesPrev += 1
            else:
                if sdata[(y+dy) * lmaxRowLen + x+dx] == '#' or \
                   temp[(y+dy) * lmaxRowLen + x+dx] != ' ':
                    continue
                
                nodesTotal += 1
                data2 = array("c", temp)
                data2[y * lmaxRowLen + x] = ' '
                data2[(y+dy) * lmaxRowLen + x+dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_solved(temp):
                        nodesRem = len(openStack)
                        toc = time.clock()
                        print csol + di[2]
                        printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                        return True
                    openStack.append((temp, csol + di[2], x+dx, y+dy))
                else:
                    nodesPrev += 1

    toc = time.clock()
    print "No solution"
    printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
    return False

def solve_ucs(numNodeTotal = None, numNodesGenPre = None, numNodesFringe = None, \
              numNodesExplored = None, runTime = None):
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    tic = time.clock()
        
    openQue = [(ddata, "", px, py, 0)]
    
    visited = set([ddata])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))

    lmaxRowLen = maxRowLen
    while openQue:
        openQue = sorted(openQue, key =lambda ele: ele[4])
        cur, csol, x, y, c= openQue.pop(0)

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lmaxRowLen + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and checkDeadlock(x, y, dx, dy, temp):
                    nodesTotal += 1
                    if temp not in visited:
                        visited.add(temp)
                        nodesExpl = len(visited)
                        if is_solved(temp):
                            toc = time.clock()
                            print csol + di[2]
                            nodesRem = len(openQue)
                            printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                            return True
                        openQue.append((temp, csol + di[2], x+dx, y+dy, c + 2))
                    else:
                        nodesPrev += 1    
            else:
                if sdata[(y+dy) * lmaxRowLen + x+dx] == '#' or \
                   temp[(y+dy) * lmaxRowLen + x+dx] != ' ':
                    continue
                nodesTotal += 1
                data2 = array("c", temp)
                data2[y * lmaxRowLen + x] = ' '
                data2[(y+dy) * lmaxRowLen + x+dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_solved(temp):
                        nodesRem = len(openQue)
                        toc = time.clock()
                        print csol + di[2]
                        printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                        return True
                    openQue.append((temp, csol + di[2], x+dx, y+dy, c + 1))
                else:
                    nodesPrev += 1    

    toc = time.clock()
    print "No solution"
    printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
    return False

def calcost1(x, y, dx, dy, temp):
    target = []
    for i, ltr in enumerate(sdata):
        if ltr =='.' and temp[i] != '*':
            target.append(i)
    target = [(b/maxRowLen,b%maxRowLen) for b in target]
    cost = min([abs(m-y-2*dy)+abs(n-x-2*dx) for (m,n) in target])
    return cost

def solve_greedy1(numNodeTotal = None, numNodesGenPre = None, numNodesFringe = None, \
              numNodesExplored = None, runTime = None):
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    tic = time.clock()
        
    openQue = [(ddata, "", px, py, 0)]
    
    visited = set([ddata])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))

    lmaxRowLen = maxRowLen
    while openQue:
        openQue = sorted(openQue, key =lambda ele: ele[4])
        cur, csol, x, y, c= openQue.pop(0)

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lmaxRowLen + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and checkDeadlock(x, y, dx, dy, temp):
                    nodesTotal += 1
                    if temp not in visited:
                        visited.add(temp)
                        nodesExpl = len(visited)
                        if is_solved(temp):
                            toc = time.clock()
                            print csol + di[2]
                            nodesRem = len(openQue)
                            printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                            return True
                        newc = calcost1(x, y, dx, dy, temp)
                        openQue.append((temp, csol + di[2], x+dx, y+dy, newc))
                    else:
                        nodesPrev += 1    
            else:
                if sdata[(y+dy) * lmaxRowLen + x+dx] == '#' or \
                   temp[(y+dy) * lmaxRowLen + x+dx] != ' ':
                    continue
                nodesTotal += 1
                data2 = array("c", temp)
                data2[y * lmaxRowLen + x] = ' '
                data2[(y+dy) * lmaxRowLen + x+dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_solved(temp):
                        nodesRem = len(openQue)
                        toc = time.clock()
                        print csol + di[2]
                        printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                        return True
                    openQue.append((temp, csol + di[2], x+dx, y+dy, c))
                else:
                    nodesPrev += 1    

    toc = time.clock()
    print "No solution"
    printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
    return False

def solve_aStar1(numNodeTotal = None, numNodesGenPre = None, numNodesFringe = None, \
              numNodesExplored = None, runTime = None):
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    tic = time.clock()
        
    openQue = [(ddata, "", px, py, 0)]
    
    visited = set([ddata])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))

    lmaxRowLen = maxRowLen
    while openQue:
        openQue = sorted(openQue, key =lambda ele: ele[4])
        cur, csol, x, y, c= openQue.pop(0)

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lmaxRowLen + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and checkDeadlock(x, y, dx, dy, temp):
                    nodesTotal += 1
                    if temp not in visited:
                        visited.add(temp)
                        nodesExpl = len(visited)
                        if is_solved(temp):
                            toc = time.clock()
                            print csol + di[2]
                            nodesRem = len(openQue)
                            printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                            return True
                        newc = calcost1(x, y, dx, dy, temp)
                        openQue.append((temp, csol + di[2], x+dx, y+dy, newc+len(csol)+1))
                    else:
                        nodesPrev += 1    
            else:
                if sdata[(y+dy) * lmaxRowLen + x+dx] == '#' or \
                   temp[(y+dy) * lmaxRowLen + x+dx] != ' ':
                    continue
                nodesTotal += 1
                data2 = array("c", temp)
                data2[y * lmaxRowLen + x] = ' '
                data2[(y+dy) * lmaxRowLen + x+dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_solved(temp):
                        nodesRem = len(openQue)
                        toc = time.clock()
                        print csol + di[2]
                        printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                        return True
                    openQue.append((temp, csol + di[2], x+dx, y+dy, c))
                else:
                    nodesPrev += 1    

    toc = time.clock()
    print "No solution"
    printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
    return False

def calcost2(x, y, dx, dy, temp):
    target = []
    for i, ltr in enumerate(sdata):
        if ltr =='.' and temp[i] != '*':
            target.append(i)
    target = [(b/maxRowLen,b%maxRowLen) for b in target]
    cost = min([abs(m-y-dy)+abs(n-x-dx) for (m,n) in target])
    return cost

def solve_greedy2(numNodeTotal = None, numNodesGenPre = None, numNodesFringe = None, \
              numNodesExplored = None, runTime = None):
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    tic = time.clock()
        
    openQue = [(ddata, "", px, py, 0)]
    
    visited = set([ddata])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))

    lmaxRowLen = maxRowLen
    while openQue:
        openQue = sorted(openQue, key =lambda ele: ele[4])
        cur, csol, x, y, c= openQue.pop(0)

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lmaxRowLen + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and checkDeadlock(x, y, dx, dy, temp):
                    nodesTotal += 1
                    if temp not in visited:
                        visited.add(temp)
                        nodesExpl = len(visited)
                        if is_solved(temp):
                            toc = time.clock()
                            print csol + di[2]
                            nodesRem = len(openQue)
                            printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                            return True
                        newc = calcost2(x, y, dx, dy, temp)
                        openQue.append((temp, csol + di[2], x+dx, y+dy, newc))
                    else:
                        nodesPrev += 1    
            else:
                if sdata[(y+dy) * lmaxRowLen + x+dx] == '#' or \
                   temp[(y+dy) * lmaxRowLen + x+dx] != ' ':
                    continue
                nodesTotal += 1
                data2 = array("c", temp)
                data2[y * lmaxRowLen + x] = ' '
                data2[(y+dy) * lmaxRowLen + x+dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_solved(temp):
                        nodesRem = len(openQue)
                        toc = time.clock()
                        print csol + di[2]
                        printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                        return True
                    newc = calcost2(x, y, dx, dy, temp)
                    openQue.append((temp, csol + di[2], x+dx, y+dy, newc))
                else:
                    nodesPrev += 1    

    toc = time.clock()
    print "No solution"
    printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
    return False

def solve_aStar2(numNodeTotal = None, numNodesGenPre = None, numNodesFringe = None, \
              numNodesExplored = None, runTime = None):
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    tic = time.clock()
        
    openQue = [(ddata, "", px, py, 0)]
    
    visited = set([ddata])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))

    lmaxRowLen = maxRowLen
    while openQue:
        openQue = sorted(openQue, key =lambda ele: ele[4])
        cur, csol, x, y, c= openQue.pop(0)

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lmaxRowLen + x+dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and checkDeadlock(x, y, dx, dy, temp):
                    nodesTotal += 1
                    if temp not in visited:
                        visited.add(temp)
                        nodesExpl = len(visited)
                        if is_solved(temp):
                            toc = time.clock()
                            print csol + di[2]
                            nodesRem = len(openQue)
                            printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                            return True
                        newc = calcost2(x, y, dx, dy, temp)
                        openQue.append((temp, csol + di[2], x+dx, y+dy, newc+len(csol)+1))
                    else:
                        nodesPrev += 1    
            else:
                if sdata[(y+dy) * lmaxRowLen + x+dx] == '#' or \
                   temp[(y+dy) * lmaxRowLen + x+dx] != ' ':
                    continue
                nodesTotal += 1
                data2 = array("c", temp)
                data2[y * lmaxRowLen + x] = ' '
                data2[(y+dy) * lmaxRowLen + x+dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_solved(temp):
                        nodesRem = len(openQue)
                        toc = time.clock()
                        print csol + di[2]
                        printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
                        return True
                    newc = calcost2(x, y, dx, dy, temp)
                    openQue.append((temp, csol + di[2], x+dx, y+dy, newc+len(csol)+1))
                else:
                    nodesPrev += 1    

    toc = time.clock()
    print "No solution"
    printstats([numNodeTotal, numNodesGenPre, numNodesFringe, numNodesExplored, runTime], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl,round(toc-tic,2)])
    return False
  
if __name__ == '__main__':
    main(sys.argv[1:])
