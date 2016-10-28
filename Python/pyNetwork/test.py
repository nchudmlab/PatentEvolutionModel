
import sys
import time
import math
import requests
import re
from nltk.collocations import BigramAssocMeasures,BigramCollocationFinder
import nltk



# s = 'Physical uplink control channel (PUCCH) resource mapping using an enhanced physical downlink control channel (CDMA-MIMO)'
# words = nltk.word_tokenize(s, 'english')
# fdist = nltk.FreqDist(words)
# 
# print(fdist['channel'])

# for term, pos in nltk.pos_tag(words):
#     
#     if re.match('^[A-Z-]+$', term) :
#         print(term)
#     




# content = 'A method and system for efficient DRX operation during handover in LTE in which a user equipment expects handover to occur, the method having the steps of: checking whether a no handover initiation decision is received within a predetermined time period; if no, performing the steps of: ensuring the user equipment is not in a DRX sleep period during reception of a handover grant; checking whether a handover grant is received, and if yes, performing a handover procedure; and if no, resuming a DRX sleep interval; and if yes, ending the process.'
# 
# 
# words = nltk.word_tokenize(content, 'english')
# finder = BigramCollocationFinder.from_words(words)
# _size = math.floor(len(finder.score_ngrams(BigramAssocMeasures().likelihood_ratio))/2)+1
# bi_words = list(finder.nbest(BigramAssocMeasures().likelihood_ratio, _size))
# 
# 
# print(finder.ngram_fd[('a', 'handover')])



# for k,v in finder.ngram_fd.items():
#     print(k,v)

# for i in range(0,5):
#     tmp = i
#     if i==3:
#         continue
#     
#     print(tmp)
    


# a = [1,2,2]
# b = [2]
# print(list(set(a)|set(b)))
#print(math.log10(3))
# 
# idf = math.log10(1)
# print(idf)
# if idf == 0:
#     print(1)
# a = [['1'],['1'],['1']]
# print(len(a))
# 
# for i in range(10):
#     sys.stdout.write("\r{0}>".format(str(i)))
#     sys.stdout.flush()
#     time.sleep(0.5)
# 
# dict = {'1':2}
# for word,value in dict.items():
#     print(word,value)
#   
# 

