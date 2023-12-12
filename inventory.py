import argparse
import sys
from tabulate import tabulate

from db import connect_db, init_db, load_db, add_item, tabulate_db, find_item, remove_item


DB_FILE_NAME = "inv.db"
SCHEMA_SQL = "schema.sql"

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
        # initialize db
        init_db(DB_FILE_NAME, SCHEMA_SQL)
        print("Database initialized.")
        sys.exit(0)
    
    elif args.a:
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            func = False
            while func is False:
                func = add_item(inv, db, cur)

            db.commit()
        
        # print db as table
        table = tabulate_db(DB_FILE_NAME)
        print(table)
        
    elif args.f:
        while True:
            item, matching_data = find_item(inv)
            
            if matching_data:
                print(tabulate(matching_data, headers=["Item", "Quantity"], tablefmt="grid"))
            else:
                print(f"{item} not in inventory")
                
    elif args.r:
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            func = False
            while func is False:
                func = remove_item(inv, db, cur)
            
            db.commit()
            
        # print db as table
        table = tabulate_db(DB_FILE_NAME)
        print(table)

if __name__ == "__main__":
    main()