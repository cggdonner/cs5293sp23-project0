# Import os and sys to link test file to file in another directory
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then reference and import incidentcounter.py from the project0 folder
from project0 import incidentcounter

# Import sqlite3
import sqlite3

# Test createdb() function
def test_createdb():
    # If createdb() was executed, that means that you connected to the normanpd.db database successfully
    incidentcounter.createdb()
    conn = sqlite3.connect("normanpd.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * from incidents") # Also show that incidents table has been created 
    cursor.fetchall()
    conn.close()
    print(f"Connected to database!")
