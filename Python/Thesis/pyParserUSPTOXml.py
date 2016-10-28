# -*- coding: UTF-8 -*-
from lxml import etree
import os
import re
from string import join

def modXML(filepath):
        
    file = open(re.sub('(\S+)\.xml', '\g<1>_mod.xml', filepath), 'w')
    first = True
    with open(filepath,'r') as f:
        for line in f.readlines():
            if '<!DOCTYPE' in line and first is True:
                file.write('<patents>\n'.encode('utf8'))
                first = False
            elif '<!DOCTYPE' in line:
                file.write(''.encode('utf8'))
            elif '<?xml' in line:
                file.write(''.encode('utf8'))
            else:
                file.write(line.encode('utf8'))
        
    file.write('\n</patents>')
    file.close() 


def XMLtoSQL(xmlpath, listsqlname, citedsqlname, kindsqlname):
    
    pat_count = 0
    target_section = u'G'
    target_class = u'06'
    target_subclass = u'K'
    kind = target_section+target_class+target_subclass
    
    insert_list = u'INSERT IGNORE INTO USPTO (title, patNO, assignee, inventors, abstract, description, claim ,date) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");\n'
    insert_cited = u'INSERT IGNORE INTO USPTORel (patNO, relNO, date) VALUES {};\n'
    insert_kind = u'INSERT IGNORE INTO USPTOKind (patNO, kind, maingroup, subgroup) VALUES (\"{}\", \"{}\", \"{}\", \"{}\");\n' 
    
    #doc = etree.parse('ipg140415.xml')
    doc = etree.parse(xmlpath)
    
    patents = doc.xpath('//us-patent-grant')
    
    cited_file = open(citedsqlname,'a')
    list_file = open(listsqlname,'a')
    kind_file = open(kindsqlname,'a')
    
    
    for patent in patents:
        
        correct_class = False

        kinds = []
        for classification in patent.xpath('.//classification-ipcr'):
            _section = classification.xpath('./section')[0].text
            _class =  classification.xpath('./class')[0].text
            _subclass = classification.xpath('./subclass')[0].text
            _group = classification.xpath('./main-group')[0].text
            _subgroup = classification.xpath('./subgroup')[0].text
            #print _section, _class, _subclass
            kinds.append([_section+_class+_subclass, _group, _subgroup])
            
            if _section == target_section and _class == target_class and _subclass == target_subclass: 
                correct_class = True
            else:
                pass
        
        if correct_class == True:
            pat_count+=1
            pat_no = patent.xpath('@file')[0].split('-')[0].strip()
            title = patent.xpath('./us-bibliographic-data-grant/invention-title')[0].text
            
            
            claims = u''
            for claim in patent.xpath('./claims/claim//claim-text'):
                try:
                    claims += join(claim.itertext())
                except AttributeError:
                    pass

            abstract = ''        
            for p in patent.xpath('./abstract//p'):
                try:
                    abstract += p.text.strip()
                except AttributeError:
                    pass
                    
            pubdate = patent.xpath('@date-publ')
            
            description = u''
            for desc in patent.xpath('./description//p'): 
                try:
                    #print join(desc.itertext())
                    #description += desc.text.strip()
                    description += join(desc.itertext())
                except AttributeError:
                    pass
                
            assignees = ''
            for assignee in patent.xpath('./us-bibliographic-data-grant/assignees/assignee/addressbook//orgname'):
                assignees +=assignee.text + u';'
            
            inventors = ''
            if 'v4.2 2006-08-23' in patent.attrib['dtd-version']:
                try:
                    for inventor in patent.xpath('./us-bibliographic-data-grant/parties/applicants/applicant//addressbook'):
                        inventors += inventor.xpath('./last-name')[0].text+','+ inventor.xpath('./first-name')[0].text + u';'
                except IndexError:
                    pass
            else:
                try:
                    for inventor in patent.xpath('./us-bibliographic-data-grant/us-parties/inventors/inventor//addressbook'):
                        inventors += inventor.xpath('./last-name')[0].text+','+ inventor.xpath('./first-name')[0].text + u';'
                except IndexError:
                    for inventor in patent.xpath('./us-bibliographic-data-grant/us-parties/us-applicant//addressbook'):
                        inventors += inventor.xpath('./last-name')[0].text+','+ inventor.xpath('./first-name')[0].text + u';'
                
            try:
                title = title.replace('"','\'')
                claims = re.sub('\n', '', claims.replace('"','\''))
                abstract = abstract.replace('"','\'')
                #description = description.replace('"','\'')
                description = re.sub('\n', '', description.replace('"','\''))
                assignees = assignees[:-1].replace('"','\'')
                inventors = inventors[:-1].replace('"','\'')
            except AttributeError:
                pass
            #print pubdate[0]
            
            #print pat_no
            #print claims
            #print description
#             if str is None:
#                 break
            
            
            list_file.write(insert_list.format(title, pat_no, assignees, inventors, abstract, description, claims, pubdate[0]).encode('utf-8'))
            
            for kind in kinds:
                kind_file.write(insert_kind.format(pat_no, kind[0], kind[1], kind[2]).encode('utf-8'))
            
            """ version difference"""
            if 'v4.2 2006-08-23' in patent.attrib['dtd-version']:
                cited_xpath = './us-bibliographic-data-grant/references-cited/citation//patcit'
            
            else:
                cited_xpath = './us-bibliographic-data-grant/us-references-cited/us-citation//patcit'
            
            s=''
            for patcit in patent.xpath(cited_xpath):
                try:
                    relNO = patcit.xpath('./document-id/doc-number')[0].text
                    if '/' not in relNO : 
                        relNO = 'US'+relNO.zfill(8)
                except IndexError:
                    relNO = None
                    
                try:
                    date = patcit.xpath('./document-id/date')[0].text
                except IndexError:
                    date = ''
                        
                if relNO is not None:
                    s+= u'(\"{}\", \"{}\", \"{}\"),'.format(pat_no, relNO, date)
            
            if s is not '':
                cited_file.write(insert_cited.format(s[:-1]))
            
            
            
        else:
            pass
        
        #print '----------------------'
    
    kind_file.close()
    list_file.close()
    cited_file.close()
    
    return pat_count
    

_YEAR = '2010'
path = 'C:/Users/Chen/Desktop/data/'+_YEAR
listsqlname = '20160108/G06K/'+_YEAR+'list.sql'
citedsqlname = '20160108/G06K/'+_YEAR+'cited.sql'
kindsqlname = '20160108/G06K/'+_YEAR+'kind.sql'

#XMLtoSQL('C:/Users/Chen/Desktop/data/2014/ipg140107_mod.xml','456','654')

""" transfer xml to correct schema"""
"""
for dirPath, dirNames, fileNames in os.walk(path):
    for fileName in fileNames:
        if 'mod' not in fileName:
            print 'TRANSFER {}'.format(fileName)
            modXML(path+'/'+fileName)
"""


total_pat = 0

for dirPath, dirNames, fileNames in os.walk(path):
    i = 1
    file_size = len(fileNames)
    for fileName in fileNames:
        if 'mod' in fileName:
            print 'PARSER {} . . . ({}/{})'.format(fileName, i, file_size)
            count = XMLtoSQL(path+'/'+fileName, listsqlname, citedsqlname, kindsqlname)
            total_pat += count
            print '    ∟ {} patents'.format(count)
        else:
            print 'PASS  {} . . . ({}/{})'.format(fileName, i, file_size)
        i+=1
        
    print ' ------>  Total {} patents'.format(total_pat)


