import sqlite3
import argparse
import sys
import re
from tabulate import tabulate
from termcolor import colored
from typing import List, Dict, Tuple

from helpers import get_item_input, get_quantity_input, is_valid_quantity
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
    
    # Initialize db if -i flag; otherwise load db as dict
    if args.i:
        init_db(DB_FILE_NAME, SCHEMA_SQL)
        sys.exit(0)
    else:
        inv = load_db(DB_FILE_NAME)
    
    # Add item to db if -a flag
    if args.a:        
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            while True:
                # Get item and quantity
                if (item := get_item_input("Item to add")) is None:
                    break
                
                if (quantity := get_quantity_input("Quantity")) is None:
                    break
                
                # Validate quantity
                if (quantity := is_valid_quantity(quantity)) is False:
                    continue

                # Add item to db. add_item returns True or db.IntegrityError
                added = add_item(item, quantity, inv, cur)
                
                if added is True:
                    print(colored(f"Added {quantity} {item} to the inventory!", "green"))
                else:
                    sys.exit(colored(added))

            # Commit db changes
            db.commit()
        
        # Print db as table
        print(tabulate_db(inv))
        
    elif args.r:
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            while True:
                # Get item and quantity
                if (item := get_item_input("Item to remove")) is None:
                    break
                
                if item not in inv:
                    print(colored("Item not in inventory!", "yellow"))
                    continue
                
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
                removed = remove_item(item, quantity, inv, cur)

                if removed is True:
                    print(colored(f"Removed {quantity} {item} from the inventory!", "green"))
                else:
                    sys.exit(colored(removed))
            
            db.commit()

        # Print db as table
        print(tabulate_db(inv))

    elif args.f:

        while True:
            # Get item
            if (item := get_item_input("Search item")) is None:
                sys.exit(0)
        
            item, matching_data = find_item(item, inv)
            
            if matching_data:
                print(tabulate(matching_data, headers=["Item", "Quantity"], tablefmt="grid"))
                continue
            else:
                print(colored(f"{item} not in inventory", "yellow"))
                continue
                
    elif args.v:
        print(tabulate_db(inv))
        
def add_item(item: str, quantity: int, inv: Dict[str, int], cur: sqlite3.Cursor) -> bool:
    """
    Add item to the database. Return True if no exception raised. Return db.IntegrityError otherwise.
    :param str item: Item to add.
    :param str quantity: Quantity of item to add.
    :param dict[str, int] inv: Database as a dict object.
    :param sqlite3.Cursor cur: SQLite Cursor instance.
    :rtype: bool
    """

    try:
        if item in inv:
            cur.execute("UPDATE inv SET quantity = ? WHERE item = ?", (inv[item]+quantity, item))
            inv[item] += quantity
        else:
            cur.execute("INSERT INTO inv (item, quantity) VALUES (?, ?)", (item, quantity))
            inv.update({item: quantity})
    except sqlite3.Error as e:
        print(colored(f"Error: {e}", "red"))
        return False
    
    return True

def remove_item(item: str, quantity: int, inv: Dict[str, int], cur: sqlite3.Cursor) -> bool:
    """
    Remove item from the database. Returns True after successful SQL execution. Return False in case of a sqlite3.Error or KeyError.
    :param str item: Item to add.
    :param str quantity: Quantity of item to add.
    :param dict[str, int] inv: Database as a dict object.
    :param sqlite3.Cursor cur: SQLite Cursor instance.
    :rtype: bool
    """

    try:
        if quantity == inv.get(item, 0):
            cur.execute("DELETE FROM inv WHERE item = ?", (item,))
            inv.pop(item)
        else:   
            cur.execute("UPDATE inv SET quantity = ? WHERE item = ?", (inv[item]-quantity, item))
            inv[item] -= quantity
    except (sqlite3.Error, KeyError) as e:
        print(colored(f"Error: {e}", "red"))
        return False
    
    return True

def find_item(item: str, inv: Dict[str, int]) -> Tuple[str, List[Tuple[str, int]]]:
    """
    Find item in inventory using regular expression matching. Return list of matching items.
    :param str item: Item to add.
    :param dict inv: Dict object corresponding to the database.
    :rtype: Tuple[str, List[Tuple[str, int]]]]
    """

    # Search pattern
    pattern = re.compile(f"^.*{item}.*$")

    # Find matches
    matching_data = [(key, value) for key, value in inv.items() if pattern.match(key)]
    
    return item, matching_data

if __name__ == "__main__":
    main()