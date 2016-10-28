import requests
from bs4 import BeautifulSoup
import os

"""
f = open('G06T_subclass.txt','r')

subclass_count=0;
for line in f.readlines():
    if 'G06T' in line:
        subclass_count+=1


print subclass_count


req = requests.get('http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=context+rich&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT')
soup = BeautifulSoup(req.text, 'html.parser')  
print soup
print '--------------------------------------------------'

nextlist_suffix = soup.find('img',{'alt':'[NEXT_LIST]'}).parent['href']
print nextlist_suffix

req = requests.get('http://patft.uspto.gov'+nextlist_suffix,req.cookies)
print '--------------------------------------------------'
print BeautifulSoup(req.text,'html.parser')

"""


