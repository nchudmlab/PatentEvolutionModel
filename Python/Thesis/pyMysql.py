import mysql.connector as connector


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
    
    
    def insert_USPTORel(self, patNO, rows):

        self.cursor = self.cnx.cursor()
    
        query = ('INSERT INTO USPTORel '
                '(patNO, relNO, relURL, relMonth, relYear) '
                'VALUES (' + str(patNO) + ', %(relNO)s, %(relURL)s, %(relMonth)s, %(relYear)s)'
                )
        
        for row in rows:
            print row['relNO']
            self.cursor.execute(query, row)
    
        
        
    """
    def insert_wsWraRiverStageRaw(self,list):
        
        self.cursor = self.cnx.cursor()
        
        query = ('INSERT INTO wsWraRiverStageRaw '
                '(ST_NO,RECDATE,Stage) '
                'VALUES (%(ST_NO)s,%(RECDATE)s,%(Stage)s)'
                )
        
        try:
            for row in list:
                self.cursor.execute(query, row)
            self.cnx.commit()
        #Duplicate key    
        except connector.errors.IntegrityError as err:
            print('Something went wrong: {}'.format(err))
        
    
    def getST_NOs(self):
        
        query = 'select ST_NO from wsWraRiverStations'
        ST_NOs = []
        
        self.cursor = self.cnx.cursor()
        self.cursor.execute(query)
        
        for row in self.cursor:
            ST_NOs.append(row[0])
        
        self.cnx.commit()
        
        return ST_NOs
    """
    
    def getTitle(self,id):
        
        query = 'select claim from USPTO where id = {}'.format(id)
    
        self.cursor = self.cnx.cursor()
        self.cursor.execute(query)
        
        for row in self.cursor:
            print row[0]
        
        
        
        
        