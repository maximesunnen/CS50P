import sqlite3
from helpers import get_item_input, get_quantity_input
from tabulate import tabulate
import re
import sys

def connect_db(DB_FILE_NAME):
    """
    Open a connection to a SQLite database. If a sqlite3.Error is raised, exits the program.
    :param DB_FILE_NAME: The path to the database file to be opened
    :type DB_FILE_NAME: string
    """
    con = None
    
    try:
        db = sqlite3.connect(DB_FILE_NAME)
        return db
    except sqlite3.Error as e:
        sys.exit(f"Error connecting to the database: {e}")
    
def init_db(DB_FILE_NAME, SCHEMA_SQL):
    """
    Initialize the database.
    :param str DB_FILE_NAME: Path to the database file to be opened
    :param str SCHEMA_SQL: Path to the schema.sql file to be used for initialization
    """
    with connect_db(DB_FILE_NAME) as db:
        cur = db.cursor()
    
        with open(SCHEMA_SQL) as f:
            cur.executescript(f.read())
    
def load_db(DB_FILE_NAME):
    """
    Load the database into memory as a dict object.
    :param str DB_FILE_NAME: Path to the database file to be loaded
    """
    with connect_db(DB_FILE_NAME) as db:
        # change row_factory
        db.row_factory = sqlite3.Row
        cur = db.cursor()
    
        # fetch data
        cur.execute("SELECT * FROM inv")
        
        dict = {}

        for r in cur.fetchall():
            dict.update({r["item"]: r["quantity"]})
    
    return dict

def add_item(inv, db, cur):
    """
    Add item to the database. Return True if the user pressed CTRL+D, False otherwise.
    :param dict inv: Dict object representing the database.
    :param sqlite3.Connection db: A SQLite database connection.
    :param sqlite3.Cursor cur: A SQLite Cursor instance.
    """
    
    # Get item
    item = get_item_input("Item to add")
    
    if item is None:
        return True
    
    # Get quantity and validate
    quantity = get_quantity_input("Quantity")
    
    if quantity is None:
        return True
        
    try:
        quantity = int(quantity)
    except ValueError:
        print("Invalid quantity")
        return False
    
    # Validate inputs and add items
    if item in inv:
        inv[item] += quantity
    else:
        inv.update({item: quantity})

    try:
        cur.execute("INSERT INTO inv (item, quantity) VALUES (?, ?) ON CONFLICT(item) DO UPDATE SET quantity = ?", (item, inv.get(item), inv.get(item)))
    except db.IntegrityError:
        print("Error 003: db.IntegrityError")

    return False

def remove_item(inv, db, cur):
    """
    Get item and quantity, validate and remove item from the database. Returns True to signal program exit, False otherwise.
    """
    # Get item
    item = get_item_input("Item to remove")
    
    if item is None:
        return True
    
    if item not in inv:
        print("Item not in inventory")
        return False
    
    # Get quantity and validate
    quantity = get_quantity_input("Quantity")
    
    if quantity is None:
        return True
    
    try:
        if (quantity := int(quantity)) > inv.get(item, 0):
            print("Removing more items than you own")
            return False
    except ValueError:
        print("Invalid quantity")
        return False
    
    # database logic
    inv[item] -= quantity
    
    try:
        cur.execute("UPDATE inv SET quantity = ? WHERE item = ?", (inv.get(item), item))
    except db.IntegrityError:
        print("Error 005: db.IntegrityError")
        
    return False

def find_item(inv):
    """
    Find item in inventory using regular expression matching. Return list of matching items.
    """
    item = get_item_input("Search item")
    
    if item is None:
        sys.exit(0)
    
    # Regular expression
    pattern = re.compile(f"^.*{item}.*$")

    # find matches
    matching_data = [[key, value] for key, value in inv.items() if pattern.match(key)]
    
    return item, matching_data

    
def tabulate_db(DB_FILE_NAME):
    # load database as dict
    inv = load_db(DB_FILE_NAME)

    inv_list = []

    for key in inv.keys():
        inv_list.append([key, inv[key]])
        
    return tabulate(inv_list, tablefmt="grid", headers=["Item", "Quantity"])