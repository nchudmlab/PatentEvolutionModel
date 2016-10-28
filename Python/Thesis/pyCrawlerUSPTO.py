# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
from pyMysql import mysql
import re
from time import sleep



#YEAR_RANGE = ['2010','2011','2012','2013','2014','2015']
MONTH = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8
         ,'September':9, 'October':10, 'November':11, 'December':12}


def crawler_Patents(url,cookies=None):
    
    
    #sql = mysql()
    #sql.connect()
    file = open('patents.txt','a')
    
    """ Get the patent list of querying keyword """
   
    try :
        req = requests.get(url,cookies)
    except requests.exceptions.ConnectionError:
        sleep(60)
        while req.status_code != 200:
            req = requests.get(url,cookies)
        
    
    soup = BeautifulSoup(req.text, 'html.parser') 
    #soup = BeautifulSoup(open(url), 'html.parser')  
    
    for trlist in soup.findAll('tr'):
         
        tdlist = trlist.findAll('td')
         
        try:
            patNO = tdlist[1].text.strip().replace(',','')
            print patNO
            file.write(patNO+'\n')
            #patTitle = tdlist[3].text.rstrip(u'\r\n')
            #patTitle = re.sub('\s{2,}', '', patTitle)
            #patUrl = tdlist[1].find('a')['href']
            #print patTitle
            #print patUr
                     
        except IndexError:
            pass
    
    
    
    file.close()
    

#     """ next page """
#     next_page_payload = {}
#     
#     form = soup.find('form', {'name':'srchForm'})
#     has_next = False
#     
#     print form
#     
#     """ parser form"""
#     for line in str(form).split('\n'):
#         if '<input' in line:
#             if 'type="HIDDEN"' in line:
#                 name = re.sub('.+name=\"(\S+)\".+', '\g<1>', line)
#                 value = re.sub('.+value=\"([\S ]+)\".+', '\g<1>', line)
#                 next_page_payload[name] = value 
#             elif 'type="submit"' in line:
#                 if 'name="Next' in line:
#                     name = re.sub('.+name=\"(\S+)\".+', '\g<1>', line)
#                     value = re.sub('.+value=\"([\S ]+)\".+', '\g<1>', line)
#                     next_page_payload[name] = value 
#                     has_next = True
#         else:
#             pass
#         
#     #print next_page_payload 
#    
#     
#     if next_page_payload is not None and has_next is True:
#         #crawler_Patents('http://patft.uspto.gov/netacgi/nph-Parser',next_page_payload)
#         req = requests.get('http://patft.uspto.gov/netacgi/nph-Parser',next_page_payload)
#         print req.url
#         soup = BeautifulSoup(req.text, 'html.parser')
#         print soup
    
    try:
        nextlist_suffix = soup.find('img',{'alt':'[NEXT_LIST]'}).parent['href']
        crawler_Patents('http://patft.uspto.gov'+nextlist_suffix, req.cookies)
    except AttributeError:
        print 'PARSER LIST END'
    
    req.close()
    #sql.close() 
    

""" Get the content of single patent page """
def get_PantentDoc(patent_url):
    
    parameter = {}
    
    if 'patft.uspto.gov' not in patent_url:
        req = requests.get('http://patft.uspto.gov'+patent_url)
    else:
        req = requests.get(patent_url)
        
        
    soup = BeautifulSoup(req.text, 'html.parser')
    
    #f = open('patent_html','w')
    #f.write(req.text)
    
    """ month and year which was issued by the USPTO"""
#     trlist = soup.findAll('tr')
#     try:
#         pubDate = trlist[6].findAll('td')[1].text.strip()
#     except KeyError:
#         pubDate = 'none'
#         
#     parameter['pubMonth'] = month_to_integer(pubDate)
#     parameter['pubYear'] = pubDate.split(',')[1].strip()
#     print parameter['pubMonth'], parameter['pubYear']
    
    """ inventors and assignee """
    inventors = soup.find('th', text='Inventors:').find_next_sibling('td').text.strip()
    parameter['inventors'] = inventors
        
        
    """ Filed date """
    filed_date = soup.find('th', text=u'Filed:\n       ').find_next_sibling('td').text.strip()
    parameter['pubMonth'] = month_to_integer(filed_date)
    parameter['pubYear'] = filed_date.split(',')[1].strip()
    print parameter['pubMonth'],parameter['pubYear']
        
        
    try:
        assignee = soup.find('th', text='Assignee:').find_next_sibling('td').text.rstrip(' \r\n')
        assignee = assignee.rstrip('\r\n')
        parameter['assignee'] = re.sub('\s{2,}', '', assignee)
    except AttributeError:
        parameter['assignee'] = None
    #print parameter['inventors'], parameter['assignee']
            
    """ abstract """
    temp = soup.find('center', text='Abstract').find_next_sibling('p').text.rstrip('\r\n')
    parameter['abstract'] = re.sub('\s{2,}', '', temp)
    #print parameter['abstract']
         
    """ references """
    parameter['rel'] = []
    ref_table = soup.find('center', text='U.S. Patent Documents').find_next_sibling('table')
        
    for tr in ref_table.findAll('tr'):
        tdlist = tr.findAll('td')
        try:
            ref_ID = tdlist[0].text.rstrip('\r\n')
            ref_ID = re.sub('\s{2,}', '', ref_ID)
            ref_url = tdlist[0].find('a')['href']
            ref_date = tdlist[1].text
            ref_date_split = ref_date.split(' ')
            parameter['rel'].append({'relNO':ref_ID, 'relURL':ref_url, 'relMonth': month_to_integer(ref_date_split[0]), 'relYear':ref_date_split[1]})
            #print ref_ID, ref_url, ref_date
        except IndexError:
            pass
        except TypeError:
            pass
                 
                 
    """ Claim """
    temp = req.text.split('<CENTER><b><i>Claims</b></i></CENTER>')[1]
    temp = temp.split('<CENTER><b><i>Description</b></i></CENTER>')[0]
    parameter['claim'] = temp.replace('<BR>', '').replace('<HR>', '')
    #print parameter['claim']
    
             
    """ descriptions"""
    descriptions = req.text.split('<CENTER><b><i>Description</b></i></CENTER>')[1]
    descriptions = descriptions.split('<CENTER><b>* * * * *</b></CENTER>')[0]
    parameter['description'] = descriptions.replace('<BR>', '').replace('<HR>', '')
    #print parameter['description']
        
    print '-> crawler OK'
    req.close()
    return parameter
    

def month_to_integer(pubDate):
    
    for month in MONTH.keys():
        if month in pubDate:
            to_integer = MONTH.get(month)
            break
        else:
            pass
        
    return to_integer
    

#get_PantentDoc('/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=1&f=G&l=50&d=PTXT&p=1&S1="content+aware"&OS="content+aware"&RS="content+aware"')
#get_PantentDoc('http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=2&f=G&l=50&co1=AND&d=PTXT&s1=%22context+rich%22&OS=%22context+rich%22&RS=%22context+rich%22')

crawler_Patents('http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=G06Q&FIELD1=CPCL&co1=AND&TERM2=1%2F1%2F2014-%3E12%2F31%2F2014&FIELD2=APD&d=PTXT')
#crawler_Patents('patent_list')

