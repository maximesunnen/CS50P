import sqlite3
from sqlite3 import Error

def connect_db(db_file):
    """ Create a database connection to a database that resides
        in the memory; initialize database using schema.sql file
    """
    connection = None
    
    # Connect to database
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
        return connection
    except Error as e:
        print(e)
    
    return connection
    
def init_db(connection):
    """
    Initialize database. Function with no return value but side effect.
    """
    # Create a new cursor object
    db = connection.cursor()
    
    with open("schema.sql") as f:
        db.executescript(f.read())