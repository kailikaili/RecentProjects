# This is the game file contain all the different algorithms

import sys
from common_function import *
from BFS import BFS
from DFS import DFS
from UCS import UCS
from GS import GS
from AS import AS
from DBFS import DBFS
from DDFS import DDFS
from DUCS import DUCS
from DGS import DGS
from DAS import DAS


if __name__ == "__main__":

    game_file = sys.argv[1]
    A_flag = int(sys.argv[2])
    H_flag = int(sys.argv[3])
    D_flag = int(sys.argv[4])
    
    if D_flag == 0:
        if A_flag == 1:
            print "---> BFS"
            BFS(game_file)
        elif A_flag == 2:
            print "---> DFS"
            DFS(game_file)
        elif A_flag == 3:
            print "---> Uniformed Cost Search"
            UCS(game_file)
        elif A_flag == 4:
            print "---> Greedy Search"
            GS(game_file, H_flag)
        elif A_flag == 5:
            print "---> A* Search"
            AS(game_file, H_flag)
        else:
            print "Please input the correct choice for algorithms \n   --->   1 for BFS\n" + \
                  "          2 for DFS\n" + "          3 for Uniformed Cost Search"+\
                  "          4 for Greedy Search\n" + "          5 for A* Search"
    elif D_flag == 1:
        if A_flag == 1:
            print "---> BFS widh Deadlock Checking"
            DBFS(game_file)
        elif A_flag == 2:
            print "---> DFS widh Deadlock Checking"
            DDFS(game_file)
        elif A_flag == 3:
            print "---> Uniformed Cost Search widh Deadlock Checking"
            DUCS(game_file)
        elif A_flag == 4:
            print "---> Greedy Search widh Deadlock Checking"
            DGS(game_file, H_flag)
        elif A_flag == 5:
            print "---> A* Search widh Deadlock Checking"
            DAS(game_file, H_flag)
        else:
            print "Please input the correct choice for algorithms \n   --->   1 for BFS\n" + \
                  "          2 for DFS\n" + "          3 for Uniformed Cost Search"+\
                  "          4 for Greedy Search\n" + "          5 for A* Search"
    else:
        print "Please input the correct choice for Deaclock Checking --->   0 for Don't Use ;  1 for Use "
 
