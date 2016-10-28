import os
import re
import nltk
from main import preprocessing
from nltk.collocations import BigramAssocMeasures,BigramCollocationFinder,TrigramAssocMeasures,TrigramCollocationFinder
import textRank 
import sys
import networkx as nx
from main import RWR
import math
import requests
import time
"""
NUS corpus (Nguyen and Kan, 2007)
"""
def NUSCorpus():
    _PATH = 'path/AutomaticKeyphraseExtraction-master/Nguyen2007/data' 
     
    keys = set()
    docs = []
    total_length = 0
     
    for dirPath, dirNames, fileNames in os.walk(_PATH):
        for fileName in fileNames:
            p = os.path.join(dirPath, fileName).replace('\\','/')
            
            if '.key' in p:
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        for line in f:
                            keys.add(line.strip())
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='latin-1') as f:
                        for line in f:
                            keys.add(line.strip())
            elif '.txt' in p:
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        context = f.read()
                        docs.append(context)
                        total_length+=len(context)
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='latin-1') as f:
                        context = f.read()
                        docs.append(context)
                        total_length+=len(context)
                
    keys.remove('')
    
    print('=== NUS corpus ====')
    print('Annotations number: %s' %(len(keys)))
    print('Document number: %s' %(len(docs)))
    print('Avg document length : %s' %(total_length/len(docs)))
    print('#gold keyphrases/document: %s' %(len(keys)/len(docs)))
    
    return (docs,keys)


"""
SemEval-2010 (Kim et al., 2010)
"""
def SemEval():
    _PATH = 'path/AutomaticKeyphraseExtraction-master/SemEval2010'
    
    keys = set()
    docs = []
    ever_read = set()
    total_length = 0
    
    for dirPath, dirNames, fileNames in os.walk(_PATH):
        for fileName in fileNames:
            p = os.path.join(dirPath, fileName).replace('\\','/')
                
            if '.txt.final' in p and re.sub('.+/(.+)\.txt\.final', '\g<1>', p) not in ever_read:
                ever_read.add(re.sub('.+/(.+)\.txt\.final', '\g<1>', p))
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        """   Abstract and Introduction"""
                        context = ''
                        for line in f:
                            if re.match('2(\.)? .+\n', line):
                                break
                            else:
                                context += line+' '
                        #context = f.read()
                        docs.append(context)
                        total_length+=len(context)
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='utf8') as f:
                        """   Abstract and Introduction"""
                        context = ''
                        for line in f:
                            if re.match('2(\.)? .+\n', line):
                                break
                            else:
                                context += line+' '
                        #context = f.read()
                        docs.append(context)
                        total_length+=len(context)
            elif '.combined.stem.final' in p:
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        for line in f:
                            for key in line.split(' : ')[1].split(','):
                                keys.add(re.sub('[\n\t]', '', key).lower())
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='utf8') as f:
                        for line in f:
                            for key in line.split(' : ')[1].split(','):
                                keys.add(re.sub('[\n\t]', '', key).lower())
            elif '.combined.final' in p:
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        for line in f:
                            for key in line.split(' : ')[1].split(','):
                                keys.add(re.sub('[\n\t]', '', key).lower())
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='utf8') as f:
                        for line in f:
                            for key in line.split(' : ')[1].split(','):
                                keys.add(re.sub('[\n\t]', '', key).lower())
     
    
    print('=== SemEval-2010 ====')
    print('Annotations number: %s' %(len(keys)))
    print('Document number: %s' %(len(docs)))
    print('Avg document length : %s' %(total_length/len(docs)))
    print('#gold keyphrases/document: %s' %(len(keys)/len(docs)))
    
    return (docs,keys)
     

"""
Inspec (Hulth, 2003)
"""
def Inspec():
    _PATH = 'path/AutomaticKeyphraseExtraction-master/Hulth2003/Validation'
     
    docs = []
    keys = set()
    total_length = 0
    KEY_NUM = 0
    
    for dirPath, dirNames, fileNames in os.walk(_PATH):
        for fileName in fileNames:
            p = os.path.join(dirPath, fileName).replace('\\','/')
                
            if '.abstr' in p:
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        context = f.read()
                        docs.append(context)
                        total_length+=len(context)
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='latin') as f:
                        context = f.read()
                        docs.append(context)
                        total_length+=len(context)
            elif '.contr' in p:
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        for key in f.read().split('; '):
                            keys.add(re.sub('[\n\t]', '', key.lower()))
                            KEY_NUM+=1
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='latin') as f:
                        for key in f.read().split('; '):
                            keys.add(re.sub('[\n\t]', '', key.lower()))
                            KEY_NUM+=1          
            elif 'uncontr' in p:
                try:
                    with open(p, mode='r', encoding='utf8') as f:
                        for key in f.read().split('; '):
                            keys.add(re.sub('[\n\t]', '', key.lower()))
                            KEY_NUM+=1
                except UnicodeDecodeError:
                    with open(p, mode='r', encoding='latin') as f:
                        for key in f.read().split('; '):
                            keys.add(re.sub('[\n\t]', '', key.lower()))
                            KEY_NUM+=1
                
    
    print('=== Inspec ====')
    print('Annotations number: %s' %(len(keys)))
    print('Document number: %s' %(len(docs)))
    print('Avg document length : %s' %(total_length/len(docs)))
    print('#gold keyphrases/document: %s' %(len(keys)/len(docs)))
    print(KEY_NUM)
    
    return (docs,keys, KEY_NUM)
    
def filter(manuals, word_window):
    if word_window == 1:
        new = set([manual for manual in manuals if ' ' not in manual])
        print('uni annotations number : %s'%(len(new)))
    else:
        new = set([manual for manual in manuals if len(manual.split(' ')) > word_window])
        print('annotations number : %s'%(len(new)))
    
    return new

"""
list, set , set
"""
def statics(tp, predicted_num, manuals_num):
    
    print('\n=== statics ====') 
    """  precision P = TP / ( TP + FP )"""
    precision = tp/predicted_num
    print('precision : %s' %(precision))
    
    """  recall R = TP / ( TP + FN )"""
    recall = tp/manuals_num
    print('recall : %s' %(recall))
    
    """ F-measure F = 2 / ( 1 / P + 1 / R) = 2 * P * R / ( P + R ) """
    f_measure = 2*precision*recall/(precision+recall)
    print('F-measure : %s' %(f_measure))
    
    

def distSortByValue(dic, _TOP_N):
    
    count = 1
    for key, value in sorted(dic.items(), key=lambda x: x[1], reverse=True):
        if count>_TOP_N:
            break
        print ('%s: %s' % (key, value))
        count+=1
        
        
def dictTopN(dic, _TOP_N):
    
    new = {}
    count = 1
    for key, value in sorted(dic.items(), key=lambda x: x[1], reverse=True):
        if count>_TOP_N:
            break
        new[key] = value
        count+=1
        
    return new
    
def TFIDF(docs):
    
    _DOCS_NUM = len(docs)
    docs_bis = []
    #total_bis = []
    result = {}
    #bigram_measures = BigramAssocMeasures()
    bisFreDist = {}
    _BI_NUM = 0
    
    for doc in docs:
        #finder = BigramCollocationFinder.from_words(preprocessing(doc))
        #bi = finder.nbest(bigram_measures.likelihood_ratio,2000)
        bi = list(nltk.bigrams(preprocessing(doc)))
        docs_bis.append(bi)
        _BI_NUM+=len(bi)
        #total_bis+=bi
        for word in bi:
            if word in bisFreDist:
                bisFreDist[word] += 1
            else:
                bisFreDist[word] = 1
    
    #bisFreDist = nltk.FreqDist(total_bis)
    #total_bis = None
    
    for word,freq in bisFreDist.items():
        try:
            count = sum(1 for doc_bis in docs_bis if word in doc_bis)
            idf = math.log10(_DOCS_NUM/count) + 0.01      
            #print(idf,bi_TFdist.freq(word))
            (x,y) = word 
            #result[x.lower()+' '+y.lower()] = bisFreDist.freq(word)*idf
            result[x.lower()+' '+y.lower()] = freq/_BI_NUM*idf
        except AttributeError:
            pass
        
    bisFreDist = None
    
    return result


def TFIDF_1(docs, manuals, topN):
    
    _DOCS_NUM = len(docs)
    docs_words = []
    idfCount = {}
    

    print('PROCESS--IDF')
    for i,doc in enumerate(docs):
        sys.stdout.write("\r{0}/{1}".format(i+1, _DOCS_NUM))
        sys.stdout.flush()
        words = preprocessing(doc.lower())
        
        docs_words.append(words)
        
        for word in set(words):
            if word in idfCount:
                idfCount[word] += 1
            else:
                idfCount[word] = 1
    
    tp = 0
    predicted_num = 0
    candidates = {}
    
    print('\nPROCESS--TFIDF and topN predict')
    for i,doc_words in enumerate(docs_words):
        sys.stdout.write("\r{0}/{1}".format(i+1, len(docs_words)))
        sys.stdout.flush()
        tfCount = {}
        tfidf = {}
        _WORDS_NUM = 0
        for word in doc_words:
            if word in tfCount:
                tfCount[word]+=1
            else:
                tfCount[word]=1
            _WORDS_NUM+=1
        
        for word,freq in tfCount.items():
            idf = math.log10(_DOCS_NUM/idfCount[word])
            tfidf[word]=freq/_WORDS_NUM*idf
        
        
        for word,value in tfidf.items():
            if word in candidates:
                candidates[word]+=value
            else:
                candidates[word]=value
        
        
        predicted = dictTopN(candidates, topN)
        predicted_num+=len(predicted)
        tp+=sum(1 for word in predicted if word in manuals)
    
    statics(tp, predicted_num, len(manuals))



def proposed(docs, manuals, topN, alpa):
    
    print('=== PROPOSED ====')
    
    _DOCS_NUM = len(docs)
    docs_words = []
    _WORDS_NUM = 0
    idfCount = {}
    tfCount = {}
    occurCount = {}
    
    

    """  Log-likelihood ratio bigrams """
    print('PROCESS--Log likelihood ratio bigrams')
    tmp = []
    for doc in docs:
        tmp+=preprocessing(doc.lower())
    finder = BigramCollocationFinder.from_words(tmp)
    #_size = math.floor(len(finder.score_ngrams(BigramAssocMeasures().likelihood_ratio))/20)+1
    bigramSet = finder.nbest(BigramAssocMeasures().likelihood_ratio, 200)
     
#     finder = TrigramCollocationFinder.from_words(tmp)
#     _size = math.floor(len(finder.score_ngrams(TrigramAssocMeasures().likelihood_ratio))/40)+1
#     trigramSet = finder.nbest(TrigramAssocMeasures().likelihood_ratio, _size)
#     tmp = None
    
    #nltk.RegexpParser('{(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}')
    
    for i,doc in enumerate(docs):
        sys.stdout.write("\r{0}/{1}".format(i+1, len(docs)))
        sys.stdout.flush()
        words = preprocessing(doc.lower())
        
        dealwith = set()
        for x,y in bigramSet:
            if x in words and y in words:
                if x not in dealwith:
                    words.remove(x)
                    dealwith.add(x)
                if y not in dealwith:
                    words.remove(y)
                    dealwith.add(y)
                words.append(x+' '+y)
            else:
                pass
              
#         for x,y,z in trigramSet:
#             if x in words and y in words and z in words:
#                 if x not in dealwith:
#                     words.remove(x)
#                     dealwith.add(x)
#                 if y not in dealwith:
#                     words.remove(y)
#                     dealwith.add(y)
#                 if z not in dealwith:
#                     words.remove(z)
#                     dealwith.add(z)
#                 words.append(x+' '+y+' '+z)
#             else:
#                 pass
            
        docs_words.append(words)
        
        _WORDS_NUM+=len(words)
        """  count idf """
        for word in set(words):
            if word in idfCount:
                idfCount[word] += 1
            else:
                idfCount[word] = 1
        
        """  count occur and tf"""
        for j,word1 in enumerate(words):
            
            if word1 in tfCount:
                tfCount[word1]+=1
            else:
                tfCount[word1]=1
            
            for word2 in words[j+1:]:
                if (word1, word2) in occurCount:
                    occurCount[(word1, word2)]+=1
                elif (word2,word1) in occurCount:
                    occurCount[(word2, word1)]+=1
                else:
                    occurCount[(word1, word2)]=1
                    
#     """ Compute PMI"""
#     for (word1, word2) in occurCount:
#         val = round(math.log10(occurCount[(word1, word2)]*_WORDS_NUM/tfCount[word1]/tfCount[word2]), 8)
#         occurCount[(word1, word2)] = val
#           
#     """  Construct graph """
#     g = nx.Graph()
#     for (word1, word2),value in occurCount.items():
#         g.add_edge(word1, word2, weight=value)
#     print('Graph node number: %s'%(g.number_of_nodes()))
#     print('Graph edge number: %s'%(g.number_of_edges()))
#     occurCount = None
#        
#     rwrScore = RWR(g, None, 0.03 , 1000, 0.000003)
     
#     _min = min(rwrScore.values())
#     _max = max(rwrScore.values())
#     print(_min,_max)
#     for key,value in rwrScore.items():
#         rwrScore[key] = (value-_min)/(_max-_min)
    

    tp = 0
    predicted_num = 0
    candidates = {}
    
    for i, doc_words in enumerate(docs_words):
        sys.stdout.write("\r{0}/{1}".format(i+1, len(docs_words)))
        sys.stdout.flush()
        thisTfCount = {}
        newScore = {}
        
        _NUM = len(doc_words)
        
        for word in doc_words:
            if word in thisTfCount:
                thisTfCount[word]+=1
            else:
                thisTfCount[word]=1
        
        """ TF-IDF """
        for word,tf in thisTfCount.items(): 
            newScore[word] = tf/_NUM*math.log10(_DOCS_NUM/idfCount[word])
        
        _min = min(newScore.values())
        _max = max(newScore.values())
        
        for word,tfidf in newScore.items():
            #val = alpa*(tfidf-_min)/(_max-_min) + (1-alpa)*rwrScore[word]
            #val = tfidf + rwrScore[word]
            if word in candidates:
                candidates[word]+=tfidf
            else:
                candidates[word]=tfidf 
        

        predicted = dictTopN(candidates, topN)
        predicted_num+=len(predicted)
        tp+=sum(1 for word in predicted if word in manuals)
    
    
    statics(tp, predicted_num, len(manuals))
    
    
def dbpediaSpotlight(docs, manuals):
    
    headers  = {
               'Connection': 'keep-alive',
               'Accept': 'application/json',
               'Origin': 'http://dbpedia-spotlight.github.io',
               'Referer': 'http://dbpedia-spotlight.github.io/demo/',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'
               }
    
    
    _DOCS_NUM = len(docs)
    tp = 0
    predicted_num = 0
    
    print('=== dbpedia spotlight ====')
    
    for i,doc in enumerate(docs):
        sys.stdout.write("\r{0}/{1}".format(i+1, _DOCS_NUM))
        sys.stdout.flush()
        
        predicted = set()
        
        for paragraph in re.split('\.\n', doc):
            #print(paragraph)
            payload = {
                   'text': re.sub('[\n\t]', '', paragraph),
                   'confidence':0.5,
                   'support':0,
                   'spotter':'Default',
                   'disambiguator':'Default',
                   'polic':'whitelist'
                   }
        
            r = requests.get('http://spotlight.sztaki.hu:2222/rest/annotate'
                             , headers=headers ,params=payload)

            try:
                for entity in r.json()['Resources']:
                    predicted.add(entity['@surfaceForm'].lower())
            except KeyError:
                """  system predict nothing """
                print(r.json())
                #statics(tp, predicted_num, len(manuals))
            except ValueError:
                pass
            
            time.sleep(1)
                
        tp+=sum(1 for word in predicted if word in manuals)
        predicted_num+=len(predicted)    
        
    statics(tp, predicted_num, len(manuals))

if __name__ == '__main__':
    
   

    #(docs, manuals) = SemEval()
    #(docs, manuals, KEY_NUM) = Inspec()
    (docs, manuals) = NUSCorpus()
    
    
    proposed(docs, manuals, 20, 0.8)
    #dbpediaSpotlight(docs, manuals)
    
    
#     print('=== TFIDF ====') 
#     TFIDF_1(docs, manuals, 10)
    
    
    
#     print('=== textRank ====') 
#     doc_size = len(docs)
#     candidates = {}
#     tp = 0
#     predicted_num = 0
#     for i,doc in enumerate(docs):
#         sys.stdout.write("\r{0}/{1}".format(i+1, doc_size))
#         sys.stdout.flush()
#            
#         for word in textRank.extractKeyphrases(doc):
#             if word in candidates:
#                 candidates[word]+=1
#             else:
#                 candidates[word]=1
#                 
#         predicted = dictTopN(candidates, 10)
#         tp+=sum(1 for word in predicted if word in manuals)
#         predicted_num+=len(predicted)
#             
#     statics(tp, predicted_num, len(manuals))
     
    





