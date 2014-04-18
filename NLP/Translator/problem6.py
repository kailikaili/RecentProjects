# Problem6

import sys, re, math, random, time

t = {}
q = {}
fset = set()
sep = re.compile('\s+')

def Load_P(t_file, q_file):
    f_t = open(t_file)
    f_q = open(q_file)
    p_t = re.compile('(\S+)\s\|\|\|\s(\S+)\s\|\|\|\s(\S+)')
    p_q = re.compile('(\d+)\s\,\s(\d+)\s\,\s(\d+)\s\,\s(\d+)\s\|\|\|\s(\S+)')
    for line in f_t:
        match = p_t.match(line.strip('\n'))
        if match:
            e = match.group(1)
            f = match.group(2)
            prob = float(match.group(3))
            if e in t:
                t[e][f] = prob
            else:
                t[e] = {f : prob}
            fset.add(f)
    f_t.close()
    for line in f_q:
        match = p_q.match(line.strip('\n'))
        if match:
            j = int(match.group(1))
            i = int(match.group(2))
            l = int(match.group(3))
            m = int(match.group(4))
            prob = float(match.group(5))
            q[j, i, l, m] = prob
    f_q.close()

if __name__ == "__main__":
    start_time = time.clock()
    Load_P(sys.argv[3], sys.argv[4])
    f_de = open(sys.argv[1], 'r')
    f_en = open(sys.argv[2], 'r')
    can_list = []
    cant_list = []
    for line in f_en:
        line = line.strip('\n')
        can_list.append(line)
        line = 'NULL ' + line
        en_sent = sep.split(line)
        cant_list.append(en_sent)
    f_en.close()
    f_tran = open(sys.argv[5], 'w')
    for line in f_de:
        line = line.strip('\n')
        f_sent = sep.split(line)
        m = len(f_sent)
        cand = 0
        prob = -10000000000
        for xx in range(0, len(cant_list)):
            e_sent = cant_list[xx]
            l = len(e_sent)
            sxx = 0
            for i in range(0, m):
                f = f_sent[i]
                if f not in fset:
                    continue
                maxt = 0
                for j in range(0, l):
                    e = e_sent[j]
                    if e in t and f in t[e] and (j, i, l, m) in q:
                        tt = q[j, i, l, m] * t[e][f]
                        if tt > maxt:
                            maxt = tt
                if maxt == 0:
                    maxt = -10000000000
                else:
                    maxt = math.log(maxt)
                sxx = sxx + maxt
            if sxx > prob:
                prob = sxx
                cand = xx
        f_tran.write(can_list[cand] + '\n')
    f_de.close()
    f_tran.close()
    end_time = time.clock()
    print 'Processing Time: ' + str(end_time - start_time) + ' sec'
    
    
