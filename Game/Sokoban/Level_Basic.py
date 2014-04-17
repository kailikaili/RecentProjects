# This file is used to generate the state matrix
# contais some common part including Node options

import sys

def Edge(Graph, u):
    Adj_list = []
    i = u[0]
    j = u[1]
    if Graph[i-1][j] != 2:
        Adj_list.append([i-1, j])
    if Graph[i+1][j] != 2:
        Adj_list.append([i+1, j])
    if Graph[i][j-1] != 2:
        Adj_list.append([i, j-1])
    if Graph[i][j+1] != 2:
        Adj_list.append([i, j+1])
    return Adj_list

def DFS_Reset_Graph(Graph, u, visited):
    if u not in visited:
        visited.append(v)
        Graph[u[0]][u[1]] = 0
        Adj_list = Edge(Graph, u)
        for v in Adj_list:
            if v not in visited:
                DFS_Reset_Graph(Graph, v, visited)
    return Graph


def Reset_Graph(Graph, People):
    u = People
    visited = []
    Graph = DFS_Reset_Graph(Graph, u, visited)
    return Graph
    

def LEVEL():
   # linecache.clearcache()
    f_in = open(sys.argv[1], 'r')
    lines = f_in.readlines()
    level_length = int(lines[0].strip('\n'))
    Graph = []
    Box = []
    Gole = []
    People = []
    for i in range(0, level_length):
        num_list = []
        for j in range(0, len(lines[i+1])):
            if lines[i+1][j] == ' ':
                num_list.append(1)
            elif lines[i+1][j] == '#':
                num_list.append(2)
            elif lines[i+1][j] == '.':
                num_list.append(1)
                Gole.append([i,j])
            elif lines[i+1][j] == '@':
                num_list.append(1)
                People = [i,j]
            elif lines[i+1][j] == '+':
                num_list.append(1)
            elif lines[i+1][j] == '$':
                num_list.append(1)
                Box.append([i,j])
            elif lines[i+1][j] == '*':
                num_list.append(1)
                Box.append([i,j])
                Gole.append([i,j])
            else:
                num_list.append(1)
        Graph.append(num_list)
    f_in.close()
    return Graph, People, Box, Gole
    # Read in the level.text, generate the graph consisted by symbols
    # generate a Visiting Matrix, corresponding to the Graph position
    # Wall and box equal to 1 and other parts are 0, for initialization
    # Put all source postion[list][index] into source, source is a queue
    


    
