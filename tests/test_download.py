# Test functions

import incidentcounter

def test_fetchincidents(filename = 'docs/____'):
    file = incidentcounter.fetchincidents(filename)
    assert len(file) = ____

def test_extractincidents(filename = 'docs/___'):
    file = incidentcounter.fetchincidents(filename)
    incidents = incidentcounter.extractincidents(file)
    assert ___

def test_createdb(filename = )

def test_populatedb(filename = )

def test_status(filename = 'docs/__', term = 'Nausea'):
    file = incidentcounter.fetchincidents(filename)
    incidents = incidentcounter.extractincidents(file)
    count = incidentcounter.status(incidents)

    assert count == ___
