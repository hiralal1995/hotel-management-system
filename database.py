import mysql.connector
from mysql.connector import Error
import config

class DatabaseConnection:
    """Handle all database connections and queries"""
    
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Execute SELECT query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing update: {e}")
            self.connection.rollback()
            return False
    
    def execute_insert(self, query, params=None):
        """Execute INSERT query and return last inserted ID"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            print(f"Error executing insert: {e}")
            self.connection.rollback()
            return None

# Global database instance
db = DatabaseConnection()