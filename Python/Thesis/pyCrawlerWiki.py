# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import json
import datetime




def crawler_related_pageTitle(url, dict, iter_count):
    
    iter_count+=1
    
    if iter_count>6:
        return
    
    _WIKI_URL = 'https://en.wikipedia.org'
    
    if 'Category:' not in url:
        print('URL ERROR')
    
    req = requests.get(url)
    doc = BeautifulSoup(req.text, 'html.parser')
    req.close()
    
    category = doc.find('h1', {'id':'firstHeading'}).text.replace('Category:','')
    
    print('[Category : %s]' %(category))
    dict.add(category)
    
    """  page """
    for e in doc.find_all('div',{'class':'mw-category-group'}):
        for e2 in e.find_all('a'):
            page = e2.text
            dict.add(page) 
            print(page)
        
    print('---------------------------')
    
    """  subcategory """ 
    for e in doc.find_all('a', {'class':'CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory'}):
        print(e.text)
        crawler_related_pageTitle(_WIKI_URL+e['href'], dict, iter_count)
    

    """  check next page""" 
    try:
        next_page = doc.find('a', text='next page')['href']
        crawler_related_pageTitle(_WIKI_URL+next_page, dict, iter_count)
    except TypeError:
        pass 
    
    
def crawler_related():
    _WIKI_DICT = set()
    iter_count = 5
    #crawler_related_pageTitle('https://en.wikipedia.org/wiki/Category:Image_processing', _WIKI_DICT, iter_count)
    crawler_related_pageTitle('https://en.wikipedia.org/wiki/Category:Computer_graphics', _WIKI_DICT, iter_count)
    
    #f = open('Image_processing_DICT','w')
    f = open('Computer_graphics_DICT','w')
    for term in _WIKI_DICT:
        f.write(term.encode('utf-8')+'\n')
        
    f.close()


def crawler_ontoloy(url, iter_count):
    
    if iter_count>5:
        return
    
    iter_count+=1
    
    ontoloyDict = {}
    
    _WIKI_URL = 'https://en.wikipedia.org'
    
    if 'Category:' not in url:
        print('URL ERROR')
    
    req = requests.get(url)
    doc = BeautifulSoup(req.text, 'html.parser')
    req.close()
    
    category = doc.find('h1', {'id':'firstHeading'}).text.replace('Category:','')
    #ontoloyDict[category] = {}
    ontoloyDict['pages'] = []
    ontoloyDict['subcategories'] = {}
    
    """  pages """
    pages = []
    for e in doc.find_all('div',{'class':'mw-category-group'}):
        for e2 in e.find_all('a'):
            pages.append(e2.text)
    ontoloyDict['pages'] = pages
    page_num = len(pages) 
    pages = None
    
    
    """  subcategories """
    sub_num = 0
    for e in doc.find_all('a', {'class':'CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory'}):
        ontoloyDict['subcategories'][e.text] = crawler_ontoloy(_WIKI_URL+e['href'], iter_count)
        sub_num+=1
        #print(e.text)
    
    
    print('%s %s --> pages:%s subcategories:%s' %(str(datetime.datetime.now()), category, page_num, sub_num))
    
    
    return ontoloyDict

def ontology_iter(j):
    
#     global page
#     global cate
    
    try:
        page_num = len(j[u'pages'])
        #page.add(j[u'pages'])
    except TypeError:
        page_num = 0
    
    try:
        cate_num = len(j[u'subcategories'])
    
        #cate.add(j[u'subcategories'].keys())
        for sub in j[u'subcategories']:
            (page_tmp, cate_tmp) = ontology_iter(j[u'subcategories'][sub])
            page_num += page_tmp
            cate_num += cate_tmp
    except TypeError:
        cate_num = 0
        
    
    return (page_num, cate_num)
    
    
def cal():
#     global page
#     global cate
#     page = set()
#     cate = set()
    
    f = open('wireless.json','r')
    j = json.loads(f.read())
    f.close
    
    print(ontology_iter(j[u'wireless']))
#     print(cate)
#     print(page)
     

cal()
# ontoloyDict = {}
# ontoloyDict['wireless'] = crawler_ontoloy('https://en.wikipedia.org/wiki/Category:Wireless',0)
# f = open('wireless.json','w')
# f.write(json.dumps(ontoloyDict))
# f.close()
