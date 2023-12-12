import argparse
import sys
from tabulate import tabulate

import re

from db import connect_db, init_db, load_db, add_item, db_to_table, find_item

DB_FILE_NAME = "inv.db"

def main():
    # argpase config
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "-init", action="store_true", help="Initialize the database")
    
    parser.add_argument("-a", "-add", action="store_true", help="Add item(s) to the inventory")
    parser.add_argument("-r", "-remove", action="store_true", help="Remove item(s) from the inventory")
    parser.add_argument("-f", "-find", action="store_true", help="Find item(s) in the inventory")
    
    args = parser.parse_args()
    
    # load db into memory (type(inv): dict)
    inv = load_db(DB_FILE_NAME)
    
    # create and/or initialize database
    if args.i:
        # connect to db
        con = connect_db(DB_FILE_NAME)
        
        # initialize db
        init_db(con)
        
        print("Database initialized.")
        sys.exit(0)
    
    elif args.a:
        # connect to db; create cursor
        db = connect_db(DB_FILE_NAME)
        cur = db.cursor()
        
        # initialize func variable
        func = False
        
        while func == False:
            func = add_item(cur, inv)

        # commit changes and close connection
        db.commit()
        db.close()
        
        # print database as table
        table = db_to_table(DB_FILE_NAME)
        print(table)
        
    elif args.f:
        while True:
            item, matching_data = find_item(inv)
            
            if matching_data:
                print(tabulate(matching_data, headers=["Item", "Quantity"], tablefmt="grid"))
            else:
                print(f"{item} not in inventory")

if __name__ == "__main__":
    main()