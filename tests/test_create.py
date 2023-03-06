# Import os and sys to link test file to file in another directory
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Then reference and import incidentcounter.py from the project0 folder
from project0 import incidentcounter

# Test createdb() function
def test_createdb():
    incidentcounter.createdb()
    print(f"Connected to database!")
