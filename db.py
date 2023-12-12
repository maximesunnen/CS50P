import sqlite3
from sqlite3 import Error
from tabulate import tabulate
from helpers import get_item_input, get_quantity_input
import re
import sys

def connect_db(DB_FILE_NAME):
    """
    Create a database connection to a database that resides in the memory
    """
    con = None
    
    # connect to database
    try:
        db = sqlite3.connect(DB_FILE_NAME)
        return db
    except Error as e:
        print(e)
    
    return sqlite3.connect(DB_FILE_NAME)
    
def init_db(DB_FILE_NAME, SCHEMA_SQL):
    """
    Connect to and initialize database. Side effect function.
    """
    with connect_db(DB_FILE_NAME) as db:
        cur = db.cursor()
    
        with open(SCHEMA_SQL) as f:
            cur.executescript(f.read())
    
def load_db(DB_FILE_NAME):
    """
    Load the database as a dict. Each item-quantity pair in the database becomes
    a key-value pair in the dict.
    """
    with connect_db(DB_FILE_NAME) as db:
        # change row_factory, create cursor
        db.row_factory = sqlite3.Row
        cur = db.cursor()
    
        # fetch db data
        cur.execute("SELECT * FROM inv")
        
        dict = {}

        for r in cur.fetchall():
            dict.update({r["item"]: r["quantity"]})
    
    return dict

def add_item(inv, db, cur):
    """
    Add item to the database. 
    Return True if the user pressed CTRL+D, otherwise return False
    """
    
    # Get inputs
    item = get_item_input("Item to add")
    
    if item is None:
        return True
    
    quantity = get_quantity_input("Quantity")
    
    if quantity is not None:
        try:
            quantity = int(quantity)
        except ValueError:
            print("Invalid quantity")
            return False
    else:
        return True
    
    # Validate inputs and add items
    if item in inv:
        inv[item] += quantity
        
        try:
            cur.execute("UPDATE inv SET quantity = ? WHERE item = ?", (inv.get(item), item))
        except db.IntegrityError:
            print("Error 003: db.IntegrityError")

    else:
        try:
            inv.update({item: quantity})
            cur.execute("INSERT INTO inv (item, quantity) VALUES (?, ?)", (item, quantity))
        except db.IntegrityError:
            print("Error 003: db.IntegrityError")
        
    return False

def tabulate_db(DB_FILE_NAME):
    # load database as dict
    inv = load_db(DB_FILE_NAME)
    
    inv_list = []
    
    for key in inv.keys():
        inv_list.append([key, inv[key]])
        
    return tabulate(inv_list, tablefmt="grid", headers=["Item", "Quantity"])

def find_item(inv):
    item = get_item_input("Search item")
    
    if item is None:
        sys.exit(0)
    
    # regular expression
    pattern = re.compile(f"^.*{item}.*$")

    # find matches
    matching_data = [[key, value] for key, value in inv.items() if pattern.match(key)]
    
    return item, matching_data

def remove_item(inv, db, cur):
    """
    Get and verify inputs and remove them from the database. Returns True to signal program exit, False otherwise.
    """
    # item input
    item = get_item_input("Item to remove")
    
    if item is None:
        return True
    
    if item not in inv:
        print("Item not in inventory")
        return False
    
    # quantity input
    quantity = get_quantity_input("Quantity")
    
    if quantity is None:
        return True
    
    try:
        quantity = int(quantity)
    except ValueError:
        print("Quantity is not an integer")
        return False

    if quantity > inv.get(item, 0):
        print("Removing more items than you own")
        return False
    
    # database logic
    inv[item] -= quantity
    
    try:
        cur.execute("UPDATE inv SET quantity = ? WHERE item = ?", (inv.get(item), item))
    except db.IntegrityError:
        print("Error 005: db.IntegrityError")
        
    return False