# Test populatedb() function

import incidentcounter

def test_populatedb(url = 'https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf', term = 'Drunk Driver'):
    incidents = incidentcounter.fetchincidents(url)
    incidentcounter.createdb()
    db_populated = incidentcounter.populatedb(incidents)
    assert term in db_populated
    print(f"{term} passed test!")
