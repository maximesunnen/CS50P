import sqlite3
import sys

from tabulate import tabulate
from termcolor import colored

def connect_db(DB_FILE_NAME):
    """
    Open a connection to a SQLite database. If a sqlite3.Error is raised, exits the program.
    :param DB_FILE_NAME: The path to the database file to be opened
    :type DB_FILE_NAME: string
    """
    
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
    
    confirm = input("Are you sure you want to initialize the database? (y/n) ").upper()
    
    while confirm not in ["Y", "N", "YES", "NO"]:
        confirm = input("Are you sure you want to initialize the database? (y/n) ").upper()

    if confirm == "Y" or confirm == "YES":
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
        
            with open(SCHEMA_SQL) as f:
                cur.executescript(f.read())
        print(colored("Database initialized.", "black", "on_white"))
        
    else:
        print(colored("Canceled database initialization.", "black", "on_white"))
    
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
    
def tabulate_db(inv):
    """
    Return plain-text table of inventory.
    :param str inv: dictionary of database
    """

    inv_list = []

    for key in sorted(inv.keys()):
        inv_list.append([key, inv[key]])
        
    return tabulate(inv_list, tablefmt="grid", headers=["Item", "Quantity"])