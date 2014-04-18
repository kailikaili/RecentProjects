# Problem4
import os, re, math, random, time, sys

t = {}  # global variable -- parameter t
sep = re.compile('\s+')

def Gen_T(de_in, en_in):
    n = {}
    f_de = open(de_in, 'r')
    f_en = open(en_in, 'r')
    for de_line in f_de:
        de_line = de_line.strip('\n')
        en_line = 'NULL ' + f_en.readline().strip('\n')
        de_sent = sep.split(de_line)
        en_sent = sep.split(en_line)
        de_set = set(de_sent)

        for e in en_sent:
            if e not in n:
                n[e] = set(de_set)
            else:
                n[e].update(de_set)
            for f in de_set:
                if e in t:
                    t[e][f] = 1.0
                else:
                    t[e] = {f:1.0}
    f_de.close()
    f_en.close()
    for e in t:
        for f in t[e]:
            t[e][f] = t[e][f]/len(n[e])
    t['NULL']['_RARE_'] = 1.0/len(n['NULL'])
        
    
if __name__ == "__main__":
    start_time = time.clock()
    Gen_T (sys.argv[1], sys.argv[2])
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
            for f in de_sent:
                sum_t = 0
                for e in en_sent:
                    sum_t = sum_t + t[e][f]
                for e in en_sent:
                    delta = t[e][f]/sum_t
                    if (f, e) in c:
                        c[f, e] = c[f, e] + delta
                    else:
                        c[f, e] = delta
                    if e in c:
                        c[e] = c[e] + delta
                    else:
                        c[e] = delta
        # M-Step: recalculate t
        for e in t:
            for f in t[e]:
                if (f, e) in c:
                    t[e][f] = c[f, e] / c[e]
        f_de.seek(0, 0)
        f_en.seek(0, 0)

    # save t into file sys.argv[4]
    f_tw = open(sys.argv[4], 'w')
    for e in t:
        for f in t[e]:
            f_tw.write(e + ' ||| ' + f + ' ||| ' + str(t[e][f]) + '\n')
    f_tw.close()

    # generate topest 10 
    f_in = open(sys.argv[5], 'r')
    f_out = open(sys.argv[6], 'w')
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
    f_align = open(sys.argv[7], 'w')
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
        f_align.write(line_ori + '\n')
        f_align.write(line_de + '\n')
        f_align.write('[')
        for f in de_sent:
            idx = 0
            maxt = 0
            for j in range(0, len(en_sent)):
                e = en_sent[j]
                prob = t[e][f]
                if prob > maxt:
                    maxt = prob
                    idx = j # j - 1 or j + 1
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
            
            
