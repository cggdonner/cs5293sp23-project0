# Test status() function

import incidentcounter

def test_status(url = 'https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf', term = 'Fireworks'):
    incidents = incidentcounter.fetchincidents(url)
    incidentcounter.createdb()
    incidentcounter.populatedb(incidents)
    incidentcounter.status()
    assert "{term} | {count}" == "Fireworks | 5"
    print(f"{term} passed test!")
