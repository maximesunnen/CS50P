from project import add_item, remove_item, find_item
from db import load_db
from db import connect_db
import pytest
import sqlite3

SCHEMA_SQL = "schema.sql"
DB_FILE_NAME = "inv.db"
TEST_DB_FILE_NAME = "test_inv.db"

TEST_ITEM_1 = "MILK"
TEST_ITEM_2 = "CAFÉ"
TEST_ITEM_3 = "SUGAR"

TEST_QUANTITY_1 = 5
TEST_QUANTITY_2 = 10
TEST_QUANTITY_3 = 1

class TestClass:
    @classmethod
    def init_db(cls):
        """
        Initialize the testing db.
        """

        with connect_db(TEST_DB_FILE_NAME) as db:
            cur = db.cursor()
        
            with open(SCHEMA_SQL) as f:
                cur.executescript(f.read())
            
            print(("Test db initialized."))
            
    def test_connect_db(self):
        """
        Test connection to the main database.
        """
        db = connect_db(DB_FILE_NAME)
        
        assert isinstance(db, sqlite3.Connection)

    def test_add_item(self):
        # Initialize db
        self.init_db()
                
        # Load the db as dict
        inv = load_db(TEST_DB_FILE_NAME)
        
        # Connect to db
        with connect_db(TEST_DB_FILE_NAME) as db:
            cur = db.cursor()
            
            # Add item to the db
            add_item(TEST_ITEM_1, TEST_QUANTITY_1, inv, cur)
            item_1 = cur.execute("SELECT item FROM inv").fetchone()[0]
            
            # Add second item to the db
            add_item(TEST_ITEM_2, TEST_QUANTITY_2, inv, cur)
            item_2 = cur.execute("SELECT item FROM inv").fetchone()[0]
        
        assert item_1 == TEST_ITEM_1
        assert item_2 == TEST_ITEM_2
        
    def test_remove_item(self):
        # Initialize db
        self.init_db()
        
        # Load the db as dict
        inv = load_db(TEST_DB_FILE_NAME)
        
        # Connect to db
        with connect_db(TEST_DB_FILE_NAME) as db:
            cur = db.cursor()
            
            # Add test items to the db
            add_item(TEST_ITEM_1, TEST_QUANTITY_1, inv, cur)
            add_item(TEST_ITEM_2, TEST_QUANTITY_2, inv, cur)
            add_item(TEST_ITEM_3, TEST_QUANTITY_3, inv, cur)

            # Remove test items from the db
            remove_item(TEST_ITEM_1, 1, inv, cur)
            remove_item(TEST_ITEM_2, 1, inv, cur)
            remove_item(TEST_ITEM_3, 1, inv, cur)
            
            quantity_1 = cur.execute("SELECT quantity FROM inv WHERE item = ?", (TEST_ITEM_1,)).fetchone()[0]
            quantity_2 = cur.execute("SELECT quantity FROM inv WHERE item = ?", (TEST_ITEM_2,)).fetchone()[0]
        
        assert quantity_1 == TEST_QUANTITY_1 - 1
        assert quantity_2 == TEST_QUANTITY_2 - 1
        
        # Test that items with quantity = 0 are completely removed from the db
        with pytest.raises(TypeError):
            cur.execute("SELECT quantity FROM inv WHERE item = ?", (TEST_ITEM_3,)).fetchone()[0]
            
    def test_find_item(self):
        # Initialize db
        self.init_db()
        
        # Load the db as dict
        inv = load_db(TEST_DB_FILE_NAME)
        print(inv)
        
        # Add test item to the db
        with connect_db(TEST_DB_FILE_NAME) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            add_item(TEST_ITEM_1, TEST_QUANTITY_1, inv, cur)
            cur.execute("SELECT * FROM inv")
        
        # Load the db as dict
        inv = load_db(TEST_DB_FILE_NAME)
        print(inv)
        
        # Find item
        _, matching_data = find_item(TEST_ITEM_1, inv)
        assert matching_data == [(TEST_ITEM_1, TEST_QUANTITY_1)]
        
        _, matching_data = find_item(TEST_ITEM_2, inv)
        assert matching_data == []