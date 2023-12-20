# CS50P- Introduction to programming with Python
Command-line tool to interact with an inventory implemented as a SQL database using sqlite3. Navigation using CL flags.

## Usage

`python3 project.py [-h] [-i] [-a] [-r] [-f] [-v]`

To exit the program at any stage, use **CTRL+D**.

## Flags

```
options:
  -h, --help   show this help message and exit
  -i, -init    Initialize the database
  -a, -add     Add item(s) to the inventory
  -r, -remove  Remove item(s) from the inventory
  -f, -find    Find item(s) in the inventory
  -v, -view    View item(s) in the inventory
```

### `python3 project.py -i`
Deletes existing tables and recreates the database using the SQL commands in `schema.sql`:

```
DROP TABLE IF EXISTS inv;

-- Table to store user (child) information
CREATE TABLE inv (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item TEXT NOT NULL UNIQUE,
  quantity INTEGER NOT NULL
);
```

**Note:** before initialization, you will be asked at the prompt to confirm your choice:

`Are you sure you want to initialize the database? (y/n)`

### `python3 project.py -a`
Adds item to the database.

First, you have to enter the item to insert into the database:

```
> python3 project.py -a
  Item to add: coffee 150g
```

Second, you have to enter the quantity to insert into the database:
```
> python3 project.py -a
  Item to add: coffee 150g
  Quantity: 5
```

>[!WARNING] 
> The quantity needs to be an integer. Thus, you cannot remove a fraction of an item.

A confirmation message appears and you're prompted for the next item to add:
```
> python3 project.py -a
  Item to add: coffee 150g
  Quantity: 5
  Added 5 COFFEE 150G to the inventory!
  Item to add:
```

### `python3 project.py -r`
Removes item from the database.

First, you have to enter the item to remove from the database:

```
> python3 project.py -r
  Item to remove: coffee 150g
```

Second, you have to enter the quantity to remove from the database:
```
> python3 project.py -r
  Item to remove: coffee 150g
  Quantity: 2
```

A confirmation message appears and you're prompted for the next item to remove:
```
> python3 project.py -r
  Item to remove: coffee 150g
  Quantity: 5
  Removed 2 COFFEE 150G to the inventory!
  Item to remove:
```

>[!WARNING] 
> You cannot remove more items than you own:

>```
> python3 project.py -r
>  Item to remove: coffee 150g
>  Quantity: 1000
>  Trying to remove more items than you own!
>  Item to remove:
>```

### `python3 project.py -f`
Finds item from the database based on regular expression pattern matching.

First, you have to enter the item you want to find in the database:

```
> python3 project.py -f
  Search item: coffee
```

>[!NOTE] 
> Note that you **don't** have to name items exactly as they're stored inside the database. Here, I replaced "coffee 150g" by "coffee", but the searching will still work. This is because I use the following regexp to look for items:

>`pattern = re.compile(f"^.*{item}.*$")``

In case of a match, a table is printed to the console and you're prompted for the next item to search for.

```
> python3 project.py -f
  Search item: coffee
  +--------+------------+
  | Item   |   Quantity |
  +========+============+
  | COFFEE |          3 |
  +--------+------------+
  Search item: 
```

If there's no match, a message is printed.

```
> python3 project.py -r
  Search item: banana
  BANANA not in inventory
```

### `python3 project.py -v`
Displays the entire database as a table in the console.

```
> python3 project.py -v
+----------------------+------------+
| Item                 |   Quantity |
+======================+============+
| CHEDDAR              |          1 |
+----------------------+------------+
| COFFEE               |          3 |
+----------------------+------------+
| CRANBERRY JUICE 1.5L |          1 |
+----------------------+------------+
| MANGO                |          5 |
+----------------------+------------+
| MILK 1L              |          2 |
+----------------------+------------+
```
