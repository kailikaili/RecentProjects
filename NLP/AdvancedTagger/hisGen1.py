import sys, re, math, random, time

# This file is used to calculate the score of History

import sys, re, math, random, time
class HisGen:
        def __init__(self, modN, feaN):
                # modN is the train.dat
                pMod = re.compile('(\S+)\s+(\S+)')
                modF = open(modN, 'r')
                self.model = {}
                for l in modF:
                        m = pMod.match(l) 
                        if not m: continue
                        self.model[m.group(1)] = float(m.group(2))
                modF.close()
                feaF = open(feaN, 'r')
                self.sFea = set()
                for l in feaF:
                        self.sFea.add(l.strip())
                feaF.close()

                self.pSuff = re.compile('SUFF:(\S+):')
                self.pTag = re.compile('TAG:')
                self.pBin = re.compile('BIGRAM:')
                self.pHy = re.compile('HYPHEN:')
                self.pCap = re.compile('CAP:')
                self.pFir = re.compile('FIRST:')
                self.pLas = re.compile('LAST:')
                self.pHasn = re.compile('HASHUM:')

                self.phy = re.compile('.*-.*')
                self.pcap = re.compile('.*[A-Z].*')
                self.pnum = re.compile('.*\d.*')

                self.pVec = re.compile('(\d+)\s+(\S+)\s+(\S+)')
                self.pSen = re.compile('(\S+)')
                self.pTr = re.compile('(\S+)\s+(\S+)')

        def genScore(self, sentence, history):
                sentLst = sentence.split('\n')
                print sentLst
                print '********************************************************'
                sent = ['*']
                for l in sentLst:
                        m = self.pSen.match(l)
                        # if line is not empty
                        if not m: continue
                        sent.append(m.group(1))
                        # put sent into sent
                histLst = history.strip().split('\n')
                res = ''
                for l in histLst:
                        m = self.pVec.match(l)
                        if not m: continue
                        i = int(m.group(1))
                        term = sent[i]
                        tim = m.group(2)
                        ti = m.group(3)
                        score = 0.0
                        for fea in self.sFea:
                                feaKey = fea
                                mt = self.pSuff.match(fea)
                                if mt:
                                        sfl = int(mt.group(1))
                                        if len(term) >= sfl:
                                                feaKey += term[len(term)-sfl:len(term)] + ':' + ti
                                if self.pTag.match(fea):
                                        feaKey += term+':'+ti
                                if self.pBin.match(fea):
                                        feaKey += tim+':'+ti
                                if self.pHy.match(fea) and self.phy.match(term):
                                        feaKey += ti
                                if self.pCap.match(fea) and self.pcap.match(term):
                                        feaKey += ti
                                if self.pFir.match(fea) and i == 1:
                                        feaKey += ti
                                if self.pLas.match(fea) and i == len(sent)-2:
                                        feaKey += ti
                                if self.pHasn.match(fea) and self.pnum.match(term):
                                        feaKey += ti
                                if not feaKey == fea:
                                        score += self.model.get(feaKey, 0.0)
                        res += m.group(0) + '\t' + str(score) + '\n'
                return res

        def update(self, pred, gd, tr):
                predLst = pred.split('\n')
                gdLst = gd.split('\n')
                trLst = tr.split('\n')
                for i in range(0, len(gdLst)):
                        l1 = predLst[i]
                        l2 = trLst[i]
                        l3 = gdLst[i]
                        if l2 == '':
                                l2 = '##EOS##\tSTOP'
                                l3 = self.pVec.match(l1).group(1) + ' ' + self.pVec.match(gdLst[i-1]).group(3) + ' STOP' 
                        m1 = self.pVec.match(l1)
                        m2 = self.pTr.match(l2)
                        m3 = self.pVec.match(l3)
                        term = m2.group(1)
                        ti = m1.group(3)
                        tim = m1.group(2)
                        yi = m3.group(3)
                        yim = m3.group(2)
                        if ti == yi and tim == yim: continue
                        for fea in self.sFea:
                                feap = fea 
                                feac = fea 
                                mt = self.pSuff.match(fea)
                                if mt:
                                        sfl = int(mt.group(1))
                                        if len(term) >= sfl:
                                                feap += term[len(term)-sfl:len(term)] + ':' + ti
                                                feac += term[len(term)-sfl:len(term)] + ':' + yi
                                mt = self.pTag.match(fea) 
                                if mt and not term == '##EOS##':
                                        feap += term+':'+ti
                                        feac += term+':'+yi
                                mt = self.pBin.match(fea)
                                if mt:
                                        feap += tim+':'+ti
                                        feac += yim+':'+yi
                                if self.pHy.match(fea) and self.phy.match(term):
                                        feap += ti
                                        feac += yi

                                if self.pCap.match(fea) and self.pcap.match(term):
                                                feap += ti
                                                feac += yi
                                if self.pFir.match(fea) and i == 1:
                                                feap += ti
                                                feac += yi
                                if self.pLas.match(fea) and i == len(gdLst)-3:
                                                feap += ti
                                                feac += yi
                                if self.pHasn.match(fea) and self.pnum.match(term):
                                                feap += ti
                                                feac += yi
        
                                if not feap == fea:
                                        if feap in self.model:
                                                self.model[feap] += -1.0
                                        else:
                                                self.model[feap] = -1.0
                                        if feac in self.model:
                                                self.model[feac] += 1.0
                                        else:
                                                self.model[feac] = 1.0

        def genModel(self, modN):
                modF = open(modN, 'w')
                for fea in self.model:
                        if self.model[fea] == 0.0: continue
                        modF.write(fea+' '+str(self.model[fea])+'\n')
                modF.close()

