# -*- coding: UTF-8 -*-
# This code is used to judege the cut-point and cut-part
# Use DFS to judge, and only need linear time
from Level_Basic import Edge

visited = []
def Judge_Cut_DFS(Graph, u, visited, deep, parent):
    if u not in visited:
        Adj_list = Edge(Graph, u)
        for v in Adj_list:
            if v not in visited:
                visited.append(v)
                deep[v] = deep[u]+1
                parent[v] = u
                DFS(Graph, v, visited, deep, parent)
    return visited, deep, parent

def Low_Digit(Graph, visited, deep, parent):
    low_digit = deep
    for i in range(0, len(visited)):
        i = i+1
        u = visited.pop()
        visited.insert(0, u)
        Adj_list = Edge(Graph, u)
        u_parent = parent[str(u)]
        if u_parent != 'root':
            Adj_list.remove(u_parent)
        print low_digit
        for v in Adj_list:
            if low_digit[str(v)] < low_digit[str(u)]:
                low_digit[str(u)] = low_digit[str(v)]
    return low_digit

def Cut_Part(cut_points, visited, parent):
    cut_part = {}
    flag = 1
    for u in visited:
        cut_part[u] = 0
    while len(visited) > 0:
        u = visited.pop()
        u = str(u)
        cut_part[u].append(flag)
        if u in cut_points:
            flag = flag + 1
        elif parent[u] in cut_points:
            flag = flag + 1
            cut_part[parent[u]].append(flag)
    return cut_part
          

def Judge_Cut(Graph, u):
    visited = []
    deep = {}
    low_digit = {}
    parent = {}
    deep[str(u)] = 0
    parent[str(u)] = 'root'
    visited.append(u)
    (visited, deep, parent) = Judge_Cut_DFS(Graph, u, visited, deep, parent)
    # based on visited list and deep, parent information, we begin to caculate the
    low_digit = Low_Digit(Graph, visited, deep, parent)
    cut_points = []  # cut_points里面的坐标点是以string的形式储存的
    for e in low_digit:
        if low_figit[e] >= deep[e]:
            cut_points.append(e)
    cut_part = Cut_Part(Cut, visited, parent)
    return cut_points, cut_part
        
    

    
    
    
    
        
            
