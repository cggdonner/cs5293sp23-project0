# Import os and sys to link test file to file in another directory
import os
import sys
import sqlite3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then reference and import incidentcounter.py from the project0 folder
from project0 import incidentcounter

# Test populatedb() function
def test_populatedb(url = 'https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf', term = 'Drunk Driver'):
    incidents = incidentcounter.fetchincidents(url)
    incidentcounter.createdb()
    
    # Connect to database to fetch rows from incidents table
    conn = sqlite3.connect("normanpd.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM incidents""")
    rows = cursor.fetchall()

    # Assertions based on the rows from the incidents table retrieved using the fetchall() method
    assert len(rows) == len(incidents)
    print(f"Length test passed")
    for i,row in enumerate(rows):
        assert row[1] == incidents[i][0]
        assert row[2] == incidents[i][1]
        assert row[3] == incidents[i][2]
        assert row[4] == incidents[i][3]
        assert row[5] == incidents[i][3]
        assert row[6] == incidents[i][4]
    for row in rows:
        assert row[5] == term
    print(f"{term} passed test!")
