import sqlite3
# PRAGMA FOREIGN KEYS = ON
conn = sqlite3.connect('banksys.db')

conn.execute('''CREATE TABLE IF NOT EXISTS  banks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE,
location TEXT NOT NULL
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS  customers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT NOT NULL,
phon_num TEXT NOT NULL,
address TEXT NOT NULL,
acct_num TEXT NOT NULL UNIQUE,
amount INTEGER,
acct_type TEXT,
bank_id TEXT,
FOREIGN KEY(acct_type) REFERENCES accounts(acct_type),
FOREIGN KEY(bank_id) REFERENCES banks(name)
);''')
#


conn.execute('''CREATE TABLE IF NOT EXISTS  tellers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
resp_bank TEXT,
location TEXT NOT NULL,
FOREIGN KEY (resp_bank) REFERENCES banks(name)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS accounts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
acct_type TEXT NOT NULL UNIQUE
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS loans(
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount TEXT NOT NULL,
reason TEXT NOT NULL,
period TEXT NOT NULL,
status INTEGER,
bank_id TEXT,
acct_num TEXT,
FOREIGN KEY (bank_id) REFERENCES banks(name),
FOREIGN KEY (acct_num) REFERENCES customers(acct_num)
);''')

conn.close()

