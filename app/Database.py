

import psycopg2
import psycopg2.extras

class Database:
    def __init__(self, host:str, user:str, password:str, database:str):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    

             
    def select(self, table:str = '', fields:list = [], where:dict = []):
        if not fields:
            fields =['*']
        where_query = '' 
        if where :
            where_query = 'AND '+' AND '.join(f"{key} = '{value}'" for key, value in where.items())
            
        sql = f"SELECT {','.join(fields)} FROM {table} WHERE 1=1 {where_query}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    

    def insert(self, table:str, data:dict):
        columns = ', '.join(data.keys())
        values = ', '.join("'" + str(v) + "'" for v in data.values())
        self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        self.connection.commit()
    
    def delete(self, table:str, where:dict = {})-> bool:
        where_query = ''
        if where :
            where_query = 'AND '+' AND '.join(f"{key} = '{value}'" for key, value in where.items())
            
        sql = f"DELETE FROM {table} WHERE 1=1 {where_query}"
        self.cursor.execute(sql)
        self.connection.commit()
    
        return self.cursor.rowcount >= 1
    

    def close(self):
        self.cursor.close()
        self.connection.close()