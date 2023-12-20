# CS50P- Introduction to programming with Python
Command-line tool to interact with an inventory implemented as a SQL database using sqlite3.

## Usage

`python3 project.py [-h] [-i] [-a] [-r] [-f] [-v]`

>[!CAUTION]
>
> You **need** to [initialize](#python3-project.py--i) the database before using this tool. This generates an `inv.db` file in your working directory.

To exit the program, use **CTRL+D**.

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

CREATE TABLE inv (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item TEXT NOT NULL UNIQUE,
  quantity INTEGER NOT NULL
);
```

>[!NOTE]
>Before initialization, you will have to confirm your choice:
>
>`Are you sure you want to initialize the database? (y/n)`

### `python3 project.py -a`
Adds an item to the database.

1. Enter item to insert:

```
> python3 project.py -a
  Item to add: coffee 150g
```

2. Enter quantity to insert:
```
> python3 project.py -a
  Item to add: coffee 150g
  Quantity: 5
```

>[!WARNING] 
> The quantity must be an integer. Thus, you cannot remove a fraction of an item.

3. A confirmation message appears and you're prompted for the next item to add:
```
> python3 project.py -a
  Item to add: coffee 150g
  Quantity: 5
  Added 5 COFFEE 150G to the inventory!
  Item to add:
```

### `python3 project.py -r`
Removes item from the database.

1. Enter the item to remove from the database:

```
> python3 project.py -r
  Item to remove: coffee 150g
```

2. Enter the quantity to remove from the database:
```
> python3 project.py -r
  Item to remove: coffee 150g
  Quantity: 2
```

3. A confirmation message appears and you're prompted for the next item to remove:
```
> python3 project.py -r
  Item to remove: coffee 150g
  Quantity: 5
  Removed 2 COFFEE 150G to the inventory!
  Item to remove:
```

>[!WARNING] 
> 1. You cannot remove more items than you own:
>```
> python3 project.py -r
>  Item to remove: coffee 150g
>  Quantity: 1000
>  Trying to remove more items than you own!
>  Item to remove:
>```
> 2. You **must** spell the item to remove exactly as it is saved inside the database. This can definitely be improved in the future.

### `python3 project.py -f`
Finds items in the database based on regular expression pattern matching.

1. Enter the item you want to find:

```
> python3 project.py -f
  Search item: coffee
```

>[!NOTE] 
> Note that you **don't** have to name items exactly as they're stored inside the database. Here, I replaced "coffee 150g" by "coffee", but the searching will still work. This is because I use the following regexp to look for items:
>
>`pattern = re.compile(f"^.*{item}.*$")`

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
