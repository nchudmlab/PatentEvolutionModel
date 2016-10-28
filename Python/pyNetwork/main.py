# -*- coding: utf8 -*-
import networkx as nx
#import matplotlib.pyplot as plt
from pyMysql import mysql
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.collocations import BigramAssocMeasures,BigramCollocationFinder,TrigramAssocMeasures,TrigramCollocationFinder
import math
import re
import datetime
import random
import logging
import json
import sys

 


def TRIMMEAN(array):
    
    mean = 0
    LEN = len(array)
    
    if LEN<3:
        mean = sum(array)/LEN
        
    else:
        MAX_VAL = max(array)
        MIN_VAL = min(array)
        
        SUM = 0
        count = 0
        for e in array:
            #if e != MAX_VAL and e != MIN_VAL:
            if e != MIN_VAL:
                SUM+=e
                count+=1    
        #print(count)
        mean = SUM/count
        
    return mean

def load_CPC(_CPC_PATH):
    
    with open(_CPC_PATH) as data_file:    
        return json.load(data_file)
 
"""
input:List word
"""
def preprocessing(s):
    
    stop_punctuations = ['*','"','--',':','&','...','`','\'','\'s','\'m','?','\'t','“','(',')','.',',','[',']','<','>',';','@','‘','”']
    stop_pos = ['PRP','IN','WRB','WDT','CC','MD','TO','VB','VBN','IN','VBZ','RB','RP','VBG','VBD','VBP','DT']
    good_pos = ['NN', 'NNS','NNP','NNPS' ]
    repls = {'in relation to':',','type of':'','type for':'','and/or':'and','at least one of':''
            ,'method and apparatus':'method','method apparatus':'method','at least one':''
            ,'one and more':'','system and method':'system','apparatus and method':'method'}
    
    #stopword = ['methods','method','invention','inventions','apparatus','first','second','present','third','plurality']
    
#     for punctuation in punctuations:
#         s = s.replace(punctuation,' ')
#     for old,new in repls.items():
#         s=s.replace(old, new)
    
    words = nltk.word_tokenize(s, 'english')
    
    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]
    
    # Remove numbers
    #words = [word for word in words if not word.isnumeric()]
    
    # Lowercase all words (default_stopwords are lowercase too)
    #words = [word.lower() for word in words]
    
    # Remove stopwords
    #words = [word for word in words if word not in set(stopwords.words('english'))]
    
    # Remove POS
    reduce_words = []
    
    for term,pos in nltk.pos_tag(words):
        
#         """and pos is not 'JJ'"""
#         if term.lower() not in stopword :
            #if pos not in stop_pos and term not in stop_punctuations:
        if pos in good_pos and pos not in stop_punctuations:
            reduce_words.append(term)
                
                
    
    
    return reduce_words


def steiner_tree(graph,terminals=None):
    
    terminals = list(terminals)
    #no_path = []
    terminal_short_path = []
    terminal_short_path_graph=nx.Graph()
    steiner_tree = nx.Graph()
    
    """ terminal short path """
    for i,source in enumerate(terminals):
        for target in terminals[i+1:]:
            try:
                path = nx.shortest_path(graph, source, target)
                
                terminal_short_path.append(path)
                #print(nx.shortest_path(graph, source, target))
                terminal_short_path_graph.add_edge(path[0], path[-1], weight=len(path)-1)
                
            except nx.exception.NetworkXNoPath:
                """ no short path : infinite""" 
                pass
        
    
    T = nx.minimum_spanning_tree(terminal_short_path_graph)
    for (src, dst) in T.edges():
        for nodes in terminal_short_path:
            if nodes[0] is src and nodes[-1] is dst:
                steiner_tree.add_path(nodes)
                terminal_short_path.remove(nodes)
                break
            
    
    return steiner_tree


""" directed steiner tree algorithm """
def di_steiner_tree(graph,terminals=None):
    
    terminals = list(terminals)
    #no_path = []
    terminal_short_path = []
    terminal_short_path_graph = nx.Graph()
    steiner_tree = nx.DiGraph()
    
    
    """ terminal short path """
    for i,source in enumerate(terminals):
        for target in terminals[i+1:]:
            paths = None
            paths = nx.all_shortest_paths(graph, source, target)
            try:
                #print(source,target,[p for p in paths])
                for p in paths:
                    terminal_short_path.append(p)
                    terminal_short_path_graph.add_edge(p[0], p[-1], weight=len(p)-1)

            except nx.exception.NetworkXNoPath:
                paths = nx.all_shortest_paths(graph, target, source)
                try:
                    #print(target,source,[p for p in paths])
                    for p in paths:
                        terminal_short_path.append(p)
                        terminal_short_path_graph.add_edge(p[0], p[-1], weight=len(p)-1)
                        
                
                except nx.exception.NetworkXNoPath:
                    paths = None
        
              
    #print(terminal_short_path)
    #print(terminal_short_path_graph.number_of_nodes())
    
    T = nx.minimum_spanning_tree(terminal_short_path_graph)
    for (src, dst) in T.edges():
        #print(src,dst)
        for nodes in terminal_short_path:
            if nodes[0] is src and nodes[-1] is dst:
                steiner_tree.add_path(nodes)
                #terminal_short_path.remove(nodes)
            elif nodes[0] is dst and nodes[-1] is src:
                steiner_tree.add_path(nodes)
            
    
#     non_terminals = set(steiner_tree.nodes())-set(terminals)
#     
#     for non_terminal in non_terminals:
#         
#         """  copy """
#         copy_steiner_tree = nx.Graph()
#         copy_steiner_tree.add_edges_from(steiner_tree.edges)
#         
#         del copy_steiner_tree.node[non_terminal]
#         
#         """  check pair terminals is connected"""
#         _FLAG = True
#         for i,source in enumerate(terminals):
#             for target in terminals[i+1:]:
#                 if nx.has_path(copy_steiner_tree, source, target):
#                     continue
#                 else:
#                     _FLAG = False
        
                    
    return steiner_tree

    
def test_di_steiner_tree():

    DG = nx.DiGraph()
    DG.add_edge('v1', 'v2')
    DG.add_edge('v1', 'v4')
    #G.add_edge('v1', 'v5')
    DG.add_edge('v1', 'v3')
    DG.add_edge('v2', 'v5')
    DG.add_edge('v7', 'v3')
    DG.add_edge('v4', 'v5')
    DG.add_edge('v8', 'v4')
    DG.add_edge('v4', 'v9')
    DG.add_edge('v5', 'v6')
    DG.add_edge('v5', 'v9')
    DG.add_edge('v7', 'v8')
    DG.add_edge('v8', 'v9')
    
    """
    domi_set = nx.dominating_set(DG)
    print(domi_set)
    #domi_set = set(['v1','v6','v8'])
    print('domi size:%s ' %(len(domi_set)))
    
    s_tree = di_steiner_tree(DG, domi_set)
    print(s_tree.edges())
    print('stree node number %d' %(s_tree.number_of_nodes()))
    """
    
    print(list(nx.all_neighbors(DG, 'v1')))
    
def bigramFreqDist(patnos):
    
    
    sql = mysql()
    sql.connect()
    s=''
    for title,abstract,description,claim in sql.getPatent_content(patnos):
        s += title+' '+abstract
    sql.close()
    
    words = nltk.word_tokenize(s, 'english')
    words = preprocessing(words)
    words = nltk.bigrams(words)

    return nltk.FreqDist(words)
    

def sort_date(dates):
    
    return sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m'))
    
def build_wiki_dict():
    
    wiki = set()
    
    URLs = ['path/Thesis/Image_processing_DICT',
            'path/Thesis/Computer_graphics_DICT']
    
    for URL in URLs:
        f = open(URL, encoding = 'utf8')
        
        for line in f:
            #phrase = re.sub('(\S+)\/?\S*', '\g<1>', line).replace('_',' ')
            phrase = line.strip()
            wiki.add(phrase)
            
        f.close
    
    #print('wiki dist size %s' %(len(wiki)))
    
    return wiki


def filter_tfidf(tfidf, threshold):
    
    new_tfidf = []
    
    for term in tfidf:
        if tfidf[term] > threshold:
            new_tfidf[term] = tfidf[term]
    
    return new_tfidf

def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"  

def choice(choices):
    
    r = random.uniform(0, len(choices))
    upto = 0
    for c in choices:
        if upto + 1 >= r:
            return c
        upto += 1
    assert False, "Shouldn't get here"  

    
"""
input: graph
    v, the starting vertex;
    a, the restart probability;
    n, the number of steps to be executed;
    t, the frequency threshold
"""
def RWR(graph, starts, _restart_prob, iter_count, threshold):
    
    counts = {}
    
    for node in graph.nodes():
        counts[node] = 0
    
    start_vertices = []
    _PICK_PRO = 0.1
    
    print('%s RWR START'%(str(datetime.datetime.now())))
    
    """  random pick a set of start vertex """
    
    if starts is None:
        nodes = list(graph.nodes())
        
        c = math.floor(len(nodes)*_PICK_PRO)
        if c<50:
            start_vertices = nodes
        else:
            while c > 0:
                start_vertices.append(choice(nodes))
                c-=1
            
    else:
        start_vertices = starts
    
    
    _VERTICES_NUM = len(start_vertices)
    for i,start_vertex in enumerate(start_vertices):
        _v = start_vertex
        c = iter_count
        
        while c > 0:
            
            sys.stdout.write("\r{0}/{1}---{2}/{3}".format(i, _VERTICES_NUM, iter_count-c+1, iter_count))
            sys.stdout.flush()
            
            #print('%s/%s'%(str(iter_count-c+1),str(iter_count)))
            if random.random() > _restart_prob:
                neighbors = list(graph.neighbors(_v))
                choices = []
                for neighbor in neighbors:
                    choices.append((neighbor,graph[_v][neighbor]['weight']))
                
                _v = weighted_choice(choices)
                counts[_v]+=1
            else:
                _v = start_vertex
            c-=1
    
            
    _PICK_SIZE = len(start_vertices)
    
#     for key, value in sorted(counts.items(), key=lambda x: x[1], reverse=True):
#         print ('%s: %s' % (key, value/_PICK_SIZE/iter_count))

    copy_counts = {}
    #print(counts)
    for key, value in counts.items():
        try:
            prob = value/_PICK_SIZE/iter_count
            prob = round(prob, 6)
        except ZeroDivisionError:
            print(value,_PICK_PRO, iter_count)
        if prob > threshold:
            copy_counts[key] = prob
        
    counts = None
    print('\n%s RWR END'%(str(datetime.datetime.now())))
    
    return copy_counts
    

def PMI(docs):
 
    """  Calculate PMI """ 
    _mutual_occur = {}
     
    docs_candidateTermSet = []
    _DOCS_NUM = len(docs)
    _TERM_NUM = 0
    fredist = {}
     
    stopword = set(['methods','method','invention','inventions','apparatus','first','second','present','third','plurality'])
     
    print('%s Processing START'%(str(datetime.datetime.now())))
     
    task_num = 1
    for doc in docs:
         
        sys.stdout.write("\r{0}/{1}".format(task_num, _DOCS_NUM))
        sys.stdout.flush()
         
        raw_words = preprocessing(doc)
        if len(raw_words)<5:
            task_num+=1
            continue
         
        fdist = nltk.FreqDist(raw_words)
        abbrSet = set()
        tmp_words = []
        for term in raw_words:
            if re.match('^[A-Z-]+$', term) :
                abbrSet.add(term)
            else:
                tmp_words.append(term)
        raw_words = None
         
        finder = BigramCollocationFinder.from_words(tmp_words)
        tmp_words = None
        
        _size = math.floor(len(finder.score_ngrams(BigramAssocMeasures().likelihood_ratio))/2)+1
        """ select top bigram """
         
        termList = []
        for x,y in list(finder.nbest(BigramAssocMeasures().likelihood_ratio, _size)):
            if x.lower() not in stopword and y.lower() not in stopword:
                termList.append(x+' '+y)
            else:
                pass
             
        termList+=list(abbrSet)
        abbrSet = None
                     
        candidateTermSet = set()
        for i,term1 in enumerate(termList):
             
            wordnum = 0
            if ' ' in term1:
                term1_split = term1.split(' ')
                wordnum = finder.ngram_fd[(term1_split[0], term1_split[1])]
            else:
                wordnum = fdist[term1]
             
            candidateTermSet.add(term1)
             
            if term1 in fredist:
                fredist[term1]+=wordnum
            else:
                fredist[term1]=wordnum
             
            _TERM_NUM +=wordnum
             
            for term2 in termList[i+1:]:
                if (term1, term2) in _mutual_occur:
                    _mutual_occur[(term1, term2)]+=1
                elif (term2, term1) in _mutual_occur:
                    _mutual_occur[(term2, term1)]+=1
                else:
                    _mutual_occur[(term1, term2)]=1
         
        docs_candidateTermSet.append(candidateTermSet)
        candidateTermSet = None
        task_num+=1
        
    termList = None
               
    for (term1, term2) in _mutual_occur:
        val = round(math.log10(_mutual_occur[(term1, term2)]*_TERM_NUM/fredist[term1]/fredist[term2]), 9)
        _mutual_occur[(term1, term2)] = val
         
    for term in fredist:
        fredist[term]=fredist[term]/_TERM_NUM
         
    print('\n%s Processing PMI END'%(str(datetime.datetime.now())))
         
    """  Construct graph """
    pmi_graph = nx.Graph()
     
    for (x,y),value in _mutual_occur.items():
        pmi_graph.add_edge(x, y, weight=value)
     
    _mutual_occur = None
     
    print('PMI Graph node number: %s'%(pmi_graph.number_of_nodes()))
    print('PMI Graph edge number: %s'%(pmi_graph.number_of_edges()))
     
     
    return (RWR(pmi_graph, None, 0.03 , 800, 0.0000001), docs_candidateTermSet, fredist)


# def PMI(docs):
#  
#     """  Calculate PMI """ 
#     _mutual_occur = {}
#      
#     docs_bigramSet = []
#     _DOCS_NUM = len(docs)
#     _BIGRAMS_NUM = 0
#     fredist = {}
#      
#     stopword = set(['methods','method','invention','inventions','apparatus','first','second','present','third','plurality'])
#      
#     print('%s Bigram PMI START'%(str(datetime.datetime.now())))
#      
#     task_num = 1
#     for doc in docs:
#          
#         sys.stdout.write("\r{0}/{1}".format(task_num, _DOCS_NUM))
#         sys.stdout.flush()
#          
#         words = preprocessing(doc)
#         if len(words)<5:
#             task_num+=1
#             continue
#          
#          
#          
#         finder = BigramCollocationFinder.from_words(words)
#         _size = math.floor(len(finder.score_ngrams(BigramAssocMeasures().likelihood_ratio))/2)+1
#         """ select top bigram"""
#         bi_words = []
#          
#         for x,y in list(finder.nbest(BigramAssocMeasures().likelihood_ratio, _size)):
#             if x.lower() not in stopword and y.lower() not in stopword:
#                 bi_words.append((x,y))
#             else:
#                 pass
#                      
#         bigrams = set()
#         for i,(x,y) in enumerate(bi_words):
#             _a = x+' '+y
#              
#             wordnum = finder.ngram_fd[(x,y)]
#              
#             bigrams.add(_a)
#              
#             if _a in fredist:
#                 fredist[_a]+=wordnum
#             else:
#                 fredist[_a]=wordnum
#              
#             _BIGRAMS_NUM +=wordnum
#              
#             for (i,j) in bi_words[i+1:]:
#                 _b = i+' '+j
#                 #print(_a , _b)
#                 if (_a,_b) in _mutual_occur:
#                     _mutual_occur[(_a,_b)]+=1
#                 elif (_b,_a) in _mutual_occur:
#                     _mutual_occur[(_b,_a)]+=1
#                 else:
#                     _mutual_occur[(_a,_b)]=1
#          
#         docs_bigramSet.append(bigrams)
#                  
#         task_num+=1
#          
#                
#     for (x,y) in _mutual_occur:
#         val = round(math.log10(_mutual_occur[(x,y)]*_BIGRAMS_NUM/fredist[x]/fredist[y]), 9)
#         _mutual_occur[(x,y)] = val
#          
#     for bigram in fredist:
#         fredist[bigram]=fredist[bigram]/_BIGRAMS_NUM
#          
#     print('\n%s Bigram PMI END'%(str(datetime.datetime.now())))
#          
#     """  Construct graph """
#     pmi_graph = nx.Graph()
#      
#     for (x,y),value in _mutual_occur.items():
#         pmi_graph.add_edge(x, y, weight=value)
#      
#     _mutual_occur = None
#      
#     print('PMI Graph node number: %s'%(pmi_graph.number_of_nodes()))
#     print('PMI Graph edge number: %s'%(pmi_graph.number_of_edges()))
#      
#      
#     return (RWR(pmi_graph, None, 0.03 , 800, 0.0000001), docs_bigramSet, fredist)
     
    
    
def first_graph(stree,pat_date_dict):
    
    f = open('first_graph','w')
    

    date_dict = {}
    
    for pat in stree.nodes():
        date = pat_date_dict[pat]
        
        if date not in date_dict:
            date_dict[date] = [pat]
        else:
            date_dict[date].append(pat)
        
    
    count=0    
    for date in sort_date(date_dict.keys()):
        f.write('sankey.stack({},{});\n'.format(count,list(date_dict[date])))
        count+=1
            
            
    edge_arr = []
    
    #s = ''
    for (src,dst) in stree.edges():
        edge_arr.append([src,5,dst])
        #s+='["{}", 5 ,"{}"],'.format(src, dst)    
        
    #f.write('sankey.setData([{}]);'.format(s[:-1]))
    f.write('sankey.setData('+str(edge_arr)+');')

    f.close()
    
    
"""
# {pat:date}
pat_date_dict = {}
    
# {pat:[kind]}
pat_groups_dict = {}
""" 
def merge(stree, pat_date_dict , pat_groups_dict):
    
    buckets = {}
    links = {}
       
    for (src,dst) in stree.edges():
           
        _src_date = pat_date_dict[src]
        _src_groups = pat_groups_dict[src]
        _src_indices = []
           
        _dst_date = pat_date_dict[dst]
        _dst_groups = pat_groups_dict[dst]
        _dst_indices = []
       
        # src 
        if _src_date in buckets:
            for _src_group in _src_groups:
                _src_indices.append('{} {}'.format(_src_date, _src_group)) 
                if _src_group in buckets[_src_date]:
                    buckets[_src_date][_src_group].append(src)
                else:
                    buckets[_src_date][_src_group] = [src]
        else:
            buckets[_src_date] = {}
            for _src_group in _src_groups:
                _src_indices.append('{} {}'.format(_src_date, _src_group))
                buckets[_src_date][_src_group] = [src]
                   
           
        # dst 
        if _dst_date in buckets:
            for _dst_group in _dst_groups:
                _dst_indices.append('{} {}'.format(_dst_date, _dst_group)) 
                if _dst_group in buckets[_dst_date]:
                    buckets[_dst_date][_dst_group].append(dst)
                else:
                    buckets[_dst_date][_dst_group] = [dst]
        else:
            buckets[_dst_date] = {}
            for _dst_group in _dst_groups:
                _dst_indices.append('{} {}'.format(_dst_date, _dst_group))
                buckets[_dst_date][_dst_group] = [dst]
           
           
       
        for _src_index in _src_indices:
            for  _dst_index in _dst_indices:
                key = '{}<=>{}'.format(_src_index, _dst_index)
                #rkey = '{}<=>{}'.format(_dst_index, _src_index)
               
                if key in links:
                    links[key] += 1
#                 elif rkey in links:
#                     links[rkey] += 5
                else:
                    links[key] = 1
    
    
    return (buckets, links)
    
    
def buildGoogleChartJson(links, tags):
    
    _TOP_NUM = 5
    
    json = []
    
    for key in links:
          
        _src = key.split('<=>')[0]
        _dst = key.split('<=>')[1]
        
        if _src is not _dst:
#         _src__date = _src.split(' ')[0]
#         _src__group = _src.split(' ')[1]
#         
#         _dst__date = _dst.split(' ')[0]
#         _dst__group = _dst.split(' ')[1]
        
#         text = (str(buckets[_src__date][_src__group])[1:-1].replace('\'','').replace(',', '\n').strip()
#                 + '-----------'
#                 + str(buckets[_src__date][_src__group])[1:-1].replace('\'','').replace(',', '\n').strip())

            text = ''
            count = 0
            for word, value in sorted(tags[_src].items(), key=lambda x: x[1], reverse=True):
                if count > _TOP_NUM:
                    break 
                text += word+':'+str(value)+' '
                count+=1
                
            text += '<br>--------------------<br>'
            
            count = 0
            for word, value in sorted(tags[_dst].items(), key=lambda x: x[1], reverse=True):
                if count > _TOP_NUM:
                    break
                text += word+':'+str(value)+' '
                count+=1
                
            json.append([_src, _dst , links[key], text])
        
        
        else:
            pass  
        
    
    sorted_json = sorted(json, key=lambda x: datetime.datetime.strptime(x[0].split(' ')[0], '%Y-%m'))
    
    
    #fix google chart no sort with timeline
    timeline = set()
    groups = set()
    for entry in sorted_json:
        timeline.add(entry[0].split(' ')[0])
        timeline.add(entry[1].split(' ')[0])
        groups.add(entry[0])
        groups.add(entry[1])
        
    timeline = sorted(timeline, key=lambda x: datetime.datetime.strptime(x, '%Y-%m'))
      
    for i,current_time in enumerate(list(timeline)):
        try :
            next_time = timeline[i+1]
        except IndexError:
            continue
          
        _src_set = set()
        _dst_set = set() 
          
        for entry in groups:
            if current_time in entry:
                _src_set.add(entry)
            elif next_time in entry:
                _dst_set.add(entry)
            else:
                pass
              
        for _src in _src_set:
            for _dst in _dst_set:
                sorted_json.append([_src, _dst , 0.005, '->'])
        
    
    # output json file for google chart
    output = '[\n' 
    for (src, dst, wight, text) in sorted_json:
        output += '["{}", "{}", {}, "{}"]\n,'.format(src, dst, wight, text)
        
    output = output[:-1]+'\n]'
    
    f = open('data.json','w')
    f.write(output)
    f.close()
    
    
def buildBi_sankeyJson(buckets, links, tags, CPC, _TOP_NUM, _output_path, _target_cpc_code=None):
    
    nodes_json = []
    links_json = []
    # restore the id of nodes
    nodeDict = {}
    
    
    #child id
    c_id = 1
    for i,date in enumerate(buckets):
        #parent id
        p_id = 'p' + str(i)
        nodeDict[date] = p_id
        nodes_json.append({'type': date ,'id': p_id, 'parent': None, 'name': date })
    
        for cpc_code in buckets[date]:
            
            name = date + ' ' + cpc_code
            
            text = ''
            count = 0
            for word, value in sorted(tags[name].items(), key=lambda x: x[1], reverse=True):
                if count > _TOP_NUM:
                    break 
                text += word+':'+str(value)+'  '
                count+=1
                
            main_code = re.sub('(\d+)\/.+', '\g<1>/00', cpc_code)
                
            group_name = ''
            if main_code in CPC:
                if cpc_code in CPC[main_code][1]:
                    #group_name = '{}\n ∟  {}'.format(CPC[main_code][0], CPC[main_code][1][cpc_code].strip())
                    group_name = CPC[main_code][1][cpc_code].strip()
                else:
                    group_name = CPC[main_code][0].strip()
                
            
            nodes_json.append({"type": date ,'id': c_id, 'parent': p_id, 'name': '[{}]'.format(cpc_code) , 'CPC_code': cpc_code,'text': text})
            nodeDict[name] = c_id
            c_id+=1
            
#             if _target_cpc_code is not None: 
#                 if _target_cpc_code == cpc_code:
#                     print(1)
#                     name = date + ' ' + cpc_code
#             
#                     text = ''
#                     count = 0
#                     for word, value in sorted(tags[name].items(), key=lambda x: x[1], reverse=True):
#                         if count > _TOP_NUM:
#                             break 
#                         text += word+':'+str(value)+'  '
#                         count+=1
#                     
#                     main_code = re.sub('(\d+)\/.+', '\g<1>/00', cpc_code)
#                     
#                     group_name = ''
#                     if main_code in CPC:
#                         if cpc_code in CPC[main_code][1]:
#                             group_name = '{}\n ∟  {}'.format(CPC[main_code][0], CPC[main_code][1][cpc_code].strip())
#                         else:
#                             group_name = CPC[main_code][0].strip()
#                     
#                     
#                     nodes_json.append({"type": date ,'id': c_id, 'parent': p_id, 'group_name': group_name , 'CPC_code': cpc_code,'text': text})
#                     nodeDict[name] = c_id
#                     c_id+=1
#                 
#                 
#             else:
#                 name = date + ' ' + cpc_code
#             
#                 text = ''
#                 count = 0
#                 for word, value in sorted(tags[name].items(), key=lambda x: x[1], reverse=True):
#                     if count > _TOP_NUM:
#                         break 
#                     text += word+':'+str(value)+'  '
#                     count+=1
#                 
#                 main_code = re.sub('(\d+)\/.+', '\g<1>/00', cpc_code)
#                 
#                 group_name = ''
#                 if main_code in CPC:
#                     if cpc_code in CPC[main_code][1]:
#                         group_name = '{}\n ∟  {}'.format(CPC[main_code][0], CPC[main_code][1][cpc_code].strip())
#                     else:
#                         group_name = CPC[main_code][0].strip()
#                 
#                 
#                 nodes_json.append({"type": date ,'id': c_id, 'parent': p_id, 'group_name': group_name , 'CPC_code': cpc_code,'text': text})
#                 nodeDict[name] = c_id
#                 c_id+=1
    
    
    for key in links:
        _src = key.split('<=>')[0]
        _dst = key.split('<=>')[1]
        
        if _target_cpc_code is not None:
            _src_cpc_code = _src.split(' ')[1]
            _dst_cpc_code = _dst.split(' ')[1]
            
            if _src_cpc_code == _target_cpc_code or _dst_cpc_code == _target_cpc_code:
                
                links_json.append({'source': nodeDict[_src], 'target': nodeDict[_dst], 'value': links[key]*0.5})
        else:
            links_json.append({'source': nodeDict[_src], 'target': nodeDict[_dst], 'value': links[key]*0.5})
    
    
    
    """ CPC code schema: main_group/sub_group
        we must merge the same main_group and the bucket as only maingroup
        because buckets as main_group/sub_group are too mess.
        """
    """
    c_id = 1
    for i,date in enumerate(buckets):
        #parent id
        p_id = 'p' + str(i)
        nodeDict[date] = p_id
        nodes_json.append({'type': date ,'id': p_id, 'parent': None, 'name': date })
        
    
        maingroup_buckets = {}
        for cpc_code in buckets[date]:
            
            name = date + ' ' + cpc_code
            main_code = re.sub('(\d+)\/.+', '\g<1>/00', cpc_code)
            
            # Extracting top-N keyword and subgroup name to compose text in main_group/sub_group 
            text=''
            if main_code in CPC:
                try:
                    text = 'CPC code: {}\nName:{}\nKeyword:\n-------------\n'.format(cpc_code, CPC[main_code][1][cpc_code].strip())
                except KeyError:
                    text = 'CPC code: {}\nName:{}\nKeyword:\n-------------\n'.format(cpc_code, CPC[main_code][0].strip())
            count = 0
            for word, value in sorted(tags[name].items(), key=lambda x: x[1], reverse=True):
                if count > _TOP_NUM:
                    break 
                text += word+':'+str(value)+'  '
                count+=1
        
            if main_code in maingroup_buckets:
                maingroup_buckets[main_code]['text']+='\n'+text
            else:
                if main_code in CPC:
                    group_name = CPC[main_code][0].strip()
                    code = '{}/00'.format(main_code)
                    maingroup_buckets[main_code]={'group_name':group_name, 'date':date, 'cpc_code':code, 'text':text}
                
                
        for main_group in maingroup_buckets:
            date = maingroup_buckets[main_group]['date']
            group_name = maingroup_buckets[main_group]['group_name']
            cpc_code = maingroup_buckets[main_group]['cpc_code']
            text = maingroup_buckets[main_group]['text']
            
            node = '{} {}/00'.format(date, main_group)
            
            nodes_json.append({"type": date ,'id': c_id, 'parent': p_id, 'group_name': group_name , 'CPC_code': cpc_code,'text': text})
            nodeDict[node] = c_id
            c_id+=1
                
    
    new_links = {}
    for key in links:
        #schema: start~end maingroup
        _src = key.split('<=>')[0].split('/')[0]
        _dst = key.split('<=>')[1].split('/')[0]
        if (_src, _dst) in new_links:
            new_links[(_src, _dst)]+=links[key]
        else:
            new_links[(_src, _dst)]=links[key]


    for (_src, _dst) in new_links:
        _src = '{}/00'.format(_src)
        _dst = '{}/00'.format(_dst)
        links_json.append({'source': nodeDict[_src], 'target': nodeDict[_dst], 'value': links[key]})
    """
    
    f = open(_output_path+'bi_sankey_nodes.json','w')
    f.write(json.dumps(nodes_json))
    f.close()
     
    f = open(_output_path+'bi_sankey_links.json','w')
    f.write(json.dumps(links_json))
    f.close()
    

def _statics_correlation(links, _OUTPUT_PATH):
    
    corDict = {}
    for key,value in links.items():
        tmp = key.split('<=>')
        _src = tmp[0].split(' ')[1]
        _dst = tmp[1].split(' ')[1]
        
        if _src != _dst:
            if _src in corDict:
                if _dst in corDict[_src]:
                    corDict[_src][_dst]+=value
                else:
                    corDict[_src][_dst]=value
            else:
                corDict[_src]={_dst:value}
            
            if _dst in corDict:
                if _src in corDict[_dst]:
                    corDict[_dst][_src]+=value
                else:
                    corDict[_dst][_src]=value
            else:
                corDict[_dst]={_src:value}
                
    
    for group in corDict:
        sum = 0
        for word,val in corDict[group].items():
            sum+=val
        print(group, sum)
#     for group in corDict:
#         f = open('{}/{}.csv'.format(_OUTPUT_PATH, group.replace('/','_')),mode='w',encoding='utf-8')
#         f.write('\,count\n')
#         for g_j, value in sorted(corDict[group].items(), key=lambda x: x[1], reverse=True):
#             f.write('{},{}\n'.format(g_j.replace('/','_'),value))
#         f.close

def statics_specific_phrase(buckets_path, tags_path, targetTermList, _OUTPUT_PATH):
    
    with open(buckets_path, mode='r') as f:
        buckets=json.loads(f.read())
    with open(tags_path, mode='r') as f:
        tags=json.loads(f.read())
    
    
    rows = {}
    
    for date in buckets:
        year = int(date[0:4])
        
        #phraseDict = {}
        if year not in rows:
            rows[year] = {}
        
        for group in buckets[date]:
            name = date + ' ' + group
            for word,value in tags[name].items():
                for target in targetTermList:
                    
                    if type(target) is list:
                        target_term = target[0]
                        
                        for synonymous in target:
                            if synonymous.lower() == word.lower():
                                print('{}--->{},{}'.format(word, target_term, value))
                                if target_term in rows[year]:
                                    rows[year][target_term].append(value)
                    
                                else:
                                    rows[year][target_term]=[value]
                                break
                            else:
                                if ' ' not in synonymous:
                                    if any(synonymous.lower() == wordsplit for wordsplit in word.lower().split(' ')):
                                        print('{}--->{},{}'.format(word, target_term, value))
                                        if target_term in rows[year]:
                                            rows[year][target_term].append(value)
                                        else:
                                            rows[year][target_term]=[value]
                                        break
                            
                        
                    elif type(target) is str:
                        target_term = target
                        if target_term.lower() == word.lower():
                            print('{}--->{},{}'.format(word, target_term, value))
                            if target_term in rows[year]:
                                rows[year][target_term].append(value)
                
                            else:
                                rows[year][target_term]=[value]
                            break
                        else:
                            if ' ' not in target_term:
                                if any(target_term.lower() == wordsplit for wordsplit in word.lower().split(' ')):
                                    print('{}--->{},{}'.format(word, target_term, value))
                                    if target_term in rows[year]:
                                        rows[year][target_term].append(value)
                                    else:
                                        rows[year][target_term]=[value]
                                    break
                    else:
                        print('error')
                    
                                                     
        #rows[date] = phraseDict
    

    with open(_OUTPUT_PATH, mode='w') as f:

        f.write('/,')
        for target in targetTermList:
            if type(target) is list:
                f.write(target[0]+',')
            elif type(target) is str:
                f.write(target+',')
            else:
                print('error')
            
            
        f.write('\n')
         
        #for date in sorted(rows.keys(), key=lambda x: datetime.datetime.strptime(x.split('~')[0], '%Y-%m')):
        for date in sorted(rows.keys()):
            f.write('{},'.format(date))
            for target in targetTermList:
                target_term = ''
                if type(target) is list:
                    target_term = target[0]
                elif type(target) is str:
                    target_term = target
                else:
                    print('error')
                
                if target_term in rows[date]:
                    avg = TRIMMEAN(rows[date][target_term])
                    f.write('{},'.format(avg))
                else:
                    f.write('0,')
                     
            f.write('\n')  
         
         


def _statics_phrase(buckets_path, tags_path, _OUTPUT_PATH):
    
    
    with open(buckets_path, mode='r') as f:
        buckets=json.loads(f.read())
    with open(tags_path, mode='r') as f:
        tags=json.loads(f.read())
    
    _TOP_NUM = 200
    rows = {}
    
#     sumDict={}
#     """   the statics timeline of phrase in all group """
#     for date in buckets:
#         phraseDict = {}
#         for group in buckets[date]:
#             name = date + ' ' + group
#              
#             for word,value in tags[name].items():
#                 if word in phraseDict:
#                     phraseDict[word][0]+=value
#                     phraseDict[word][1]+=1
#                 else:
#                     phraseDict[word]=[value,1]
#                      
#                 if word in sumDict:
#                     sumDict[word]+=value
#                 else:
#                     sumDict[word]=value
#         rows[date] = phraseDict
#                  
#      
#     phraseSet=set()
#     count = 0
#     for word, value in sorted(sumDict.items(), key=lambda x: x[1], reverse=True):
#         if count > _TOP_NUM:
#             break
#         phraseSet.add(word)
#         count+=1
#              
#              
#     phraseList=list(phraseSet)
#      
#      
#     f = open('{}the statics timeline of phrase in all group.csv'.format(_OUTPUT_PATH), mode='w',encoding='utf-8')
#     f.write('/,')
#     for phrase in phraseList:
#         f.write(phrase+',')
#          
#     f.write('\n')
#     
#     
#     for date in sorted(rows.keys(), key=lambda x: datetime.datetime.strptime(x.split('~')[0], '%Y-%m')):
#         f.write(date+',')
#         for phrase in phraseList:
#             if phrase in rows[date]:
#                 f.write('{},'.format(rows[date][phrase][0]/rows[date][phrase][1]))
#             else:
#                 f.write('0,')
#                  
#         f.write('\n')  
#          
#     f.close()    



    filterPhrase = ['netwrok A','A wireless','Method apparatus','present invention','system A',
                    'A method','Method system','method system','system method','Methods apparatus',
                    'System method','invention method','network A','Systems methods','method claim','claim wherein',
                    'system claim','claim further','medium claim','object object']
#  
    """   the statics timeline of phrase each group """
    groupDict = {}
    for bucket in tags:
        tmp = bucket.split(' ')
        time = tmp[0]
        group = tmp[1].split('/')[0]
        #group = tmp[1]
       
        if group in groupDict:
            #groupDict[group][time] = tags[bucket]
            if time in groupDict[group]:
                for word,value in tags[bucket].items():
                    if word in groupDict[group][time]:
                        groupDict[group][time][word].append(value)
                         
                    else:
                        groupDict[group][time][word]=[value]
            else:
                groupDict[group][time] = {}
                for word,value in tags[bucket].items():
                    groupDict[group][time][word]=[value]
                 
        else:
            groupDict[group]={time:{}}
            for word,value in tags[bucket].items():
                    groupDict[group][time][word]=[value]
           
       
    for group in groupDict:
           
        f = open('{}the statics of {}.csv'.format(_OUTPUT_PATH, group.replace('/','_')),mode='w',encoding='utf-8')
           
        phraseSum={}
        """ 常出現 """
        #phraseHits={}
        for time in groupDict[group]:
            for word,value in groupDict[group][time].items():
                if word not in filterPhrase:
                    if word in phraseSum:
                         
                        phraseSum[word]+=value
                        #phraseHits[word]+=1
                    else:
                        phraseSum[word]=value
                        #phraseHits[word]=1
                       
        #print(phraseSum)
                       
        phraseList = []
        count = 0
        #for word, value in sorted(phraseHits.items(), key=lambda x: x[1], reverse=True):
        for word, value in sorted(phraseSum.items(), key=lambda x: x[1], reverse=True):
            if count > _TOP_NUM:
                break
            phraseList.append(word)
            count+=1
           
           
        f.write('/,')
        for word in phraseList:
            f.write(word+',')
        f.write('\n')
           
        for time in sorted(groupDict[group].keys(), key=lambda x: datetime.datetime.strptime(x.split('~')[0], '%Y-%m')):
            f.write(time+',')
            for word in phraseList:
                if word in groupDict[group][time]:
                    f.write('{},'.format(TRIMMEAN(groupDict[group][time][word])))
                else:
                    f.write('0,')
            f.write('\n')
               
        f.close()
    
    
def newScore(TFIDF_dict, PMI_dict, weight):
    
    result = {}
    
    _TFIDF_WEIGHT = weight
    _PMI_WEIGHT = 1-weight
    
    
    if len(PMI_dict) > 0:
    
        _PMI_MAX = max(PMI_dict.values())
        _PMI_MIN = min(PMI_dict.values())
        _PMI_INTVAL = _PMI_MAX-_PMI_MIN
        #print(_PMI_MAX,_PMI_MIN)
        
        _TFIDF_MAX = max(TFIDF_dict.values())
        _TFIDF_MIN = min(TFIDF_dict.values())
        _TFIDF_INTVAL = _TFIDF_MAX-_TFIDF_MIN
        
#         print('TFIDF intval: {}'.format(_TFIDF_INTVAL))
#         print('RWR intval: {}'.format(_PMI_INTVAL))
#     
#         if _TFIDF_INTVAL == 0:
#             print(TFIDF_dict)
#         
#         if _PMI_INTVAL == 0:
#             print(PMI_dict)
        
        for word,value in TFIDF_dict.items():
            try:
                score = 0
                if _PMI_INTVAL == 0:
                    try:
                        score = _TFIDF_WEIGHT*(value-_TFIDF_MIN)/_TFIDF_INTVAL + _PMI_WEIGHT
                    except ZeroDivisionError:
                        score = 0
                elif _TFIDF_INTVAL == 0:
                    score = _TFIDF_WEIGHT + _PMI_WEIGHT*(PMI_dict[word]-_PMI_MIN)/_PMI_INTVAL
                else:
                    
                    score = _TFIDF_WEIGHT*(value-_TFIDF_MIN)/(_TFIDF_INTVAL) + _PMI_WEIGHT*(PMI_dict[word]-_PMI_MIN)/(_PMI_INTVAL)
                result[word]=score
                
            except KeyError:
                if _TFIDF_MAX-_TFIDF_MIN>0:
                    score = (value-_TFIDF_MIN)/(_TFIDF_MAX-_TFIDF_MIN)
                    result[word]=score
                else:
                    result[word]=0
    return result
    
    
def ROUGE(docs_bigrams, data,_TOP_NUM):
    
    _REF_TOTAL_GRAMS = 0
        
    for doc_bigrams in docs_bigrams:
        _REF_TOTAL_GRAMS += len(doc_bigrams)
    
    i = 0
    hits = 0
    for word, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
        if i > _TOP_NUM:
            break 

        for doc_bigrams in docs_bigrams:
            for bigram in doc_bigrams:
                if word is bigram:
                    hits+=1
        i+=1
    
    return hits/_REF_TOTAL_GRAMS

def generateTargetTag(bucket_path, target_group, output_tag_txt_path):
    
    with open(bucket_path, mode='r') as f:
        buckets=json.loads(f.read())
    
    
    sql = mysql()
    sql.connect()
    tags = {}

    TFIDF = {}
    RWRprob = {}
    
    for date in sorted(buckets.keys()):
        
        TFIDF[date] = {}
        RWRprob[date] = {}
        
        for group in buckets[date]:
            
            if group.split('/')[0] == target_group:
            
                print('[%s %s]'%(date,group))
                docs = []
                for patNo,title,abstract,description,claim,assignee in sql.getPatent_content(set(buckets[date][group])):
                    text = re.sub('\d+\.', ' ', '%s %s' %(title,abstract))
                    docs.append(text)
    
                
                (counts, docs_bigramSet, fredist) = PMI(docs)
                docs = None
                  
                _DOCS_NUM = len(docs_bigramSet)
                
                bi_tfidf = {}
                for word,freq in fredist.items():
                    try:
                        count = 0
                        count = sum(1 for bigramSet in docs_bigramSet if word in bigramSet)
                        """
                        for doc_bigrams in docs_bigrams:
                            if word in doc_bigrams:
                                count+=1
                        """ 
                        idf = math.log10(_DOCS_NUM/count) + 0.01
                      
                        #print(idf,bi_TFdist.freq(word))
                        value = freq*idf
                        bi_tfidf[word] = value 
                          
                    except AttributeError:
                        pass
                 
                data = newScore(bi_tfidf, counts)
                tags[date+' '+group] = data
                
                
                TFIDF[date][group] = bi_tfidf
                RWRprob[date][group] = counts
                 
                
                print('-------------------------')
             
    sql.close
    
    with open(output_tag_txt_path, mode='w') as f:
        
        for tag in tags:
            f.write('{}\n-------------------------\n'.format(tag))
            i = 0
            for word, value in sorted(tags[tag].items(), key=lambda x: x[1], reverse=True):
                if i > 50:
                    break 
                text += word+':'+str(value)+'  '
                f.write('{} : {}\n'.format(word.encode(encoding='utf_8', errors='strict'), value))
                i+=1

            f.write('\n\n')


    

def generateTag(buckets, output_tag_path, output_tfidf_path, output_rwr_path):
    
    sql = mysql()
    sql.connect()
    tags = {}

    TFIDF = {}
    RWRprob = {}
    
#     iter = 0
#     tfidf_rouge = 0
#     rwr_rouge = 0
#     both_rouge = 0
    
#     task_num = 0
#     for date in buckets:
#         for group in buckets[date]:
#             task_num+=1
    
    for date in buckets:
        
        TFIDF[date] = {}
        RWRprob[date] = {}
        
        for group in buckets[date]:
            print('[%s %s]'%(date,group))
            docs = []
            for patNo,title,abstract,description,claim,assignee in sql.getPatent_content(set(buckets[date][group])):
                text = re.sub('\d+\.', ' ', '%s %s %s' %(title,abstract, description))
                docs.append(text)
                text = None
            
            (counts, docs_bigramSet, fredist) = PMI(docs)
            docs = None
              
            _DOCS_NUM = len(docs_bigramSet)
            
            bi_tfidf = {}
            for word,freq in fredist.items():
                try:
                    count = 0
                    count = sum(1 for bigramSet in docs_bigramSet if word in bigramSet)
                    """
                    for doc_bigrams in docs_bigrams:
                        if word in doc_bigrams:
                            count+=1
                    """ 
                    idf = math.log10(_DOCS_NUM/count) + 0.01
                  
                    #print(idf,bi_TFdist.freq(word))
                    value = freq*idf
                    bi_tfidf[word] = value 
                      
                except AttributeError:
                    pass
            
            docs_bigramSet = None
            fredist = None
            
            data = newScore(bi_tfidf, counts, 0.4)
            
            tags[date+' '+group] = data
            TFIDF[date][group] = bi_tfidf
            RWRprob[date][group] = counts
            counts = None
            bi_tfidf = None
            data = None
            
            with open(output_tfidf_path, mode='w') as f:
                f.write(json.dumps(TFIDF))
            
            with open(output_rwr_path, mode='w') as f:
                f.write(json.dumps(RWRprob))
        
            with open(output_tag_path, mode='w') as f:
                f.write(json.dumps(tags))
             
            """ evaluation """
#             tfidf_rouge += ROUGE(docs_bigrams, bi_tfidf, 10)
#             rwr_rouge += ROUGE(docs_bigrams, counts, 50)
#             both_rouge += ROUGE(docs_bigrams, data, 50)
#             iter += 1
#             print('Tasks finished : {} %'.format(round(iter/task_num, 2)*100))
            print('-------------------------')
             
    sql.close

#     print('tfidf ROUGE-2 :%s'%(str(tfidf_rouge/iter)))
#     print('rwr ROUGE-2 :%s'%(str(rwr_rouge/iter)))
#     print('both ROUGE-2 :%s'%(str(both_rouge/iter)))
    
    with open(output_tfidf_path, mode='w') as f:
        f.write(json.dumps(TFIDF))
    
    with open(output_rwr_path, mode='w') as f:
        f.write(json.dumps(RWRprob))
        
    with open(output_tag_path, mode='w') as f:
        f.write(json.dumps(tags))
        
    return tags


def debug(buckets, links, tags):
    
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.debug('-----------------------')
    
    _bucket_set = set()
    _tag_set = set()
    _link_set = set()
    
    for date in buckets:
        for group in buckets[date]:
            _bucket_set.add(date+' '+group)
            
    for key in tags:
        _tag_set.add(key)
    
    for key in links:
        _src = key.split('<=>')[0]
        _dst = key.split('<=>')[1]
        _link_set.add(_src)
        _link_set.add(_dst)
        
    print('bucket number: %s'%(len(_bucket_set)))
    print('tag number: %s'%(len(_tag_set)))
    print('link number: %s'%(len(_link_set)))
    print('bucket == tag ?'+str(all(key in _tag_set for key in _bucket_set)))
    print('bucket == link ?'+str(all(key in _link_set for key in _bucket_set)))
    print('link == tag ?'+str(all(key in _tag_set for key in _link_set)))
    

def company_tech_distribution(bucket_path, target_company, output_path):
    
    with open(bucket_path, mode='r') as f:
        buckets=json.loads(f.read())
    
    sql = mysql()
    sql.connect()
    
    rows = {}
    maingroupSum = {}
    #patentSet = {}

    for date in buckets:
        year = int(date[0:4])
        rows[year] = {}
        #patentSet[year] = {}
        for group in buckets[date]:
            
            #maingroup = group
            maingroup = group.split('/')[0]
            
            for patNo,title,abstract,description,claim,assignee in sql.getPatent_content(set(buckets[date][group])):

                if target_company.lower() in assignee.lower():
                    
#                     if maingroup in patentSet[year]:
#                         patentSet[year][maingroup].append((patNo,title))
#                     else:
#                         patentSet[year][maingroup]=[(patNo,title)]
                    
                    if maingroup in rows[year]:
                        rows[year][maingroup]+=1
                    else:
                        rows[year][maingroup]=1
                        
                    if maingroup in maingroupSum:
                        maingroupSum[maingroup]+=1
                    else:
                        maingroupSum[maingroup]=1
                    
    sql.close()

    sortedMaingroup = sorted(maingroupSum.items(), key=lambda x: x[1], reverse=True)
     
    with open(output_path, mode='w') as f:
           
        f.write('/,')
        for maingroup,value in sortedMaingroup[0:10]:
            f.write(maingroup+',')
        f.write('other\n')
           
        for year in sorted(rows.keys()):
               
            sum = 0
            for maingroup,value in rows[year].items():
                sum+=value
               
            tmp = 0
            f.write('{},'.format(year))
            for maingroup,value in sortedMaingroup[0:10]:
                try:
                    f.write('{},'.format(rows[year][maingroup]*100/sum))
                    tmp+=rows[year][maingroup] 
                except KeyError:
                    f.write('0,')
            try:         
                f.write('{}\n'.format((sum-tmp)*100/sum))
            except ZeroDivisionError:
                f.write('0\n')

#     for year in [2012,2013,2014,2015]:
#         for maingroup,value in sortedMaingroup[0:4]:
#             if rows[year][maingroup] > 0:
#                 print(year,maingroup)
#                 print('----------------------')
#                 for no,title in patentSet[year][maingroup]:
#                     print(no,title)
#                 print('==============================')
        
    
def _statistics_company(stree_nodes, pat_date_dict, pat_groups_dict):
    
    company_rows = {}
    group_rows = {}
    """
    company_rows = {
            '2009':{ company:50 }
            }
    """

    sql = mysql()
    sql.connect()
    
    for patNo,title,abstract,description,claim,assignee in sql.getPatent_content(set(stree_nodes)):
        year = re.sub('(\d+)-\S+', '\g<1>', pat_date_dict[patNo])
        group_list = pat_groups_dict[patNo]
        
#         assignee = assignee.lower().replace('.','')
#         
#         if year in company_rows:
#             if assignee in company_rows[year]:
#                 company_rows[year][assignee]+=1
#             else:
#                 company_rows[year][assignee]=1
#         else:
#             company_rows[year]={assignee:1}
        
        for group in group_list:
            if year in group_rows:
                if group in group_rows[year]:
                    group_rows[year][group]+=1
                else:
                    group_rows[year][group]=1
            else:
                group_rows[year]={group:1}
    
    sql.close()
    
    """ sorted """
#     for year in company_rows: 
#         print(year)
#         print('------------')
#         for key,value in sorted(company_rows[year].items(), key=lambda x: x[1], reverse=True):
#             print('{} {}'.format(key, value))
#     
#     print('=============================================')
    
    for year in group_rows:
        print(year)
        print('------------')
        for key,value in sorted(group_rows[year].items(), key=lambda x: x[1], reverse=True):
            print('{} {}'.format(key, value))
        


def tagToBi_sankeyJson(_buckets_path, _links_path, _tags_path, _CPC_PATH, _TOP_NUM, _output_path, _target_cpc_code):
    
    CPC = load_CPC(_CPC_PATH)
    
    with open(_buckets_path, mode='r') as f:
        buckets=json.loads(f.read())
    with open(_links_path, mode='r') as f:
        links=json.loads(f.read())
    with open(_tags_path, mode='r') as f:
        tags=json.loads(f.read())

    buildBi_sankeyJson(buckets, links, tags, CPC, _TOP_NUM, _output_path, _target_cpc_code)
    
    
def get_evolution():
    
    _KIND = 'G06T' 
    _START = '2009-01-01'
    _END = '2015-12-31'
    
    logging.basicConfig(filename='pyNetwork.log')
    G=nx.DiGraph()
    sql = mysql()
    sql.connect()
    

    for patNO, relNO in sql.getEdges(_START, _END, _KIND):
        G.add_edge(relNO, patNO)
        
        """
        if patNO in nodes:
            nodes[patNO]['groups'].append('{}/{}'.format(maingroup, subgroup)) 
        else:
            nodes[patNO] = {'date':patDate, 'groups':['{}/{}'.format(maingroup, subgroup)]}
        """
     
    # {pat:date}
    pat_date_dict = {}
    
    # {pat:[kind]}
    pat_groups_dict = {}
        
    for patNO, date, maingroup, subgroup in sql.getNodes(_KIND):
        
        if patNO not in pat_date_dict:
            pat_date_dict[patNO] = str(date)[:-3]
            """
            if date.month in range(1,3):
                pat_date_dict[patNO] = '{}-03'.format(date.year)
            elif date.month in range(3,6):
                pat_date_dict[patNO] = '{}-06'.format(date.year)
            elif date.month in range(6,9):
                pat_date_dict[patNO] = '{}-09'.format(date.year)
            else:
                pat_date_dict[patNO] = '{}-12'.format(date.year)
            """
            if date.month in range(1,6):
                pat_date_dict[patNO] = '{}-01~{}-05'.format(date.year,date.year)
            else:
                pat_date_dict[patNO] = '{}-06~{}-12'.format(date.year,date.year)
                
        
#         if patNO in pat_groups_dict:
#             pat_groups_dict[patNO].append('{}/*'.format(maingroup)) 
#         else:
#             pat_groups_dict[patNO] = ['{}/*'.format(maingroup)]
#         
        if patNO in pat_groups_dict:
            pat_groups_dict[patNO].append('{}/{}'.format(maingroup, subgroup)) 
        else:
            pat_groups_dict[patNO] = ['{}/{}'.format(maingroup, subgroup)]
    
    
#     for pat in pat_date_dict:
#         print(pat,pat_date_dict[pat])
    
    """
    #update nodes attributes
    for key in nodes:
        G.add_node(key, date=nodes[key]['date'], groups=nodes[key]['groups'])
    """ 
    
    print('Node number : %d' %(G.number_of_nodes()))
    print('Edge number : %d' %(G.number_of_edges()))
    #keepMaint = sql.getStatistics_fromMaintFeeEvents(set(G.nodes()),None)
    
    domi_set = nx.dominating_set(G)
    print('Dominating size : %d' %(len(domi_set)))
    
    stree = di_steiner_tree(G,domi_set)
    print('STree Node number : %d' %(stree.number_of_nodes()))
    print('STree Edge number : %d' %(stree.number_of_edges()))
    #sql.getStatistics_fromMaintFeeEvents(set(stree.nodes()), keepMaint)
    sql.close()
    
    #_statistics_company(stree.nodes(), pat_date_dict, pat_groups_dict)
    
    (buckets, links) = merge(stree, pat_date_dict, pat_groups_dict)
    
    with open('G06T/buckets', mode='w') as f:
        f.write(json.dumps(buckets))
    
    with open('G06T/links', mode='w') as f:
        f.write(json.dumps(links))
    
    tags = generateTag(buckets)
    
    with open('G06T/tags', mode='w') as f:
        f.write(json.dumps(tags))
    
    #_statics_phrase(buckets, links, tags)
#     
#     debug(buckets, links, tags)
#     
#     buildGoogleChartJson(links, tags)
#     
    #buildBi_sankeyJson(buckets, links, tags, 50)
    
    
    """  all group TFIDF """
#     groups = {}
#     for patno in stree.nodes():
#         date = pat_date_dict[patno]
#         for kind in pat_groups_dict[patno]:
#               
#             if date in groups:
#                 if kind in groups[date]:
#                     groups[date][kind].append(patno)
#                 else:
#                     groups[date] = {kind:[patno]}
#             else:
#                 groups[date] = {kind:[patno]}
#     
#     sql.connect()
#     for date in groups:
#         for kind in groups[date]:
#             print(kind)
#             docs = []
#             for title,abstract,description,claim in sql.getPatent_content(set(groups[date][kind])):
#                 docs.append('%s %s %s %s' %(title,abstract,claim))
#             tfidf(docs)
#             
#     sql.close
    

    #first_graph(stree,pat_date_dict)
    
#     f = open('tmp02','w')
#     """ merge """
#     # {date:{group:[patno]}}
#     buckets = {}
#     # {('date-group','date-group'):edge size}
#     links = {}
#       
#       
#     for (src,dst) in stree.edges():
#           
#         _src_date = pat_date_dict[src]
#         _src_groups = pat_groups_dict[src]
#         _src_indices = []
#           
#         _dst_date = pat_date_dict[dst]
#         _dst_groups = pat_groups_dict[dst]
#         _dst_indices = []
#       
#         # src 
#         if _src_date in buckets:
#             for _src_group in _src_groups:
#                 _src_indices.append('{} {}'.format(_src_date, _src_group)) 
#                 if _src_group in buckets[_src_date]:
#                     buckets[_src_date][_src_group].append(src)
#                 else:
#                     buckets[_src_date][_src_group] = [src]
#         else:
#             for _src_group in _src_groups:
#                 _src_indices.append('{} {}'.format(_src_date, _src_group))
#                 buckets[_src_date] = {_src_group:[src]}
#                   
#           
#         # dst 
#         if _dst_date in buckets:
#             for _dst_group in _dst_groups:
#                 _dst_indices.append('{} {}'.format(_dst_date, _dst_group)) 
#                 if _dst_group in buckets[_dst_date]:
#                     buckets[_dst_date][_dst_group].append(dst)
#                 else:
#                     buckets[_dst_date][_dst_group] = [dst]
#         else:
#             for _dst_group in _dst_groups:
#                 _dst_indices.append('{} {}'.format(_dst_date, _dst_group))
#                 buckets[_dst_date] = {_dst_group:[dst]}
#           
#           
#       
#         for _src_index in _src_indices:
#             for  _dst_index in _dst_indices:
#                 key = '{}<=>{}'.format(_src_index, _dst_index)
#                 rkey = '{}<=>{}'.format(_dst_index, _src_index)
#           
#                 if key in links:
#                     links[key] += 5
#                 elif rkey in links:
#                     links[rkey] += 5
#                 else:
#                     links[key] = 5
#          
#      
#     """    old -> new
#     {group:[{date:[(word,freq), (word,freq),...]}, ...]} 
#     """
#     word_vectors = {}
#     #count=0
#     for date in buckets:
#         tmp = []
#         for group in buckets[date]:
#             tmp.append(str(buckets[date][group])[1:-1].replace('\'','').replace(',', '\n').strip())
#               
#             _bigram_freq_dist = bigramFreqDist(set(buckets[date][group]))
#               
#             if group in word_vectors:
#                 word_vectors[group][date] = _bigram_freq_dist
#             else:
#                 word_vectors[group] = {date:_bigram_freq_dist}
#                   
#                   
#         #f.write('sankey.stack({},{});\n'.format(count, tmp))
#         #count+=1
#           
#       
#     """  acceleration  """
#     blocks = {}
#     for group in word_vectors:
#         #sort date
#         sort_indeics = sort_date(word_vectors[group].keys()) 
#         #first
#         date = sort_indeics[0]
#           
#         blocks[date] = {group:word_vectors[group][date].most_common(5)}
#         print(sort_indeics)
#           
#         for i,j in enumerate(sort_indeics[:-1]):
#             _next = sort_indeics[i+1]
#             _curret = str(sort_indeics[i])
#             tmp = nltk.FreqDist()
#               
#             for word in word_vectors[group][_next]:  
#                 frequency = word_vectors[group][_next].freq(word)
#                 print(word,frequency)
#                 try:
#                     tmp[word] = frequency - word_vectors[group][_curret].freq(word)
#                 except KeyError:
#                     tmp[word] = frequency
#                       
#             blocks[_next] = {group:tmp.most_common(5)}
#       
#     print(blocks)
#      
#     count = 0
#     for date in blocks:
#         arr = []
#         for group in blocks[date]:
#             s=''            
#             for (first,second),freq in blocks[date][group]:
#                 #print(term)
#                 s += first+' '+second+'\n'
#             arr.append(s)
#             blocks[date][group].append(s)
#         f.write('sankey.stack({},{});\n'.format(count, arr))
#         count+=1
#          
#      
#     edge_arr = []  
#     for key in links:
#          
#         _src_split = key.split('<=>')[0].split(' ')
#         _dst_split = key.split('<=>')[1].split(' ')
#         print(_src_split[0], _src_split[1])
#         print(_dst_split[0], _dst_split[1])
#         print(links[key])
#         print('-----------------------------')
#          
#         try: 
#             #src = str(buckets[_src_split[0]][_src_split[1]])[1:-1].replace('\'','').replace(',', '\n').strip()
#             #dst = str(buckets[_dst_split[0]][_dst_split[1]])[1:-1].replace('\'','').replace(',', '\n').strip()
#             src = str(blocks[_src_split[0]][_src_split[1]][-1])
#             dst = str(blocks[_dst_split[0]][_dst_split[1]][-1])
#         except KeyError:
#             continue
#          
#         edge_arr.append([src, links[key], dst])
#          
#      
#     f.write('sankey.setData({});'.format(str(edge_arr)))
#      
#     f.close()

def weigh_test_tfidf_rwr(tfidf_path, rwr_path, weight, output_path):
    
    with open(tfidf_path, mode='r') as f:
        tfidfDict=json.loads(f.read())
    
    with open(rwr_path, mode='r') as f:
        rwrDict=json.loads(f.read())
    
    tags = {}
    
    for date in tfidfDict:
        for group in tfidfDict[date]:
            
            print('[%s %s]'%(date,group))
                
            data = newScore(tfidfDict[date][group], rwrDict[date][group], weight)
            tags[date+' '+group] = data
                    
            print('-------------------------')
    
    
    with open(output_path, mode='w') as f:
        f.write(json.dumps(tags))
    
    
def getPatDocument(bucket_path, target_group, output_path):
    
    with open(bucket_path, mode='r') as f:
        buckets=json.loads(f.read())
        
        
    fw = open(output_path, mode='w')
    
    sql = mysql()
    sql.connect()
    
    for date in sorted(buckets.keys()):
        for group in buckets[date]:
            if group.split('/')[0] == target_group:
                fw.write('{} {}\n'.format(date, group))
                fw.write('-------------------------\n')
                for patNo,title,abstract,description,claim,assignee in sql.getPatent_content(set(buckets[date][group])):
                    fw.write('{}, {}, {}\n'.format(assignee, patNo, title))
                fw.write('\n')
    sql.close
    
    fw.close
    
def bucketToTag(bucket_path, output_tag_path, output_tfidf_path, output_rwr_path):
    
    with open(bucket_path, mode='r') as f:
        buckets=json.loads(f.read())
    
    generateTag(buckets, output_tag_path, output_tfidf_path, output_rwr_path)


def calculateKeywordCoverage(tags_path, topN):
    """  計算每一個主題下擷取的關鍵字詞佔該主題專利文件中的字詞比例     """
    
    stopword = set(['methods','method','invention','inventions','apparatus','first','second','present','third','plurality'])
    topicKeywordDict = {}
    
    with open(tags_path, mode='r') as f:
        tags=json.loads(f.read())
    
    for key in tags:
        _tempTopic = key.split(" ")[1]
        _tempKeywordSet = set()
        
        count = 0
        for keyword, value in sorted(tags[key].items(), key=lambda x: x[1], reverse=True):
            if count < topN: 
                _tempKeywordSet.add(keyword)
                count+=1
            else:
                break
        
        if _tempTopic in topicKeywordDict:
            topicKeywordDict[_tempTopic]=topicKeywordDict[_tempTopic]|_tempKeywordSet
        else:
            #topicDict[_tempTopic] = set()
            topicKeywordDict[_tempTopic] = _tempKeywordSet
            
            
    
    """   抓專利全內容   """
    _KIND = 'H04W' 
    _START = '2009-01-01'
    _END = '2015-12-31'
    
    sql = mysql()
    sql.connect()

    topicPatNoDict = {}
    
    for patNO, date, maingroup, subgroup in sql.getNodes(_KIND):
        _tempTopic = maingroup+'/'+subgroup
        
        if _tempTopic in topicPatNoDict:
            topicPatNoDict[_tempTopic].add(patNO)
        else:
            topicPatNoDict[_tempTopic] = set()
            topicPatNoDict[_tempTopic].add(patNO)
    
    coverageList = []
    termSize = 0
    
    for topic in topicPatNoDict:
        #print(topicPatNoDict[topic])
        for patNo,title,abstract,description,claim,assignee in sql.getPatent_content(topicPatNoDict[topic]):
            _text = title+' '+abstract
            _raw_words = preprocessing(_text)
            
            #fdist = nltk.FreqDist()
            abbrSet = set()
            tmp_words = []
            for term in _raw_words:
                if re.match('^[A-Z-]+$', term) :
                    abbrSet.add(term)
                else:
                    tmp_words.append(term)
                _raw_words = None
         
            finder = BigramCollocationFinder.from_words(tmp_words)
            tmp_words = None
        
            try:
                _size = math.floor(len(finder.score_ngrams(BigramAssocMeasures().likelihood_ratio))/2)+1
            except ValueError:
                continue
            
            termList = []
            for x,y in list(finder.nbest(BigramAssocMeasures().likelihood_ratio, _size)):
                if x.lower() not in stopword and y.lower() not in stopword:
                    termList.append(x+' '+y)
                else:
                    pass
            
            for abbr in abbrSet:
                termList.append(abbr)
            """   計算keyword於單一專利的coverage"""
            hit = 0
            try:
                for keyword in topicKeywordDict[topic]:
                    for term in termList:
                        if keyword == term:
                            hit+=1 
            except KeyError:
                pass
            
            try:
                _coverageRate = hit/len(termList)
                coverageList.append(_coverageRate)
                termSize += len(termList)
            except ZeroDivisionError:
                pass
            
    sql.close()
    
    sum = 0
    for coverage in coverageList:
        sum+=coverage
    print('Coverage rate : {}'.format(sum/len(coverageList)))
    
    _keywordSize = 0
    for topic in topicKeywordDict:
        _keywordSize+=len(topicKeywordDict[topic])
    print('keyword size : {}'.format(_keywordSize))
    
    print('term size :{}'.format(termSize))

    
    
if __name__ == '__main__':
    
    #generateTargetTag('H04W/buckets', '52', 'H04W/52_tags_20160427')
    #getPatDocument('H04W/buckets', '68', 'H04W/68_pat')
    #getPatDocument('G06T/buckets', '17', 'G06T/17_pat')
    #company_tech_distribution('G06T/buckets', 'microsoft', 'G06T/microsoft_Tech_Distribution.csv')
    
    #bucketToTag('H04W/buckets', 'H04W/tags_20160429_full', 'H04W/TFIDF_20160429_full', 'H04W/RWRprob_2016049_full')
    #bucketToTag('G06T/buckets', 'G06T/tags_20160428_weight04', 'G06T/TFIDF_20160428', 'G06T/RWRprob_2016048')
    
    #OUTPATH = 'H04W/'
    #OUTPATH = 'C:/xampp/htdocs/bi_sankey/'
    #tagToBi_sankeyJson('H04W/buckets', 'H04W/links', 'H04W/tags_fix', 'H04W/H04W_GROUP.json', 50, OUTPATH, '56/00')
    
    #get_evolution()
    #test_di_steiner_tree()
    
    
#     with open('H04W/buckets', mode='r') as f:
#         buckets=json.loads(f.read())
#     with open('H04W/links', mode='r') as f:
#         links=json.loads(f.read())
#     with open('H04W/tags', mode='r') as f:
#         tags=json.loads(f.read())
    
#     tags = generateTag(buckets)
#     
#     with open('H04W/tags_1', mode='w') as f:
#         f.write(json.dumps(tags))
# 
#     _statics_phrase('H04W/buckets', 'H04W/tags_20160427_weight04','H04W/')
#     _statics_correlation(links,'H04W/cor')


    #weigh_test_tfidf_rwr('H04W/TFIDF_20160427', 'H04W/RWRprob_20160427', 0.8, 'H04W/tags_20160427_weight08')
    

#    termList = ['GSM','GPRS','WCDMA','HSDPA','LTE-A','LTE']
#     termList = ['FDMA','TDMA','CDMA','OFDMA','SC-FDMA','TD-SCDMA','MIMO','eNode']
#     termList = ['CA','carrier aggregation','transmit power','base station'
#                 ,'Component Carriers','CC','Component Carrier']
#     termList = ['CQI','PUCCH','PUSCH','HARQ',['user equipment','UE']
#                 ,'transmit power','base station']
#                 #,['Coordination Multi-Point','CoMP','Coordinated Multipoint','joint transmission']]
    #statics_specific_phrase('H04W/buckets', 'H04W/tags_20160427_weight04', termList, 'H04W/statics5.csv')
    
    calculateKeywordCoverage('H04W/tags_20160427_weight04', 10)
    
#     termList = ['Virtual Reality']
#     statics_specific_phrase('G06T/buckets', 'G06T/tags_20160428_weight04', termList, 'G06T/statics.csv')

    
    