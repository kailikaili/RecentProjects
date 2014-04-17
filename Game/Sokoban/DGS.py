# This is used for Heuristic Greedy search

import sys
import os
import time
from array import array
from collections import deque
from common_function import *
from heuristic import HF_1, HF_2
from deadlock import deadlock
        

def Solve_GS(H_flag, puzzle, max_rowlen, line_num, wall_data, state_data, px, py, \
              nodesTotal_flag = None, nodesPrev_flag = None, nodesRem_flag = None, \
               nodesExpl_flag = None, runTime_flag = None):
    nodesTotal = 0
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    start_time = time.clock()
    l_max_rowlen = max_rowlen
    H_flag = int(H_flag)
    gole = []
    for i in xrange(len(wall_data)):
        if wall_data[i] == '.':
            gole.append(i)
    cost = 0       
    if H_flag == 1:
        cost = HF_1(state_data, gole)
    elif H_flag == 2:
        cost = HF_2(px, py, l_max_rowlen, gole)
    else:
        print "Please input a correct choice of Heuristic Function: 1 for HF_1 ; 2 for HF_2"

    open_List = [(state_data, "", px, py, cost)]
        
    # for each node, we record the state_data, a action list and person's cordinate
    visited = set([state_data])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))
    while open_List:
        open_List = sorted(open_List, key = lambda ele: ele[4])
        cur, csol, x, y, c = open_List.pop(0)
        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y + dy) * l_max_rowlen + x + dx] == '*':
                temp = Push(x, y, dx, dy, temp, wall_data, max_rowlen)
                if temp:
                    nodesTotal += 1
                    if temp not in visited:
                        if deadlock(x, y, dx, dy, temp, wall_data, l_max_rowlen, line_num):
                            visited.add(temp)
                            nodeExpl = len(visited)
                            if is_Solved(temp, wall_data):
                                end_time = time.clock()
                                print "The Action Sequence --->  " + str(csol + di[2].upper())
                                nodesRem = len(open_List)
                                print_Stats([nodesTotal_flag, nodesPrev_flag, nodesRem_flag, nodesExpl_flag, runTime_flag], \
                                           [nodesTotal, nodesPrev, nodesRem, nodesExpl, round(end_time - start_time, 4)])
                                return True
                            if H_flag == 1:
                                cost = HF_1(state_data, gole)
                            elif H_flag == 2:
                                cost = HF_2(x+dx, y+dy, l_max_rowlen, gole)
                            elif H_flag == 3:
                                cost = (HF_1(state_data, gole)+HF_2(x+dx, y+dy, l_max_rowlen, gole))/2
                            else:
                                print "Please input a correct choice of Heuristic Function: 1 for HF_1 ; 2 for HF_2"
                        
                            open_List.append((temp, csol + di[2].upper(), x+dx, y+dy, cost))
                    else:
                        nodesPrev += 1
            else:
                if wall_data[(y + dy) * l_max_rowlen + x + dx] == '#' or \
                   temp[(y + dy) * l_max_rowlen + x + dx] != ' ':
                    continue
                nodesTotal += 1
                data = array("c", temp)
                data[y * l_max_rowlen + x] = ' '
                data[(y + dy) * l_max_rowlen + x + dx] = '@'
                temp = data.tostring()

                if temp not in visited:
                    visited.add(temp)
                    nodesExpl = len(visited)
                    if is_Solved(temp, wall_data):
                        nodesRem = len(open_List)
                        end_time = time.clock()
                        print "The Action Sequence --->  " + str(csol + di[2].upper())
                        printstats([nodesTotal_flag, nodesPrev_flag, nodesRem_flag, nodesExpl_flag, runTime_flag], \
                                   [nodesTotal, nodesPrev, nodesRem, nodesExpl, round(end_time - start_time, 4)])
                        return True
                    if H_flag == 1:
                        cost = HF_1(state_data, gole)
                    elif H_flag == 2:
                        cost = HF_2(x+dx, y+dy, l_max_rowlen, gole)
                    elif H_flag == 3:
                            cost = (HF_1(state_data, gole)+HF_2(x+dx, y+dy, l_max_rowlen, gole))/2
                    else:
                        print "Please input a correct choice of Heuristic Function: 1 for HF_1 ; 2 for HF_2"
                    open_List.append((temp, csol + di[2], x + dx, y + dy, cost))
                else:
                    nodesPrev += 1

    print  "Sorry, No Solution :( "
    end_time = time.clock()
    print_Stats([nodesTotal_flag, nodesPrev_flag, nodesRem_flag, nodesExpl_flag, runTime_flag], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl, round(end_time - start_time, 4)])
    return False
    


def DGS(game_file, H_flag):
    (puzzle, max_rowlen, line_num, wall_data, state_data, px, py) = Initialization(game_file)
    Solve_GS(H_flag, puzzle, max_rowlen, line_num, wall_data, state_data, px, py, 1, 1, 1, 1, 1)


