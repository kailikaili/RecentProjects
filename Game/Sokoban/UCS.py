# This is used for Uniformed Cost search

import sys
import os
import time
from array import array
from collections import deque
from common_function import *


def Solve_UCS(puzzle, max_rowlen, line_num, wall_data, state_data, px, py, \
              nodesTotal_flag = None, nodesPrev_flag = None, nodesRem_flag = None, \
               nodesExpl_flag = None, runTime_flag = None):
    nodesTotal = 1
    nodesPrev = 0
    nodesRem = 0
    nodesExpl = 0
    start_time = time.clock()
    open_List = [(state_data, "", px, py, 0)]
    # for each node, we record the state_data, a action list and person's cordinate
    visited = set([state_data])
    dirs = ((0, -1, 'u'), ( 1, 0, 'r'),
            (0,  1, 'd'), (-1, 0, 'l'))
    l_max_rowlen = max_rowlen
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
                        visited.add(temp)
                        nodeExpl = len(visited)
                        if is_Solved(temp, wall_data):
                            end_time = time.clock()
                            print "The Action Sequence --->  " + str(csol + di[2].upper())
                            nodesRem = len(open_List)
                            print_Stats([nodesTotal_flag, nodesPrev_flag, nodesRem_flag, nodesExpl_flag, runTime_flag], \
                                       [nodesTotal, nodesPrev, nodesRem, nodesExpl, round(end_time - start_time, 4)])
                            return True
                        open_List.append((temp, csol + di[2].upper(), x+dx, y+dy, c+2))
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
                    open_List.append((temp, csol + di[2], x + dx, y + dy, c+1))
                else:
                    nodesPrev += 1

    print  "Sorry, No Solution :( "
    end_time = time.clock()
    print_Stats([nodesTotal_flag, nodesPrev_flag, nodesRem_flag, nodesExpl_flag, runTime_flag], \
           [nodesTotal, nodesPrev, nodesRem, nodesExpl, round(end_time - start_time, 4)])
    return False
    


def UCS(game_file):
    (puzzle, max_rowlen, line_num, wall_data, state_data, px, py) = Initialization(game_file)
    Solve_UCS(puzzle, max_rowlen, line_num, wall_data, state_data, px, py, 1, 1, 1, 1, 1)


