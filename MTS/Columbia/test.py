# -*- encoding: utf-8 -*-

import urllib2,sys
import json
import urllib
import time


def tran(query):
        url = 'http://api.microsofttranslator.com/v2/ajax.svc/TranslateArray2?\
appId=%22TdzjK2kMM-8Qb1bbbLghjkj-jlUZ5pDI-x1Q8S8QIPOQneI_MrLEOPAimhW4iAXQX%22&\
texts=[%22' + urllib.quote(query) +'%22]&from=%22%22&to=%22en%22&oncomplete=_mstc2&onerror=_mste2&loc=en&ctr=&'
        headers = { 'User-Agent' : 'Mozilla/5.0', 'Host':'www.microsofttranslator.com', 'Accept-Language':'zh,en-us;q=0.7,en;q=0.3', 'Accept': '*/*'}
        req = urllib2.Request(url, None, headers)
        html = urllib2.urlopen(req).read()[11:-3]
        print html
        #.read()[11:-3]
        trans_res = json.loads(html)
        return trans_res['TranslatedText']


if __name__ == "__main__":
        reload(sys)
        sys.setdefaultencoding('utf-8')
        line = '我们都是好孩子。'
        query = line.strip('\n').replace('\"','\\"')
        print query
        import sys
        print sys.getdefaultencoding()
        outline = str(tran(query))
        print outline
       
            
