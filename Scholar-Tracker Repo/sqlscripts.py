import sqlite3
import traceback
from utility.checkaddress import is_valid_address
database = 'scholars.db'
try:
        
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE scholars(
            name TEXT,
            address TEXT,
            cut REAL
        )
        '''
    )
    conn.commit()
    conn.close()
except Exception:
    pass

class QueryError(Exception):
    pass

def add_scholar(name,address,cut):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("INSERT INTO scholars VALUES(?,?,?)",(name,address,cut))
    conn.commit()
    conn.close()
    
def get_scholar_data(target):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if(is_valid_address(target)):
        c.execute(f"SELECT * FROM scholars WHERE address='{target}'")
    else:
        c.execute(f"SELECT * FROM scholars WHERE name='{target}'")
    data = c.fetchall()
    conn.close()
    return data

def get_all_scholar_data():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM scholars")
    data = c.fetchall()
    conn.close()
    return data

def delete_scholar(address):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if(is_valid_address(address)):
        c.execute("DELETE FROM scholars WHERE address= ?",(address,))
    else:
        c.execute("DELETE FROM scholars WHERE name= ?",(address,))
    if(c.rowcount<1):
        raise QueryError("Query operation is not successful")
    conn.commit()
    conn.close()

def edit_cut(target,change):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if(is_valid_address(target)):
        c.execute(f" UPDATE scholars SET cut = ? WHERE address = '{target}'", (change,))
    else:
        c.execute(f" UPDATE scholars SET cut = ? WHERE name = '{target}'", (change,))
    if(c.rowcount<1):
        raise QueryError("Query operation is not successful")
    conn.commit()
    conn.close()

def edit_name(target,name):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if(is_valid_address(target)):
        c.execute(f" UPDATE scholars SET name = ? WHERE address = ?", (name,target))   
    if(c.rowcount<1):
        raise QueryError("Query operation is not successful")
    conn.commit()
    conn.close()

