import nltk
import os
from nltk.collocations import BigramAssocMeasures,BigramCollocationFinder
from main import preprocessing


def read_dataset(_PATH):
    
    text = ''
    for dirPath, dirNames, fileNames in os.walk(_PATH):
        for fileName in fileNames:
            p = os.path.join(dirPath, fileName).replace('\\','/')
            f= open(p, mode = 'r', encoding='latin-1')
            text += f.read()
            
    
    text=text.replace('``', '')
    text=text.replace("''", '')
    return text


def read_annotation(_PATH):
    
    annotations = []
    
    f= open(_PATH, mode = 'r', encoding='latin-1')
    bi_num = 0
    for line in f:
        if len(line.split(' ')) == 2:
            bi_num+=1
            annotations.append(line.strip())
            
    print(bi_num)
    f.close()
    
    return annotations


def test():
    
    text = """
    LTE single-card dual-standby multi-mode terminal and method for processing concurrency of its CS service and PS service 

    The present invention is applicable to the field of communications technologies, and provides an method, the method includes: when a CS service and PS service of a local LTE single-card dual-standby multi-mode terminal are concurrent, detecting, by a local LTE single-card dual-standby multi-mode terminal, whether a peer communication terminal that is performing voice communication with it is in a voice silent period; when detecting that the peer communication terminal is not in the voice silent period, receiving, by the local LTE single-card dual-standby multi-mode terminal, downlink data in an LTE system, and suspending, by the local LTE single-card dual-standby multi-mode terminal, sending of uplink data in the LTE system at the same time; and when detecting that the peer communication terminal is in the voice silent period, sending the uplink data and receiving the downlink data, by the local LTE single-card dual-standby multi-mode terminal, in the LTE system.
    
    """
     
    bigram_measures = BigramAssocMeasures()
    #trigram_measures = TrigramAssocMeasures()
      
    # change this to read in your data
      
    finder = BigramCollocationFinder.from_words(preprocessing(text))
     
     
      
    # only bigrams that appear 3+ times
    #finder.apply_freq_filter(2)
      
    # return the 10 n-grams with the highest PMI
    #print(finder.nbest(bigram_measures.pmi,50))
    #print(finder.nbest(bigram_measures.likelihood_ratio, 20))
    #print(finder.nbest(bigram_measures.poisson_stirling, 20))
    for x,y in finder.nbest(bigram_measures.likelihood_ratio,50):
        print(x+' '+y)
    

def cal(finder, _TOP_NUM, total_bigrams, annotations):
    
    #print('total bigram num:%s'%(len(total_bigrams)))
    
    truth_no_related = []
    for x,y in total_bigrams:
        if x+'' +y not in annotations:
            truth_no_related.append(x+'' +y)
    

    bigram_measures = BigramAssocMeasures()
    #print('TOP WORDS : %s'%(_TOP_NUM))
    
    TP = 0
    TN = 0
    system_bigrams = finder.nbest(bigram_measures.likelihood_ratio, _TOP_NUM)
    system_no_related = []
    for x,y in total_bigrams:
        if x+' '+y not in system_bigrams:
            system_no_related.append(x+'' +y)
    
    for w in truth_no_related:
        if w in system_no_related:
            TN += 1
        
    for x,y in system_bigrams:
        if x+' '+y in annotations:
            TP += 1
    #print('likelihood_ratio precision: %s'%(TP/_TOP_NUM))
    #print('likelihood_ratio accuracy: %s'%((TP+TN)/(_TOP_NUM+len(system_no_related))))
    print('%s'%((TP+TN)/(_TOP_NUM+len(system_no_related))))
    
    
test()
# text = read_dataset('path/EL資料/deos14_ualberta_experiments/aquaint/RawTexts')
# annotations = read_annotation('path/EL資料/deos14_ualberta_experiments/aquaint/answer.txt')
# 
# words = preprocessing(text)
# total_bigrams = list(nltk.bigrams(words))
# 
# 
# finder = BigramCollocationFinder.from_words(preprocessing(text))
# 
# num = 50
# while(num<2000):
#     cal(finder, num, total_bigrams, annotations)
#     num += 50
#     



