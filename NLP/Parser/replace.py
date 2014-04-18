import sys
import re

if __name__ == '__main__':
    f_oricount = open(sys.argv[1], 'r')
    f_oritrain = open(sys.argv[2], 'r')
    f_newtrain = open(sys.argv[3], 'w')

    count_dic = {}
    pattern = re.compile('(\d+)\sUNARYRULE\s\S+\s(\S+)')
    for line in f_oricount:
        match = pattern.match(line)
        if match:
            w = match.group(2)
            freq = int(match.group(1))
            if count_dic.has_key(w):
                count_dic[w] = count_dic[w] + freq
            else:
                count_dic[w] = freq
    f_oricount.close()
    rare_list = []
    for w in count_dic:
        if count_dic[w] < 5:
            rare_list.append(w)

    text = f_oritrain.read()
    for w in rare_list:
        if "\/" in w:
            p =re.compile('(S+)\\/(S+)')
            match = p.match(w)
            if match:
                w = str(match.group(1) + '\\\/' + match.group(2))
        text = text.replace('\"'+ w +'\"]', '\"_RARE_\"]')

    f_newtrain.write(text)
    f_oritrain.close()
    f_newtrain.close()

    
