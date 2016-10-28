import mysql.connector as connector
import re

class mysql:

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.config = {
          'host' : 'DB_Address',
          'user' :  'username',
          'password' : 'userPassword',
          'charset' : 'utf8',
          'database' : 'CHIUAN'
        }

    def connect(self):
        self.cnx = connector.connect(**self.config)
    
    def close(self):
        try:
            self.cursor.close()
            self.cnx.close()
        except AttributeError:
            pass
    
    def commit(self):
        self.cnx.commit()
        
    def insert_USPTO(self, patNO, patTitle, patUrl, params):
        
        self.cursor = self.cnx.cursor()
        
        """
        query = ('INSERT INTO USPTO '
                '(title,patNO,assignee,inventors,abstract,description,claim,pubYear,pubMonth,url) '
                'VALUES ('+ patTitle +', '+ patNO +', %(assignee)s, %(inventors)s'
                ', %(abstract)s, %(description)s, %(claim)s, %(pubYear)s, %(pubMonth)s, '+ patUrl +')'
                )
        
        """
        query = ('INSERT INTO USPTO '
                '(title,patNO,assignee,inventors,abstract,description,claim,pubYear,pubMonth,url) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                )
        
        data = (patTitle, patNO, params['assignee'], params['inventors'], params['abstract']
                , params['description'], params['claim'] ,params['pubYear'] ,params['pubMonth'], patUrl)
        
        self.cursor.execute(query, data)
    
    
    def getEdges(self,startdate,enddate,kind):
        
        query = "select patNO, relNO from "+kind+" WHERE rel_date BETWEEN %s and %s"
        
        self.cursor = self.cnx.cursor()
        self.cursor.execute(query, (startdate, enddate))
    
        return self.cursor
    
    
    def getNodes(self,kind):
        
        query = "select patNO, date, maingroup, subgroup from View02 WHERE kind = '{}'".format(kind)
        
        self.cursor = self.cnx.cursor()
        self.cursor.execute(query)
    
        return self.cursor
    
        
    def getPatNOs(self):
        
        pats = set()
        
        query = "select patNO from USPTO"
        
        self.cursor = self.cnx.cursor()
        self.cursor.execute(query)
        
        for row in self.cursor:
            pats.add(row[0])
        
        return pats
        
    
    def getTitle(self,patno_collection):
        
        
        if type(patno_collection) is str:
            
            query = "select title from USPTO where patNO = %s"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query, patno_collection)
            
            for title in self.cursor:
                return title
        
        elif type(patno_collection) is list:
            
            query = "select patNO,title from USPTO where patNO in {}"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\[(.+)\]', '(\g<1>)', str(patno_collection))))
            
            return self.cursor
        
        elif type(patno_collection) is set:
            
            query = "select patNO,title from USPTO where patNO in {}"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\{(.+)\}', '(\g<1>)', str(patno_collection))))
            
            return self.cursor
        
    
        else:
            print('error')
    
    
    def getClaim(self,patno_collection):
        
        if type(patno_collection) is str:
            
            query = "select claim from USPTO where patNO = %s"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query, patno_collection)
            
            for claim in self.cursor:
                return claim
            
        
        elif type(patno_collection) is list:
            
            query = "select patNO,claim from USPTO where patNO in {}"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\[(.+)\]', '(\g<1>)', str(patno_collection))))
            
            return self.cursor
        
        elif type(patno_collection) is set:
            
            query = "select patNO,claim from USPTO where patNO in {}"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\{(.+)\}', '(\g<1>)', str(patno_collection))))
            
            return self.cursor
        
    
        else:
            print('error')
        
        
    def getAbstract(self,patno_collection):    
        
        if type(patno_collection) is str:
            
            query = "select abstract from USPTO where patNO = %s"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query, patno_collection)
            
            for abstract in self.cursor:
                return abstract
            
        
        elif type(patno_collection) is list:
            
            query = "select patNO,abstract from USPTO where patNO in {}"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\[(.+)\]', '(\g<1>)', str(patno_collection))))
            
            return self.cursor
        
        elif type(patno_collection) is set:
            
            query = "select patNO,abstract from USPTO where patNO in {}"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\{(.+)\}', '(\g<1>)', str(patno_collection))))
            
            return self.cursor
        
    
        else:
            print('error')
        
    
    def getPatent_content(self,patno_collection):
        
        if type(patno_collection) is str:
        
            query = "select title,abstract,description,claim from USPTO where patNO = '{}'"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(patno_collection))
            return self.cursor
        
        elif type(patno_collection) is set:
            
            query = "select patNo,title,abstract,description,claim,assignee from USPTO where patNO in {}"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\{(.+)\}', '(\g<1>)', str(patno_collection))))
            return self.cursor
        
        else:
            print('error')
            
            
    def getDate(self,patno_collection):
        
        if type(patno_collection) is str:
        
            query = "select patNO,date from USPTO where patNO = '{}'"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(patno_collection))
            return self.cursor
        
        elif type(patno_collection) is set:
            
            query = "select patNO,date from USPTO where patNO in {} ORDER BY date ASC"
        
            self.cursor = self.cnx.cursor()
            self.cursor.execute(query.format(re.sub('\{(.+)\}', '(\g<1>)', str(patno_collection))))
            return self.cursor
        
        else:
            print('error')
            
            
    def getCount_fromMaintFeeEvents(self,patno_collection):
        
        query = "select count(id) from MaintFeeEvents where patNO in {}"
        
        self.cursor = self.cnx.cursor()
        self.cursor.execute(query.format(re.sub('\{(.+)\}', '(\g<1>)', str(patno_collection))))
        for count in self.cursor:
            return count
        
    
    def getStatistics_fromMaintFeeEvents(self,patno_collection, comparison=None):
        
        KEEP_MAINT_CODES = ['M2551','ASPN','M1559','M1461','EXPX','M3551','M1551']
        NO_MAINT_CODES = ['R2551','R1551','RMPN','EXP.']
        #OTHER = []
        
        keepMaint = set()
        noMaint = set()
        other = set()
        
        query = "select id, patNo, maintCode from MaintFeeEvents where patNO in {}"
        event_number = 0
        maintCodes = {}
        
        self.cursor = self.cnx.cursor()
        self.cursor.execute(query.format(re.sub('\{(.+)\}', '(\g<1>)', str(patno_collection))))
        
        for id, patNo, maintCode in self.cursor:
            event_number+=1
            
            if maintCode in KEEP_MAINT_CODES:
                keepMaint.add(patNo)
            elif maintCode in NO_MAINT_CODES:
                noMaint.add(patNo)
            else:
                other.add(patNo)
            
            if maintCode in maintCodes:
                maintCodes[maintCode]+=1
            else:
                maintCodes[maintCode]=1
                
                
        print('============')
        print('Maintenance Fee event number : %d'%(event_number))
        print(maintCodes)
        print('keep Maintenance patent number : %d'%(len(keepMaint)))
        print('no Maintenance patent number : %d'%(len(noMaint)))
        print('other patent number : %d'%(len(other)))
        
        if comparison is not None:
            print(len(set(keepMaint&comparison)))
        
        
        event_patents = keepMaint|noMaint|other
        
#         for patno in patno_collection:
#             if patno not in event_patents:
#                 print(patno)
        
        
        print('============')
        
        return keepMaint
        
        