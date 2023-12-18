import sqlite3
import argparse
import sys
from tabulate import tabulate
from termcolor import colored
from helpers import get_item_input, get_quantity_input, is_valid_quantity
import re
from db import connect_db, init_db, load_db, tabulate_db

DB_FILE_NAME = "inv.db"
SCHEMA_SQL = "schema.sql"

def main():
    # argpase config
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "-init", action="store_true", help="Initialize the database")
    
    parser.add_argument("-a", "-add", action="store_true", help="Add item(s) to the inventory")
    parser.add_argument("-r", "-remove", action="store_true", help="Remove item(s) from the inventory")
    
    parser.add_argument("-f", "-find", action="store_true", help="Find item(s) in the inventory")
    
    parser.add_argument("-v", "-view", action="store_true", help="View item(s) in the inventory")
    
    args = parser.parse_args()
    
    # create and/or initialize database
    if args.i:
        # initialize db
        init_db(DB_FILE_NAME, SCHEMA_SQL)
        sys.exit(0)
    
    elif args.a:
        # Load db into memory (type(inv): dict)
        inv = load_db(DB_FILE_NAME)
        
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            while True:
                # Get item
                if (item := get_item_input("Item to add")) is None:
                    break
                
                # Get quantity and validate
                if (quantity := get_quantity_input("Quantity")) is None:
                    break
                
                if (quantity := is_valid_quantity(quantity)) is False:
                    continue

                # Add item to db
                status = add_item(item, quantity, inv, db, cur)
                
                if status is True:
                    print(colored(f"Added {quantity} {item} to the inventory!", "green"))
                else:
                    sys.exit(colored(status))

            db.commit()
        
        # Print db as table
        print(tabulate_db(DB_FILE_NAME))
        
    elif args.r:
        # Load db into memory (type(inv): dict)
        inv = load_db(DB_FILE_NAME)
        
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            while True:
                # Get item and validate
                if (item := get_item_input("Item to remove")) is None:
                    break
                
                if item not in inv:
                    print(colored("Item not in inventory!", "yellow"))
                    continue
                
                # Get quantity and validate
                if (quantity := get_quantity_input("Quantity")) is None:
                    break
                
                try:
                    quantity = int(quantity)
                except ValueError:
                    print(colored("Invalid quantity!", "yellow"))
                    continue
                
                if quantity > inv.get(item, 0):
                    print(colored("Trying to remove more items than you own!", "yellow"))
                    continue
                
                # Remove item from db
                status = remove_item(item, quantity, inv, db, cur)
                
                if status is True:
                    print(colored(f"Removed {quantity} {item} from the inventory!", "green"))
                else:
                    continue
            
            db.commit()

        # Print db as table
        print(tabulate_db(DB_FILE_NAME))

    elif args.f:
        # load db into memory (type(inv): dict)
        inv = load_db(DB_FILE_NAME)
        
        while True:
            item, matching_data = find_item(inv)
            
            if matching_data:
                print(tabulate(matching_data, headers=["Item", "Quantity"], tablefmt="grid"))
            else:
                print(f"{item} not in inventory")
                
    elif args.v:
        print(tabulate_db(DB_FILE_NAME))
        
        
def add_item(item, quantity, inv, db, cur):
    """
    Add item to the database. Return True if no exception raised. Return the db.IntegrityError otherwise.
    :param dict inv: Dict object corresponding to the database.
    :param sqlite3.Connection db: A SQLite database connection.
    :param sqlite3.Cursor cur: A SQLite Cursor instance.
    """

    if item in inv:
        inv[item] += quantity
    else:
        inv.update({item: quantity})

    try:
        cur.execute("INSERT INTO inv (item, quantity) VALUES (?, ?) ON CONFLICT(item) DO UPDATE SET quantity = ?", (item, inv.get(item), inv.get(item)))
    except db.IntegrityError as e:
        return e

    return True

def remove_item(item, quantity, inv, db, cur):
    """
    Get item and quantity, validate and remove item from the database. Returns True to signal program exit, False otherwise.
    :param dict inv:
    :param sqlite3.Connection db: A SQLite database connection.
    :param sqlite3.Cursor cur: A SQLite Cursor instance.
    """
        
    if quantity == inv.get(item, 0):
        try:
            cur.execute("DELETE FROM inv WHERE item = ?", (item,))
            return True
        except sqlite3.Error as e:
            print(colored(f"Error deleting row: {e}", "red"))
            return False
    else:    
        inv[item] -= quantity
        
        try:
            cur.execute("UPDATE inv SET quantity = ? WHERE item = ?", (inv.get(item), item))
            return True
        except db.IntegrityError as e:
            print(colored("Error updating row: {e}", "red"))
            return False

def find_item(inv):
    """
    Find item in inventory using regular expression matching. Return list of matching items.
    :param dict inv: Dict object corresponding to the database.
    """
    item = get_item_input("Search item")
    
    if item is None:
        sys.exit(0)
    
    # Regular expression
    pattern = re.compile(f"^.*{item}.*$")

    # find matches
    matching_data = [[key, value] for key, value in inv.items() if pattern.match(key)]
    
    return item, matching_data

if __name__ == "__main__":
    main()