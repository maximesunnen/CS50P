from project import add_item, remove_item, find_item
from db import load_db
from db import connect_db

import pytest

SCHEMA_SQL = "schema.sql"
DB_FILE_NAME = "test_inv.db"

class TestClass:
    @classmethod
    def setup_class(cls):
        """
        Initialize the testing database.
        """

        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
        
            with open(SCHEMA_SQL) as f:
                cur.executescript(f.read())
            
            print(("Test database initialized."))

    def test_add_item(self):
        # Load the database as dict
        inv = load_db(DB_FILE_NAME)
        
        # Connect to db
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            # Add item to the database
            add_item("milk".upper(), 5, inv, db, cur)
            item_1 = cur.execute("SELECT item FROM inv").fetchone()[0]
            
            # Add second item to the database
            add_item("café".upper(), 2, inv, db, cur)
            item_2 = cur.execute("SELECT item FROM inv").fetchone()[0]
        
        assert item_1 == "MILK"
        assert item_2 == "CAFÉ"
        
