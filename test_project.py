from project import add_item, remove_item, find_item
from db import load_db
from db import connect_db
import pytest

SCHEMA_SQL = "schema.sql"
DB_FILE_NAME = "test_inv.db"

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

        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
        
            with open(SCHEMA_SQL) as f:
                cur.executescript(f.read())
            
            print(("Test db initialized."))

    def test_add_item(self):
        # Initialize db
        self.init_db()
                
        # Load the db as dict
        inv = load_db(DB_FILE_NAME)
        
        # Connect to db
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            # Add item to the db
            add_item(TEST_ITEM_1, TEST_QUANTITY_1, inv, db, cur)
            item_1 = cur.execute("SELECT item FROM inv").fetchone()[0]
            
            # Add second item to the db
            add_item(TEST_ITEM_2, TEST_QUANTITY_2, inv, db, cur)
            item_2 = cur.execute("SELECT item FROM inv").fetchone()[0]
        
        assert item_1 == TEST_ITEM_1
        assert item_2 == TEST_ITEM_2
        
    def test_remove_item(self):
        # Initialize db
        self.init_db()
        
        # Load the db as dict
        inv = load_db(DB_FILE_NAME)
        
        # Connect to db
        with connect_db(DB_FILE_NAME) as db:
            cur = db.cursor()
            
            # Add test item to the db
            add_item(TEST_ITEM_1, TEST_QUANTITY_1, inv, db, cur)
            add_item(TEST_ITEM_2, TEST_QUANTITY_2, inv, db, cur)
            add_item(TEST_ITEM_3, TEST_QUANTITY_3, inv, db, cur)

            # Remove test item from the db
            remove_item(TEST_ITEM_1, 1, inv, db, cur)
            remove_item(TEST_ITEM_2, 1, inv, db, cur)
            remove_item(TEST_ITEM_3, 1, inv, db, cur)
            
            quantity_1 = cur.execute("SELECT quantity FROM inv WHERE item = ?", (TEST_ITEM_1,)).fetchone()[0]
            quantity_2 = cur.execute("SELECT quantity FROM inv WHERE item = ?", (TEST_ITEM_2,)).fetchone()[0]
        
        assert quantity_1 == TEST_QUANTITY_1 - 1
        assert quantity_2 == TEST_QUANTITY_2 - 1
        
        with pytest.raises(TypeError):
            cur.execute("SELECT quantity FROM inv WHERE item = ?", (TEST_ITEM_3,)).fetchone()[0]