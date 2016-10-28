from bs4 import BeautifulSoup, NavigableString, Tag
import re
import requests

input = '''<coma>Oblon, Spivak, McClelland, Maier & Neustadt, L.L.P.
<BR>
<HR>
<br />
Important Text 1
<br />
<br />
Not Important Text
<br />
Important Text 2
<br />
Important Text 3
<br />
<br />
Non Important Text
<br />
Important Text 4
<br /></coma>'''

#<CENTER><b><i>Claims</b></i></CENTER>

input2 = '''<coma>
<br />
Important Text 1
<br />
<br />
Not Important Text
<br />
Important Text 2
<br />
Important Text 3
<br />
<br />
Non Important Text
<br />
Important Text 4
<br /></coma>'''

input3 = '''<coma>Yudell Isidore PLLC
<BR>
       <HR>
       <CENTER><b><i>Parent Case Text</b></i></CENTER>
       <HR>
       <BR><BR>CROSS-REFERENCES TO RELATED APPLICATIONS
<BR><BR> This application is a continuation of application Ser. No. 13/972,007
     filed Aug. 21, 2013 and entitled "System and Method for Sudden Proximal
     User Interface" which is a continuation of application Ser. No.
     12/590,831 (now U.S. Pat. No. 8,634,796 issued on Jan. 21, 2014) filed
     Nov. 13, 2009 and entitled "System and Method for Location Based
     Exchanges of Data Facilitating Distributed Locational Applications" which
     is a continuation in part of application Ser. No. 12/287,064 (now U.S.
     Pat. No. 8,639,267 issued on Jan. 28, 2014) filed Oct. 3, 2008 and
     entitled "System and Method for Location Based Exchanges of Data
     Facilitating Distributed Locational Applications" which is a continuation
     in part of application Ser. No. 12/077,041 (now U.S. Pat. No. 8,600,341
     issued on Dec. 3, 2013) filed Mar. 14, 2008 and entitled "System and
     Method for Location Based Exchanges of Data Facilitating Distributed
     Locational Applications". This application contains an identical
     specification to Ser. No. 13/972,007 except for the title and claims.
     Claims herein are very similar to Ser. No. 13/972,155 (now U.S. Pat. No.
     8,718,598 issued on May 6, 2014) filed Aug. 21, 2013 and entitled "System
     and Method for Location Based Exchange Vicinity Interest Specification".
         <HR>
<CENTER><b><i>Claims</b></i></CENTER> <HR> <BR><BR>What is claimed is: <BR><BR> 1.  A method comprising: accepting, from a user of a user interface of a mobile application of a user carried mobile data processing system, a user specified location based
event configuration used by the mobile data processing system in detecting a region of vicinity around a remote data processing system beaconing a beaconed broadcast wireless data record having no fields containing a finalized physical location useful
without conversion for subsequent data processing system mathematical triangulation, the beaconed broadcast wireless data record received by the mobile data processing system, the user specified location based event configuration stored local to the
mobile data processing system and used by the mobile data processing system for the mobile data processing system matching at least three distinct data items of the user specified location based event configuration derived from the accepting to a
corresponding at least three distinct beacon items in a plurality of application data fields of the beaconed broadcast wireless data record, the matching for distinguishing: regions of vicinity around remote data processing systems beaconing beaconed
broadcast wireless data records including the corresponding at least three distinct beacon items that match the at least three distinct data items of the user specified location based event configuration derived from the accepting, among regions of
vicinity around remote data processing systems beaconing beaconed broadcast wireless data records not including the corresponding at least three distinct beacon items that match the at least three distinct data items of the user specified location based
event configuration derived from the accepting;  and saving, by the mobile application, the user specified location based event configuration to a memory of the mobile data processing system for the mobile data processing system performing operations
including: monitoring the user specified location based event configuration for the detecting the region of vicinity around the remote data processing system beaconing the beaconed broadcast wireless data record by the mobile data processing system
comparing the at least three distinct data items of the user specified location based event configuration derived from the accepting to the corresponding at least three distinct beacon items in the plurality of application data fields of the beaconed
broadcast wireless data record, the at least three distinct beacon items including: an identifier item for identifying one or more of the remote data processing systems beaconing, a plurality of mobile application data items being semantically related to
each other by the mobile application data items having organization hierarchy meaning recognized by the mobile application, and a reference item for the mobile data processing system determining a distance between the mobile data processing system and
the remote data processing system;  matching, upon the mobile data processing system comparing, the at least three distinct data items of the user specified location based event configuration derived from the accepting to the corresponding at least three
distinct beacon items in the plurality of application data fields of the beaconed broadcast wireless data record;  and communicating, upon the matching a notification of the matching.
<BR><BR> <CENTER><b>* * * * *</b></CENTER></coma>


'''

# soup = BeautifulSoup(input3,'html.parser')
# 
# print soup.findAll('br')

#print str(u'9,191,459').replace(',', '')

payload = {'NextList2':'Next 50 Hits'
           ,'Sect1':'PTO2'
           ,'Sect2':'HITOFF'
           ,'u':'/netahtml/PTO/search-adv.htm'
           ,'r':'0'
           ,'f':'S'
           ,'l':'50'
           ,'d':'PTXT'
           ,'OS':'"context rich"'
           ,'RS':'"context rich"'
           ,'Query':'"context rich"'
           ,'TD':'101'
           ,'Srch1':'"context rich"'}
req = requests.get('http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=context+rich&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT&Sect1=PTO2&Sect2=HITOFF&d=PTXT&NextList2=Next+50+Hits&f=S&RS=%22context+rich%22&l=50&r=0&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&Query=%22context+rich%22&TD=101&OS=%22context+rich%22&Srch1=%22context+rich%22'
                   ,params=payload)

print req.url
"""
for br in soup.find('coma').findAll('br'):
    next = br.nextSibling
    if not (next and isinstance(next,NavigableString)):
        continue
    next2 = next.nextSibling
    if next2 and isinstance(next2,Tag) and next2.name == 'br':
        text = str(next).strip()
        if text:
            print "Found:", next
            """