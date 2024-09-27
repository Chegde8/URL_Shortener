import pyodbc

class databaseConnector:
    
    def __init__(self):
        self.server = 'localhost,1433'
        self.connection = None
        self.password= 'SqlPassword.2024'
        self.database_name = 'URL_Shortener_db'
        self.conn_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database_name};UID=SA;PWD={self.password};TrustServerCertificate=Yes;'
        self.setup_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};UID=SA;PWD={self.password};TrustServerCertificate=Yes;'
    
    def __del__(self):
        # destrcutor for databaseConnection class
        self.cleanup()
    
    def setup(self):
        # Database is setup here.
        # This is a one time setup of the database
        # Only need to run this when bringing up a new database server
        # Creates the database and the tables
        # Details explained in the schema in the README.md
        
        connection_setup = None
        
        try:
            # Create a cursor from the connection
            connection_setup = pyodbc.connect(self.setup_string, autocommit=True)
            cursor = connection_setup.cursor()
            
            # Check if database exists
            print("Checking if the database is prepared")
            cursor.execute("SELECT database_id FROM sys.databases WHERE name = ?;", (self.database_name,))
            db_exists = cursor.fetchone()
            cursor.close()
            
            if db_exists:
                print(f"Database '{self.database_name}' already exists.")
            else:
                
                # Create database if it does not exist
                cursor = connection_setup.cursor()
                cursor.execute(f"CREATE DATABASE {self.database_name};")
                connection_setup.commit()
                cursor.close()
                print(f"Database '{self.database_name}' has been created.")
                
                # Create tables if they dont exists
                cursor = connection_setup.cursor()
                #USE {self.database_name}
                # Switch to the URL_Shortener_db database
                use_db_sql = f"USE {self.database_name}"
                cursor.execute(use_db_sql)
                create_table_sql = '''
CREATE TABLE urls (
    id INT IDENTITY(1,1) UNIQUE NOT NULL,
    short_url VARCHAR(60) PRIMARY KEY NOT NULL,
    original_url TEXT NOT NULL,
    expires_at DATETIME
);
'''
                cursor.execute(create_table_sql)
                connection_setup.commit()
                cursor.close()
                print("Database urls has been created.")
        except pyodbc.Error as e:
            print(f"There was a problem in setting up the database, {e}")
            raise e
        finally:
            if connection_setup:
                connection_setup.close()
            
            # TODO
            # DELETE FROM urls WHERE expires_at < SYSDATETIMEOFFSET() AT TIME ZONE 'UTC';
    
    def connectSQL(self):
        # This function sets up the connection to the database
        # This is needed everytime a new connection to the database is created
    
        try:
            self.connection = pyodbc.connect(self.conn_string, autocommit=True)
            print("Connection established successfully.")
            
             # retrieve one record
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM urls")
            row = cursor.fetchone()
            print(row)
            cursor.close()
            print("Tried retrieving one record.")   
        except pyodbc.Error as e:
            print(f"Error: {e}")
            raise e
      
    def cleanup(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection closed.")
            
    def checkDuplicate(self, short_url):
        # if self.isClosed():
        #     self.connectSQL()
        cursor = None
        try:
            cursor = self.connection.cursor()
    
            # SQL query to check if the short_code exists
            query = '''
            SELECT COUNT(*) 
            FROM urls 
            WHERE short_url = ?;
            '''
        
            # Execute the query
            cursor.execute(query, (short_url,))
            result = cursor.fetchone() # -> (0,) 
            self.connection.commit()
            if result and result[0] > 0:
                return True
            else:
                return False
        except pyodbc.Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
    
    def retrieveRecord(self, short_url):
        # if self.isClosed():
        #     self.connectSQL()
        cursor = None
        try:
            cursor = self.connection.cursor()
    
            # SQL query to check if the short_code exists
            query = '''
            SELECT original_url
            FROM urls 
            WHERE short_url = ?;
            '''
        
            # Execute the query
            cursor.execute(query, (short_url,))
            result = cursor.fetchone()
            self.connection.commit()
            if result and len(result) > 0:
                return True, result[0]
            else:
                return False, None
        except pyodbc.Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
    
    def insertRecord(self, short_url, original_url, expiry_time):
        # if self.isClosed():
        #     self.connectSQL()
        cursor = None
        try:
            cursor = self.connection.cursor()
    
            # SQL query to check if the short_code exists
            query = '''
            INSERT INTO urls (short_url, original_url, expires_at)
            VALUES (?, ?, ?);
            '''
        
            # Execute the query
            cursor.execute(query, (short_url, original_url, expiry_time))
            self.connection.commit()
        except pyodbc.Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
    # record expiry
    # DELETE FROM urls WHERE expires_at < SYSDATETIMEOFFSET() AT TIME ZONE 'UTC';
    