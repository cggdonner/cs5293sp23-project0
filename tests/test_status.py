# Import os and sys to link test file to file in another directory
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then reference and import incidentcounter.py from the project0 folder
from project0 import incidentcounter

# Test status() function
def test_status(url = 'https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf'):
    # Call previous functions from incidentcounter.py
    incidents = incidentcounter.fetchincidents(url)
    incidentcounter.createdb()
    incidentcounter.populatedb(incidents)
    
    import sys # To recall the output of status()
    from io import StringIO 
    sys.stdout = StringIO() # Store the output in a StringIO() buffer object
    incidentcounter.status() # Call status()
    output = sys.stdout.getvalue().strip()
    assert "Fireworks | 5" in output # Assert that the number of times Fireworks is in the incident report is 5
