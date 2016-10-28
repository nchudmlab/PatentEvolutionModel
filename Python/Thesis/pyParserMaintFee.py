

insertStr = u'INSERT IGNORE INTO MaintFeeEvents (patNo, applNo, smallEntity, applFilingDate, grantIssueDate, maintDate, maintCode) VALUES {};\n'
s = ''
insert_num = 0

fr = open('MaintFeeEvents_20150316.txt','r')
fs = open('MaintFeeEvents_20150316.sql','w')

for line in fr:
    insert_num+=1
    
    items = line.split(' ')
    
    patNo = 'US0' + items[0]
    
    if items[2] is 'Y':
        smallEntity = 1
    else:
        smallEntity = 0
    
    if insert_num < 1000:
        s+= u'(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"),'.format(patNo, items[1], smallEntity, items[3], items[4], items[5], items[6].strip())
    else:
        fs.write(insertStr.format(s[:-1]))
        insert_num = 0
        s = ''
    
        
fs.close()
fr.close()




