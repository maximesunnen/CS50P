DROP TABLE IF EXISTS inv;

-- Table to store user (child) information
CREATE TABLE inv (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item TEXT NOT NULL,
  quantity INTEGER NOT NULL
);