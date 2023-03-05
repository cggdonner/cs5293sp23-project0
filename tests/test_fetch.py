# Test fetchincidents() function

import incidentcounter

def test_fetchincidents(url = 'https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf')
    incidents = incidentcounter.fetchincidents(url)
    assert incidents[0][0] == "1/1/2023 00:06"
    assert incidents[0][1] == "2023-00000001"
    assert incidents[0][2] == "2000 ANN BRANDEN BLVD"
    assert incidents[0][4] == "Transfer/Interfacility"
    assert incidents[0][5] == "EMSSTAT"
    print(f"All tests passed")
