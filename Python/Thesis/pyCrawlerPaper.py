# coding=utf-8
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import requests
from bs4 import BeautifulSoup


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    print text


#print convert_pdf_to_txt("C:\\Users\\Chen\\Desktop\\Real-Time Sentiment-Based Anomaly Detection in Twitter Data Streams.pdf")


def dblp_url_redirect(url):
    
    req = requests.get(url)
    redirct_url = req.url
    print "[REDIRCT] {} --> {}".format(url,redirct_url)
    
    if 'sciencedirect.com' in redirct_url:
        get_sciencedirect_PDF(req)
    elif 'link.springer' in redirct_url:
        get_springer_PDF(req)
    elif 'dl.acm' in redirct_url:
        get_acm_PDF(req)
    elif 'ieeexplore' in redirct_url:
        get_ieeexplore_PDF(req)
    else:
        print 
        
    req.close()
    
    
def get_acm_PDF(req):
    
    soup = BeautifulSoup(req.text, 'html.parser')
    pdf_url = 'http://dl.acm.org/' + soup.find("a", {'name':'FullTextPDF'})['href']
    print " [GET PDF] {}".format(pdf_url)
    local_filename = pdf_url.split('/')[-1]
    
    r = requests.get(pdf_url)
    with open(local_filename, 'wb') as f:
         for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    r.close()       
    
    convert_pdf_to_txt(local_filename)
    

def get_ieeexplore_PDF(req):
    
    soup = BeautifulSoup(req.text, 'html.parser')
    pdf_url = 'http://ieeexplore.ieee.org' + soup.find("a", {'id':'full-text-pdf'})['href']
    print " [GET PDF] {}".format(pdf_url)
    local_filename = pdf_url.split('/')[-1]
    
    r = requests.get(pdf_url)
    with open(local_filename, 'wb') as f:
         for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    r.close()       
    
    convert_pdf_to_txt(local_filename)
    

def get_sciencedirect_PDF(req):
    
    soup = BeautifulSoup(req.text, 'html.parser')
    pdf_url = soup.find("a", {'id':'pdfLink'})['pdfurl']
    print " [GET PDF] {}".format(pdf_url)
    local_filename = pdf_url.split('/')[-1]
    
    r = requests.get(pdf_url)
    with open(local_filename, 'wb') as f:
         for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    r.close()       
    
    convert_pdf_to_txt(local_filename)
    
    
def get_springer_PDF(req):
    
    soup = BeautifulSoup(req.text, 'html.parser')
    try:
        pdf_url = 'http://link.springer.com' + soup.find("a", {'id':'abstract-actions-download-chapter-pdf-link'})['href']
    except:
        pdf_url = 'http://link.springer.com' + soup.find("a", {'id':'abstract-actions-download-book-pdf-link'})['href']
        
    print " [GET PDF] {}".format(pdf_url)
    local_filename = pdf_url.split('/')[-1]
    
    r = requests.get(pdf_url)
    with open(local_filename, 'wb') as f:
         for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    r.close()       
    
    convert_pdf_to_txt(local_filename)


    

def query_dblp(query):
    
    print "[DBLP QUERY] {}".format(query)

    req = requests.get('http://dblp.uni-trier.de/search/publ/inc?q='+query+'&h=30&f=150&s=yvpc')
    soup = BeautifulSoup(req.text, 'html.parser')
    
    paper_title = ''
    paper_url = ''
    parper_date = ''
    xml = None
    
    for entry in soup.find_all('li', {'class':'entry article'}):
        paper_title = entry.find('span', {'class':'title'}).text.encode('utf-8')
        
        """link to paper xml"""
        req = requests.get('http://dblp.uni-trier.de/rec/xml/'+ entry['id'] + '.xml')
        xml = BeautifulSoup(req.text, 'html.parser')
        paper_url = xml.find('ee').text
        paper_date = xml.find('article')['mdate']
        print ' <paper> {} {}'.format(paper_date, paper_title)
        dblp_url_redirect(paper_url)
        print '-------------'
        
    for entry in soup.find_all('li', {'class':'entry inproceedings'}):
        paper_title = entry.find('span', {'class':'title'}).text.encode('utf-8')
        
        """link to paper xml"""
        req = requests.get('http://dblp.uni-trier.de/rec/xml/'+ entry['id'] + '.xml')
        xml = BeautifulSoup(req.text, 'html.parser')
        paper_url = xml.find('ee').text
        paper_date = xml.find('inproceedings')['mdate']
        print ' <paper> {} {}'.format(paper_date, paper_title)
        dblp_url_redirect(paper_url)
        print '-------------'
        
    req.close()


#query_dblp('context+rich')


query_dblp('context rich')

