# Problem5
import os, re, math, random, time, sys

t = {}  # global variable -- parameter t
q = {}  # global variable -- parameter q
sep = re.compile('\s+')

def Load_T(t_file):
    n = {}
    f_t = open(t_file, 'r')
    p = re.compile('(\S+)\s\|\|\|\s(\S+)\s\|\|\|\s(\S+)')
    for line in f_t:
        m = p.match(line.strip('\n'))
        if m:
            e = m.group(1)
            f = m.group(2)
            prob = float(m.group(3))
            if e in t:
                t[e][f] = prob
            else:
                t[e] = {f : prob}
    f_t.close()
def Gen_Q(j, i, l, m):
    if (j, i, l, m) not in q:
        q[j, i, l, m] = 1.0/(l + 1)
    return q[j, i, l, m]
    
    
if __name__ == "__main__":
    start_time = time.clock()
    Load_T (sys.argv[4])
    S = sys.argv[3] # number of EM iteration times
    f_de = open(sys.argv[1], 'r')
    f_en = open(sys.argv[2], 'r')
    
    for s in range(0, int(S)):
        print str(s)+'th EM iteration.'
        # E-Step
        c = {} # record expectation (count)
        for de_line in f_de:
            de_line= de_line.strip('\n')
            en_line = f_en.readline().strip('\n')
            en_line = 'NULL ' + en_line
            #de_sent = sep.split(de_line)
            de_sent = de_line.split(' ')
            en_sent = sep.split(en_line)
            # print de_sent
            # print en_sent
            m = len(de_sent)
            l = len(en_sent)
            for i in range(0, m):
                f = de_sent[i]
                sum_t = 0
                for j in range(0, l):
                    e = en_sent[j]
                    sum_t = sum_t + Gen_Q(j, i, l, m) * t[e][f]
                for j in range(0, l):
                    e = en_sent[j]
                    delta = Gen_Q(j, i, l, m) * t[e][f]/sum_t
                    if (f, e) in c:
                        c[f, e] = c[f, e] + delta
                    else:
                        c[f, e] = delta
                    if e in c:
                        c[e] = c[e] + delta
                    else:
                        c[e] = delta
                    if (j, i, l, m) in c:
                        c[j, i, l, m] = c[j, i, l, m] + delta
                    else:
                        c[j, i, l, m] = delta
                    if (i, l, m) in c:
                        c[i, l, m] = c[i, l, m] + delta
                    else:
                        c[i, l, m] = delta
        # M-Step: recalculate t
        for e in t:
            for f in t[e]:
                if (f, e) in c:
                    t[e][f] = c[f, e] / c[e]
        for (j, i, l, m) in q:
            q[j, i, l, m] = c[j, i, l, m] / c[i, l, m]
        f_de.seek(0, 0)
        f_en.seek(0, 0)

    # save t into file sys.argv[5]
    f_tw = open(sys.argv[5], 'w')
    for e in t:
        for f in t[e]:
            f_tw.write(e + ' ||| ' + f + ' ||| ' + str(t[e][f]) + '\n')
    f_tw.close()
    # save q into file sys.argv[6]
    f_qw = open(sys.argv[6], 'w')
    for (j, i, l, m) in q:
        f_qw.write(str(j) + ' , ' + str(i) + ' , ' + str(l) + ' , ' + str(m)  + ' ||| ' + str(q[j, i, l, m]) + '\n')
    f_qw.close()

    # generate topest 10 
    f_in = open(sys.argv[7], 'r')
    f_out = open(sys.argv[8], 'w')
    for line in f_in:
        e = line.strip('\n')
        f_list = []
        if e not in t:
            continue
        for f in t[e]:
            f_list.append((-t[e][f], f))
            f_list.sort()
            f_list = f_list[0:10]
        out_list = e + '\n['
        for (p, f) in f_list:
            out_list = out_list + '(\'' + f + '\', ' + str(-p) + '), '
        out_list = out_list[0: len(out_list)-2]
        out_list = out_list + ']\n'
        f_out.write(out_list)
    f_in.close()
    f_out.close()

    # generate alignments
    f_align = open(sys.argv[9], 'w')
    f_de.seek(0, 0)
    f_en.seek(0, 0)
    count = 0
    for line_de in f_de:
        line_de = line_de.strip('\n')
        line_en = f_en.readline().strip('\n')
        line_ori = line_en
        line_en = 'NULL ' + line_en
        de_sent = sep.split(line_de)
        en_sent = sep.split(line_en)
        m = len(de_sent)
        l = len(en_sent)
        f_align.write(line_ori + '\n')
        f_align.write(line_de + '\n')
        f_align.write('[')
        
        for i in range(0, m):
            f = de_sent[i]
            idx = 0
            maxt = 0
            for j in range(0, l):
                e = en_sent[j]
                prob = q[j, i, l, m] * t[e][f]
                if prob > maxt:
                    maxt = prob
                    idx = j   ### j + 1 or j - 1
            f_align.write(str(idx) + ' ')
        f_align.write(']\n\n')
        count = count + 1
        if count == 20:
            break
    f_align.close()
    f_de.close()
    f_en.close()
    end_time = time.clock()
    print 'Total Processing Time:' + str((end_time - start_time)) + ' sec'
