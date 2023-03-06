# Import os and sys to link test file to file in another directory
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then reference and import incidentcounter.py from the project0 folder
from project0 import incidentcounter

# Test fetchincidents() function
def test_fetchincidents(url = 'https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf'):
    incidents = incidentcounter.fetchincidents(url)
    assert len(incidents) > 0
    assert incidents[0][1] == "1/1/2023 0:06"
    assert incidents[0][2] == "2023-00000001"
    assert incidents[0][3] == "2000 ANN BRANDEN BLVD "
    assert incidents[0][4] == "Transfer/Interfacility"
    assert incidents[0][5] == " EMSSTAT"
    # Note: incidentcounter.py did collect the necessary data, however to assert exact results it will have a problem with spaces that happened to be read before or after a field
    print(f"All tests passed")
