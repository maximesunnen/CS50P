import sqlite3
from sqlite3 import Error
from tabulate import tabulate
import re
import sys

def connect_db(database_file):
    """ Create a database connection to a database that resides
        in the memory; initialize database using schema.sql file
    """
    con = None
    
    # Connect to database
    try:
        con = sqlite3.connect(database_file)
        return con
    except Error as e:
        print(e)
    
    return con
    
def init_db(con):
    """
    Initialize database. Function with no return value but side effect.
    """
    # Create a new cursor object
    cur = con.cursor()
    
    with open("schema.sql") as f:
        cur.executescript(f.read())
        
    con.close()
    
def load_db(database_file):
    # connect to database; change row_factory
    con = connect_db("inv.db")
    con.row_factory = sqlite3.Row
    
    # create a database cursor
    cur = con.cursor()
    
    # fetch data and create dict
    cur.execute("SELECT * FROM inv")
    dict = {}

    for r in cur.fetchall():
        dict.update({r["item"]: r["quantity"]})
        
    # close connection
    con.close()
    
    return dict

def add_item(cur, inv):
    try:
        item = input("Item to add: ").upper().strip()
        quantity = input("Quantity: ").strip()
    except EOFError:
        print("\nExiting program...")
        return True
    
    # convert quantity to int
    try:
        quantity = int(quantity)
    except ValueError:
        print("Invalid quantity")
        return False

    if item in inv.keys():
        # get current quantity
        new_quantity = inv[item] + int(quantity)
        
        cur.execute("UPDATE inv SET quantity = ? WHERE item = ?", (new_quantity, item))
        
    else:
        cur.execute("INSERT INTO inv (item, quantity) VALUES (?, ?)", (item, quantity))
        
    return False

def db_to_table(DB_FILE_NAME):
    # show inventory as table
    inv = load_db(DB_FILE_NAME)
    
    inv_list = []
    
    for key in inv.keys():
        inv_list.append([key, inv[key]])
        
    return tabulate(inv_list, tablefmt="grid")

def find_item(inv):
    try:            
        item = input("Search item: ").upper().strip()
    except EOFError:
        print("\nExiting search.")
        sys.exit(0)
    
    pattern = re.compile(f"^.*{item}.*$")

    matching_data = [[key, value] for key, value in inv.items() if pattern.match(key)]
    
    return item, matching_data