# This is used for common part

import sys
import os
import time
from array import array
from collections import deque

def Initialization(game_file):
    puzzle = []
    max_rowlen = 0
    px = py = 0
    wall_data = ""
    state_data = ""
    #folder_path = (os.getcwd())
    # f_in = open(folder_path + '/gemes/' + game_file, 'r')
    f_in = open(game_file, 'r')
    puzzle = f_in.read().splitlines()
    max_rowlen = max(len(row) for row in puzzle)
    line_num = int(puzzle[0])
    puzzle = puzzle[1:len(puzzle)]

    gen_wall = {' ':' ', '.':'.', '@':' ', '#':'#', '$':' ', '*':'.', '+':'.'}
    gen_state = {' ':' ', '.':' ', '@':'@', '#':' ', '$':'*', '*':'*', '+':'@'}

    for r, row in enumerate(puzzle):
        for c, ch in enumerate(row):
            wall_data = wall_data + gen_wall[ch]
            state_data = state_data + gen_state[ch]
            if ch == '@':
                px = c
                py = r   # record the cordinate of people
        for i in range(len(row), max_rowlen):
            wall_data = wall_data + ' '
            state_data = state_data + ' '
    # to generate a string, wall_data to record the wall and gole, state_data to record box and people
    return puzzle, max_rowlen, line_num, wall_data, state_data, px, py


def Push(x, y, dx, dy, state, wall_data, max_rowlen):
    if wall_data[(y + 2*dy) * max_rowlen + x + 2*dx] == '#'\
       or state[(y + 2*dy) * max_rowlen + x + 2 * dx] != ' ':
        # if the state we what to move to is not wall or it is not space,
        # we do not move
        return None
    # else, we need to push the box
    data = array("c", state)
    data[y * max_rowlen + x] = ' '
    data[(y + dy) * max_rowlen + x + dx] = '@'
    data[(y + 2 * dy) * max_rowlen + x + 2 * dx] = '*'
    # after we pushed the box, we need to change the state string, which is state_data
    return data.tostring()

def is_Solved(temp, wall_data):
    for i in xrange(len(temp)):
        if (wall_data[i] == '.') != (temp[i] == '*'):
            return False
    return True

def print_Stats(flag_List, stat_List):
    print "The number of nodes generated ---> " + str(stat_List[0])
    print "The number of nodes containing states that were generated previously --->  " + str(stat_List[1])
    print "The number of nodes on the fringe when termination occurs --->  " + str(stat_List[2])
    print "The number of nodes on the explored list (if there is one) --->  " + str(stat_List[3])
    print "The actual run time of the algorithm, expressed in actual time units --->  " + str(stat_List[4])



