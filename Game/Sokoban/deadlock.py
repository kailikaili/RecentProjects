# this file is used to check the Deadlock Situation to gain some extra points

def deadlock(x, y, dx, dy, puzzle, wall_data, l_max_rowlen, line_num):
    #pass
    ddx = int(not(dx))
    ddy = int(not(dy))
    dirs = ((ddx,ddy),(-ddx,-ddy))
    c = 0
    if wall_data[(y+3*dy) * l_max_rowlen + x+3*dx] == '#' or \
        puzzle[(y+3*dy) * l_max_rowlen + x+3*dx] != ' ':
        for di in dirs:
            ddx, ddy = di[0], di[1]
            if wall_data[(y+2*dy+ddy) * l_max_rowlen + x+2*dx+ddx] =='#' or \
                puzzle[(y+2*dy+ddy) * l_max_rowlen + x+2*dx+ddx] != ' ':
                c += 1
    #if sdata[(y+2*dy) * maxRowLen + x+2*dx]
     
    if c:
        return False
    #no deadlock
    return True
    '''
    else:
        column = ""
        line = ""
        gole_column = ""
        gole_line = ""
        for i in xrange(l_max_rowlen):
            if puzzle[(y+3*dy) * l_max_rowlen +i] == '*':
                line += '#'
            elif wall_data[(y+3*dy) * l_max_rowlen + i] == '.':
                line += ' '
            else:
                line += wall_data[(y+3*dy) * l_max_rowlen + i]
            gole_line += wall_data[(y+2*dy) * l_max_rowlen + i]
        for i in xrange(line_num):
            if puzzle[i*l_max_rowlen + x + 3*dx] == '*':
                column += '#'
            elif wall_data[i*l_max_rowlen + x + 3*dx] == '.':
                column += ' '
            else:
                line += wall_data[i*l_max_rowlen + x + 3*dx]
            gole_column += wall_data[i*l_max_rowlen + x + 2*dx]

        column.strip(' ')
        line.strip(' ')

        if (" " in column or "." in gole_column) and (" " in line or "." in gole_line):
            return True
        else:
            return False
    '''
            

