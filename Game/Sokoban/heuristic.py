def HF_1(state_data, gole):
    box = []
    cost = 0
    for i in xrange(len(state_data)):
        if state_data[i] == '*':
            box.append(i)
    for i in xrange(len(box)):
        onelist = []
        for j in xrange(len(gole)):
            onelist.append(abs(box[i] - gole[j]))
        cost += min(onelist)
    cost = cost/len(box)
    return cost
# manhatton distance from box to the goal, average distance
            
def HF_2(x, y, l_max_rowlen, gole):
    cost = 0
    p = y*l_max_rowlen + x
    for i in xrange(len(gole)):
        cost += abs(p - gole[i])
    cost = cost/len(gole)
    return cost
# average manhatton distance from box to the


def HF_3(state_data, gole, csol):
    box = []
    cost = 0
    for i in xrange(len(state_data)):
        if state_data[i] == '*':
            box.append(i)
    for i in xrange(len(box)):
        onelist = []
        for j in xrange(len(gole)):
            onelist.append(abs(box[i] - gole[j]))
        cost += min(onelist)
    cost = cost/len(box) + len(csol)
    return cost
# manhatton distance from box to the goal, average distance
            
def HF_4(x, y, l_max_rowlen, gole, csol):
    cost = 0
    p = y*l_max_rowlen + x
    for i in xrange(len(gole)):
        cost += abs(p - gole[i])
    cost = cost/len(gole) + len(csol)
    return cost
# average manhatton distance from box to the
