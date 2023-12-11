import argparse
import sys

from db import connect_db, init_db

def main():
    # Add CL argument to initialize datbase
    parser = argparse.ArgumentParser()
    parser.add_argument("-init", action="store_true")
    args = parser.parse_args()
    
    # Create and/or initialize database
    if args.init:
        connection = connect_db("inv.db")
        init_db(connection)
        
        print("Database initialized.")
        sys.exit(0)
 
if __name__ == "__main__":
    main()