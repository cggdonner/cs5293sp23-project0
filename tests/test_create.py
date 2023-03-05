# Test createdb() function

import incidentcounter

def test_createdb():
    incidentcounter.createdb()
    print(f"Connected to database!")
