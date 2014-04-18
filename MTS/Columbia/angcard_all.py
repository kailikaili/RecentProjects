#-*- coding=utf-8 -*-
from flask import Flask, request, render_template
from flask.json import jsonify
from flask.views import MethodView
import os, re, sys, urllib, urllib2, json, subprocess, time, math

reload(sys)
sys.setdefaultencoding('utf-8')



app = Flask(__name__)
app.secret_key = 'adafdasdfdasfads'

@app.route('/')
def index():
    return render_template('admin_index.html')



class Google(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()
        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('csent-test-common.seg','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()

        # 爬取过程
        query = str(source_sentence)
        url = 'http://translate.google.com/translate_a/t?client=t&sl=zh-CN&tl=en&hl=zh-CN&sc=2&ie=UTF-8&oe=UTF-8&prev=btn&ssel=0&tsel=0&q='+ urllib.quote(query)
        headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36', 'Host':'translate.google.com', 'Accept-Language':'zh-CN,zh;q=0.8', 'Accept': '*/*'}
        req = urllib2.Request(url, None, headers)
        html = urllib2.urlopen(req).read()

        x = html.split('"],[')
        sent_num = len(query.strip('\n').strip(' ').split('。')) - 1
        text = ''
        if sent_num >= 1:
            p1 = re.compile("\[\[\[\"(.*?)\"\,\"")
            p2 = re.compile("\"(.*?)\"\,\"")
            m1 = p1.match(x[0])
            if m1:
                text += m1.group(1)
            for i in range(1, sent_num):
                m2 = p2.match(x[i])
                if m2:
                    text += m2.group(1)
        elif sent_num < 1:
            p = re.compile("\[\[\[\"(.*?)\"\,\"")
            m = p.match(html)
            if m:
                text = m.group(1)
            
            
        text = str(text.replace('\\\"','\"')).strip(' ').strip('\n').strip('\r')

        # 返回爬虫结果
        translate_result = text  
        return jsonify(success=True, translate_result=translate_result)


class Bing(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()
        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('csent-test-common.seg','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()
        # 爬取过程
        query = str(source_sentence)
        query = query.replace('\"','\\"')
        #query = query.decode('gbk').encode('utf-8')
        url = 'http://api.microsofttranslator.com/v2/ajax.svc/TranslateArray2?appId=%22T7BT5po4x9m-kiptAu2IZSB5WLfps4d3lyY7EXD8vre0*%22&texts=[%22'\
          + urllib.quote(query) +'%22]&from=%22zh-chs%22&to=%22en%22&oncomplete=_mstc9&onerror=_mste9&loc=en&ctr=&'
        headers = { 'User-Agent' : 'Mozilla/5.0', 'Host':'www.microsofttranslator.com', 'Accept-Language':'zh,en-us;q=0.7,en;q=0.3', 'Accept': '*/*'}
        req = urllib2.Request(url, None, headers)
        html = urllib2.urlopen(req).read()[11:-3]
        trans_res = json.loads(html)
        translate_result = trans_res['TranslatedText'].strip('% ')
        # 返回爬虫结果         
        return jsonify(success=True, translate_result=translate_result)


class Youdao(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()
        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('csent-test-common.seg','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()
        query = str(source_sentence)
        # 爬取过程
        query = query.strip('\n').replace('\」','\\"').replace('\「','\\"').replace('\"','\\"')
        url = "http://fanyi.youdao.com/openapi.do?keyfrom=columbianlpgroup&\
key=601999569&type=data&doctype=jsonp&callback=show&version=1.1&q=" + urllib.quote(query)
        page = urllib2.urlopen(url, None, 20)
        ff = page.read()
        f = ff[5:-2]
        trans_res = json.loads(f)
        outline = trans_res["translation"][0]
        text = outline.encode('utf-8').strip(' ').strip('\n').strip('\r')
        
        # 返回爬虫结果
        translate_result = text
        return jsonify(success=True, translate_result=translate_result)    


class NRC(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()

        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('./files/nrc','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()

        translate_result = source_sentence  # 这里需要改成自己的翻译结果
        return jsonify(success=True, translate_result=translate_result)  


class PBT(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()

        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('./files/pbt','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()

        translate_result = source_sentence  # 这里需要改成自己的翻译结果
        return jsonify(success=True, translate_result=translate_result)  


class AML(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()

        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('./files/aml','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()

        translate_result = source_sentence  # 这里需要改成自己的翻译结果
        return jsonify(success=True, translate_result=translate_result)                                    


class JX(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()

        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('./files/jx','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()

        translate_result = source_sentence  # 这里需要改成自己的翻译结果
        return jsonify(success=True, translate_result=translate_result)  

class SH(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()

        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('./files/sh','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()

        translate_result = source_sentence  # 这里需要改成自己的翻译结果
        return jsonify(success=True, translate_result=translate_result)  


class SRI(MethodView):
    def get(self):
        source_sentence = request.args.get('source_sentence', '').strip()

        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('./files/sri','r').readlines()
            index = int(source_sentence)
            source_sentence = f_in[index - 1].strip()

        translate_result = source_sentence  # 这里需要改成自己的翻译结果
        return jsonify(success=True, translate_result=translate_result)


class Best(MethodView):
    # calculate best for online engines
    def get(self):
        start_time = time.clock()
        source_sentence = request.args.get('source_sentence', '').strip()

        # 获取翻译引擎的翻译结果
        gsent = request.args.get('google', '').strip()
        bsent = request.args.get('bing', '').strip()
        ysent = request.args.get('youdao', '').strip()

        f_g = open('./files/google.file','w')
        f_g.writelines(gsent + ' (1)\n')
        f_g.close()
        f_b = open('./files/bing.file','w')
        f_b.writelines(bsent + ' (1)\n')
        f_b.close()
        f_y = open('./files/youdao.file','w')
        f_y.writelines(ysent + ' (1)\n')
        f_y.close()

        # 计算TERP分数
        print 'Begin to Calculate the score:'
        engine_list = ['google.file','bing.file','youdao.file']
        score_g = [0, 0, 0]
        score_b = [0, 0, 0]
        score_y = [0, 0, 0]
        dic = [score_g, score_b, score_y]
        pattern = re.compile('(\d+)\s+\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|\s+(\S+)')
        for i in range(0, 3):
            f_hyp = './files/' + engine_list[i]
            for j in range(i+1, 3):
                f_ref = './files/' + engine_list[j]
                subprocess.call('/local/kz2203/perfect/terp.v1/bin/terp -r '+\
                                f_ref + ' -h ' + f_hyp +' -n ./files/output -o sum', shell = True)
                ter = open('./files/output.sum','r')
                for line in ter:
                    line = line.strip('\n').strip(' ')
                    m = pattern.match(line)
                    if m:
                        score = m.group(12).strip(' ')
                        score = float(score)/100.00
                        print 'SCORE IS ' + str(score)
                        dic[i][j] = str(score)
                        dic[j][i] = str(score)
        # 生成phrase_table
        f_pt = open('./files/phrase_table','w')
        f_pt.writelines('_1_ ||| ' + gsent + ' ||| ' + str(score_g[0]) + ' ' + str(score_g[1]) + ' ' + str(score_g[2]) + ' ||| |||\n')
        f_pt.writelines('_1_ ||| ' + bsent + ' ||| ' + str(score_b[0]) + ' ' + str(score_b[1]) + ' ' + str(score_b[2]) + ' ||| |||\n')
        f_pt.writelines('_1_ ||| ' + ysent + ' ||| ' + str(score_y[0]) + ' ' + str(score_y[1]) + ' ' + str(score_y[2]) + ' ||| |||\n')
        f_pt.close()
        # 利用online.ini翻译， 将翻译出来的结果保存
        # 生成input文件 _1_
        f_in = open('./files/input.file','w')
        f_in.writelines('_1_\n')
        f_in.close()

        subprocess.call('/local/kz2203/moses/mosesdecoder/bin/moses -f online.ini < /local/kz2203/demo/Columbia/files/input.file > /local/kz2203/demo/Columbia/files/translated.file',shell = True)
        f_result = open('./files/translated.file','r')
        result = f_result.readline().strip('\n')
        f_result.close()

        print result + '**************'
        
        # 删除中间生成的文件
        subprocess.call('rm -f ./files/google.file', shell = True)
        subprocess.call('rm -f ./files/bing.file', shell = True)
        subprocess.call('rm -f ./files/youdao.file', shell = True)
        subprocess.call('rm -f ./files/output.sum', shell = True)
        #subprocess.call('rm -f ./files/input.file', shell = True)
        #subprocess.call('rm -f ./files/phrase_table', shell = True)
        #subprocess.call('rm -f ./files/translated.file', shell = True)
        
        translate_result = result  # 这里需要改成自己的翻译结果
        end_time = time.clock()
        print 'Total time used is ' + str(end_time - start_time)
        return jsonify(success=True, translate_result=translate_result)

class Best2(MethodView):
    # calculate best for offline engines
    def get(self):
        start_time = time.clock()
        source_sentence = request.args.get('source_sentence', '').strip()
        source_sentence = str(source_sentence)
        num = re.compile('\d+')
        m = num.match(source_sentence)
        if m:
            f_in = open('csent-test-common.seg','r').readlines()
            sentid = int(source_sentence)
            source_sentence = f_in[sentid - 1].strip()
        f_in
        

        # 获取翻译引擎的翻译结果
        nrcsent = request.args.get('nrc', '').strip()
        pbtsent = request.args.get('pbt', '').strip()
        amlsent = request.args.get('aml', '').strip()
        jxsent = request.args.get('jx', '').strip()
        shsent = request.args.get('sh', '').strip()
        srisent = request.args.get('sri', '').strip()

        # 计算TERP分数
        print 'Start Calculating TERP Score'
        f_in = open('./files/nrc.file','w')
        f_in.writelines(nrcsent + ' (1)\n')
        f_in.close()
        f_in = open('./files/pbt.file','w')
        f_in.writelines(pbtsent + ' (1)\n')
        f_in.close()
        f_in = open('./files/aml.file','w')
        f_in.writelines(amlsent + ' (1)\n')
        f_in.close()
        f_in = open('./files/jx.file','w')
        f_in.writelines(jxsent + ' (1)\n')
        f_in.close()
        f_in = open('./files/sh.file','w')
        f_in.writelines(shsent + ' (1)\n')
        f_in.close()
        f_in = open('./files/sri.file','w')
        f_in.writelines(srisent + ' (1)\n')
        f_in.close()

        engine_list = ['nrc.file','pbt.file','aml.file','jx.file','sh.file','sri.file']
        score_nrc = [0, 0, 0, 0, 0, 0]
        score_pbt = [0, 0, 0, 0, 0, 0]
        score_aml = [0, 0, 0, 0, 0, 0]
        score_jx = [0, 0, 0, 0, 0, 0]
        score_sh = [0, 0, 0, 0, 0, 0]
        score_sri = [0, 0, 0, 0, 0, 0]
        dic = [score_nrc, score_pbt, score_aml, score_jx, score_sh, score_sri]
        pattern = re.compile('(\d+)\s+\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|\s+(\S+)')
        for i in range(0, 6):
            f_hyp = './files/' + engine_list[i]
            for j in range(i+1, 6):
                f_ref = './files/' + engine_list[j]
                subprocess.call('/local/kz2203/perfect/terp.v1/bin/terp -r '+\
                                f_ref + ' -h ' + f_hyp +' -n ./files/output -o sum', shell = True)
                ter = open('./files/output.sum','r')
                for line in ter:
                    line = line.strip('\n').strip(' ')
                    m = pattern.match(line)
                    if m:
                        score = m.group(12).strip(' ')
                        score = float(score)/100.00
                        print 'SCORE IS ' + str(score)
                        dic[i][j] = str(score)
                        dic[j][i] = str(score)
        Ter_Feature = []
        for i in range(0, 6):
            feature = ''
            for j in range(0, 6):
                feature += str(dic[i][j])
                feature += ' '
            Ter_Feature.append(feature.strip(' '))

        subprocess.call('rm -f ./files/nrc.file', shell = True)
        subprocess.call('rm -f ./files/pbt.file', shell = True)
        subprocess.call('rm -f ./files/aml.file', shell = True)
        subprocess.call('rm -f ./files/jx.file', shell = True)
        subprocess.call('rm -f ./files/sh.file', shell = True)
        subprocess.call('rm -f ./files/sri.file', shell = True)
        subprocess.call('rm -f ./files/output.sum', shell = True)
        
        print 'Completed Ter Feature Calculation!'
        print Ter_Feature


        # 开始计算dependency parser feature
        

        f_in = open('./files/source.file','w')
        f_in.writelines(source_sentence + '\n')
        f_in.close()
        f_in = open('./files/engine.file','w')
        f_in.writelines(nrcsent + '\n')
        f_in.writelines(pbtsent + '\n')
        f_in.writelines(amlsent + '\n')
        f_in.writelines(jxsent + '\n')
        f_in.writelines(shsent + '\n')
        f_in.writelines(srisent + '\n')
        f_in.close()

        file_in = './files/source.file'
        file_out = './files/source_p.file'
        sourceparser = subprocess.Popen('/local/kz2203/perfect/stanford-parser/lexparser.sh '\
                        + file_in + ' > ' + file_out, shell = True)

        file_in = './files/engine.file'
        file_out = './files/engine_p.file'
        engineparser = subprocess.Popen('/local/kz2203/perfect/stanford-parser/lexparser-en.sh '\
                        + file_in + ' > ' + file_out, shell = True)
        p1 = re.compile('\(ROOT')
        p2 = re.compile('(\S+?)\((\S+?)\-\d+\,\s(\S+?)\-\d+\)')
        engineparser.wait()
        f_in = open('./files/engine_p.file','r')
        f_out = open('./files/engine_parser.file','w')
        for line in f_in:
            line = line.strip('\n')
            m2 = p2.match(line)
            if m2:
                f_out.writelines(line +'\n')
            else:
                m1 = p1.match(line)
                if m1:
                    f_out.writelines('\n')
        f_in.close()
        f_out.close()
        sourceparser.wait()
        f_in = open('./files/source_p.file','r')
        f_out = open('./files/source_parser.file','w')
        for line in f_in:
            line = line.strip('\n')
            m2 = p2.match(line)
            if m2:
                f_out.writelines(line +'\n')
            else:
                m1 = p1.match(line)
                if m1:
                    f_out.writelines('\n')
        f_in.close()
        f_out.close()
        subprocess.call('rm -f /local/kz2203/demo/sentence/files/source_p.in', shell = True)
        subprocess.call('rm -f /local/kz2203/demo/sentence/files/engine_p.in', shell = True)
        print 'Completed Parsing'
        

        #开始建立dependency parser feature 的dict
        # 首先需要导入全部的alignement
        f_in = open('./files/nrc.align','r').readlines()
        nrc_align = f_in[sentid].strip('\n').strip(' ')
        f_in = open('./files/pbt.align','r').readlines()
        pbt_align = f_in[sentid].strip('\n').strip(' ')
        f_in = open('./files/aml.align','r').readlines()
        aml_align = f_in[sentid].strip('\n').strip(' ')
        f_in = open('./files/jx.align','r').readlines()
        jx_align = f_in[sentid].strip('\n').strip(' ')
        f_in = open('./files/sh.align','r').readlines()
        sh_align = f_in[sentid].strip('\n').strip(' ')
        f_in = open('./files/sri.align','r').readlines()
        sri_align = f_in[sentid].strip('\n').strip(' ')
        align = [nrc_align, pbt_align, aml_align, jx_align, sh_align, sri_align]

        # 建立源语的denpendency dictionary
        # 貌似不需要打开源文件， 因为每个文件只有一行，针对一个句子 s = open('/local/kz2203/demo/sentence/files/source.in','r').readlines()
        sp = open('./files/source_parser.file','r').readlines()
        s_dic = {}
        pattern = re.compile('(\S+?)\((\S+?)\-(\d+)\,\s(\S+?)\-(\d+)\)')

        for line in sp:
            line = line.strip('\n').strip(' ')
            m = pattern.match(line)
            if m:
                pair = m.group(5) + '-' + m.group(3)
                s_dic[pair] = m.group(1)
        # 建立引擎翻译结果的dependency dictionary
        ep = open('./files/engine_parser.file','r').readlines()
        f_tran = open('./files/transdic.file','w')
        e_dic = [{},{},{},{},{},{}]
        enum = -1
        for line in ep:
            line = line.strip('\n').strip(' ')
            if len(line) == 0:
                enum += 1
                continue
            dic = e_dic[enum]
            m = pattern.match(line)
            if m:
                pair = m.group(5) + '-' + m.group(3)
                dic[pair] = m.group(1)
        # 根据alignment关系，建立所有可能出现的dependency dictionary
        Parser_Feature = []
        for i in range(0, 6):
            f_tran.writelines('ENGINE\n')
            engine = e_dic[i]
            alignment = align[i].strip('\n').split(' ')
            align_dic = {} # 用来存放alignment对儿
            for pair in alignment:
                pair = pair.split('-')
                if str(int(pair[0]) + 1) not in align_dic:
                    align_dic[str(int(pair[0]) + 1)] = [str(int(pair[1]) + 1)]
                else:
                    align_dic[str(int(pair[0]) + 1)].append(str(int(pair[1]) + 1))
            correct = 0
            strict = 0

            trans_dic = {} # 过渡字典，用来存储所有可能出现的pair
            for skey in s_dic:
                pair = skey.split('-')
                if pair[0] in align_dic:
                    term1 = align_dic[pair[0]]
                else: continue
                if pair[1] in align_dic:
                    term2 = align_dic[pair[1]]
                else: continue
                for word1 in term1:
                    for word2 in term2:
                        key = str(word1) + '-' + str(word2)
                        trans_dic[key] = s_dic[skey]
            for tranpair in trans_dic:
                if tranpair in engine:
                    correct += 1
                    f_tran.writelines(tranpair + '\n')
                    if trans_dic[tranpair] == engine[tranpair]:
                        strict += 1

            Parser_Feature.append(str(float(correct)/float(len(s_dic))) + ' ' + str(float(strict)/float(len(s_dic))))
        f_tran.close()
        #subprocess.call('rm -f source_parser.file',shell = True)
        #subprocess.call('rm -f engine_parser.file', shell = True)
        print 'Completed Calaulating Parser Feature'
        print Parser_Feature

        

        # 计算name entity parser feature
        # 运算name entigy
        file_in = './files/source.file'
        file_out = './files/source_ner.file'
        subprocess.call('/local/kz2203/perfect/stanford-ner/ner-chinese.sh ' + file_in + \
                        ' > ' + file_out, shell = True)
        file_in = './files/engine.file'
        file_out = './files/engine_ner.file'
        subprocess.call('/local/kz2203/perfect/stanford-ner/ner4.sh ' + file_in + \
                        ' > ' + file_out, shell = True)
        # 开始建立named entity 的dict
        # 首先需要导入全部的alignement, 上一步已经导入了
        #align = [nrc_align, pbt_align, aml_align, jx_align, sh_align, sri_align]
        sn = open('./files/source_ner.file','r').readlines()
        s_dic = {}
        e_dic = [{},{},{},{},{},{}]

        # build source language's entity dictionary
        sn_token = sn[0].strip('\n').strip(' ').split(' ')
        for t in range(0, len(sn_token)):
            token = sn_token[t].split('/')
            if token[1] != 'O':
                if token[1] == 'GPE':
                    s_dic[str(t)] = 'LOC'
                else:
                    s_dic[str(t)] = token[1]
        en = open('./files/engine_ner.file','r').readlines()
        for j in range(0, 6):
            en_token = en[j].strip('\n').strip(' ').split(' ')
            for t in range(0, len(en_token)):
                token = en_token[t].split('/')
                if token[1] != 'O':
                    if token[1] == 'LOCATION':
                        e_dic[j][str(t)] = 'LOC'
                    elif token[1] == 'ORGANIZATION':
                        e_dic[j][str(t)] = 'ORG'
                    else:
                        e_dic[j][str(t)] = token[1]

        Ner_Feature = []
 
        for j in range(0, 6):
            engine = e_dic[j]
            alignment = align[j].strip('\n').strip(' ').split(' ')
            align1 = {}
            for pair in alignment:
                pair = pair.split('-')
                if pair[0] not in align1:
                    align1[pair[0]] = [pair[1]]
                else:
                    align1[pair[0]].append(pair[1])

            correct = 0

            trans_dic = {}
            for sk in s_dic:
                if sk in align1:
                    for word in align1[sk]:
                        trans_dic[word] = s_dic[sk]

            for word in engine:
                if word in trans_dic:
                    if trans_dic[word] == engine[word]:
                        correct += 1
            Ner_Feature.append(str(float(correct)/float(len(s_dic) + 1)))
        
        subprocess.call('rm -f ./files/source_ner.file', shell = True)
        subprocess.call('rm -f ./files/engine_ner.file', shell = True)

        print 'Completed Calculating Named Entity Feature'
        print Ner_Feature

        print 'Start building phrase table'
        # 生成phrase_table
        f_pt = open('./files/phrase_table','w')
        f_pt.writelines('_1_ ||| ' + nrcsent + ' ||| ' + str(Ter_Feature[0]) + ' ' + str(Parser_Feature[0]) + ' ' + str(Ner_Feature[0]) + ' ||| |||\n')
        f_pt.writelines('_1_ ||| ' + pbtsent + ' ||| ' + str(Ter_Feature[1]) + ' ' + str(Parser_Feature[1]) + ' ' + str(Ner_Feature[1]) +  ' ||| |||\n')
        f_pt.writelines('_1_ ||| ' + amlsent + ' ||| ' + str(Ter_Feature[2]) + ' ' + str(Parser_Feature[2]) + ' ' + str(Ner_Feature[2]) + ' ||| |||\n')
        f_pt.writelines('_1_ ||| ' + jxsent + ' ||| ' + str(Ter_Feature[3]) + ' ' + str(Parser_Feature[3]) + ' ' + str(Ner_Feature[3] )+ ' ||| |||\n')
        f_pt.writelines('_1_ ||| ' + shsent + ' ||| ' + str(Ter_Feature[4]) + ' ' + str(Parser_Feature[4]) + ' ' + str(Ner_Feature[4] )+ ' ||| |||\n')
        f_pt.writelines('_1_ ||| ' + srisent + ' ||| ' + str(Ter_Feature[5]) + ' ' + str(Parser_Feature[5]) + ' ' + str(Ner_Feature[5]) + ' ||| |||\n')
        f_pt.close()
        # 利用online.ini翻译， 将翻译出来的结果保存
        # 生成input文件 _1_
        f_in = open('./files/input.file','w')
        f_in.writelines('_1_\n')
        f_in.close()

        subprocess.call('/local/kz2203/moses/mosesdecoder/bin/moses -f offline.ini < ./files/input.file > ./files/translated.file',shell = True)
        #subprocess.call('/local/kz2203/moses/mosesdecoder/bin/moses -f offline.ini < /local/kz2203/demo/Columbia/files/input.file ',shell = True)
        f_result = open('./files/translated.file','r')
        result = f_result.readline().strip('\n')
        f_result.close()
        
        # 删除中间生成的文件
        #subprocess.call('rm -f ./files/source.file', shell = True)
        subprocess.call('rm -f ./files/engine.file', shell = True)
        #subprocess.call('rm -f ./files/input.file', shell = True)
        #subprocess.call('rm -f ./files/phrase_table', shell = True)
        #subprocess.call('rm -f ./files/translated.file', shell = True)

        translate_result = result  # 这里需要改成自己的翻译结果
        end_time = time.clock()
        print 'Total Time IS ' + str(end_time - start_time)
        return jsonify(success=True, translate_result=translate_result)


class Dependency(MethodView):
    def get(self):


        # dependency_data 格式：
        # [
        #   {'engine': 'google', 'sent_1': ['abc','egd','age'], 'sent_2':[ 'def'], 'correct_dependency': ['abc']},
        #   {'engine': 'google', 'sent_1': ['abc','egd','age'], 'sent_2':[ 'def'], 'correct_dependency': ['abc']},
        #   {'engine': 'google', 'sent_1': ['abc','egd','age'], 'sent_2':[ 'def'], 'correct_dependency': ['abc']},
        # ]
        #'''
        f_en = open('./files/engine_parser.file','r')
        f_s = open('./files/source_parser.file','r')
        f_tran = open('./files/transdic.file','r')

        depend = [{},{},{},{},{},{}]
        engine_list = ['NRC','RWTH-PBT','RWTH-PBT-AML','RWTH-PBT-JX','RWTH-PBT-SH','SRI-HPBT']
        for i in xrange(6):
            depend[i]['engine'] = engine_list[i]
            depend[i]['sent_1'] = []
            depend[i]['sent_2'] = []
            depend[i]['correct_dependency'] = []

        sent = []
        for line in f_s:
            line = line.strip('\n')
            if line:
                sent.append(line)
        f_s.close()
        
        for i in xrange(6):
            depend[i]['sent_1'] = sent
            
        i = -1
        for line in f_en:
            line = line.strip('\n')
            if len(line) == 0:
                i = i + 1
                continue
            else:
                depend[i]['sent_2'].append(line)
        f_en.close()

        p = re.compile('(\S+?)\((\S+?)\-(\d+)\,\s(\S+)\-(\d+)\)')

        trans = [[],[],[],[],[],[]]
        i = -1
        for line in f_tran:
            line = line.strip('\n')
            if line == 'ENGINE':
                i = i+1
                continue
            else:
                trans[i].append(line)

        for i in xrange(6):
            for line in depend[i]['sent_2']:
                m = p.match(line)
                if m:
                    pair = m.group(5) + '-' + m.group(3)
                if pair in trans[i]:
                    depend[i]['correct_dependency'].append(line)
        #'''              
        
        dependency_data = depend
        #subprocess.call('rm -f ./files/engine_parser.file', shell = True)
        #subprocess.call('rm -f ./files/source_parser.file', shell = True)
        #subprocess.call('rm -f ./files/transdict.file', shell = True)
        
        return jsonify(success=True, data=dependency_data)
        

class TxtDB(MethodView):
    def get(self):
        filename = 'csent-test-common.seg'        
        f = open(filename, 'rb')
        db_list = f.readlines()  # 读取文本文件到list, db_list=[行1，行2，..., 行n]
        f.close()

        index = 1
        txtdb = []
        for row in db_list:
            if row.strip() != '':
                txtdb.append({'index': str(index), 'row': str(index) + ":" + row})  # 以row做index
                index += 1

        return jsonify(success=True, txtdb=txtdb)


app.add_url_rule('/google', view_func=Google.as_view('v_google'))
app.add_url_rule('/bing', view_func=Bing.as_view('v_bing'))
app.add_url_rule('/youdao', view_func=Youdao.as_view('v_youdao'))
app.add_url_rule('/nrc', view_func=NRC.as_view('v_nrc'))
app.add_url_rule('/pbt', view_func=PBT.as_view('v_pbt'))
app.add_url_rule('/aml', view_func=AML.as_view('v_aml'))
app.add_url_rule('/jx', view_func=JX.as_view('v_jx'))
app.add_url_rule('/sh', view_func=SH.as_view('v_sh'))
app.add_url_rule('/sri', view_func=SRI.as_view('v_sri'))
app.add_url_rule('/best', view_func=Best.as_view('v_best'))
app.add_url_rule('/best2', view_func=Best2.as_view('v_best2'))
app.add_url_rule('/dependency', view_func=Dependency.as_view('v_dependency'))
app.add_url_rule('/txtdb', view_func=TxtDB.as_view('v_txtdb'))
