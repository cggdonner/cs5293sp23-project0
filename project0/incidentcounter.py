# Functions to be used for main.py

# Download data
import urllib
import urllib.request
import tempfile

# Read incident data
def fetchincidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    return data

import PyPDF2 # be sure to pipenv install pypdf2
from PyPDF2 import PdfReader

# Extract data (all pages from pdf)
def extractincidents(incident_data):
    # Create temporary file
    fp = tempfile.TemporaryFile()

    # Write pdf data to temporary file
    fp.write(incident_data)

    # Set cursor of file back to beginning
    fp.seek(0)

    # Read PDF file
    pdfReader = PdfReader(fp)

    # Get number of pages
    pagecount = len(pdfReader.pages)

    #Store incident data in a list of tuples
    incidents = []

    #Loop through number of pages and extract text
    for pagenum in range(0, pagecount):
        p = pdfReader.pages[pagenum].extract_text().split("  ") #for loop to loop through each page and extract text
        for i in range(len(p)): #then nested for loop for each incident on each page
            if not p[i].startswith("20"): continue #clarify what starts an incident
            components = p[i].split(maxsplit=4) #maximum text split of 4
            incident = tuple(components) #store these fields in a tuple
            incidents.append(incident) #add each incident to the list of incidents
            
        return incidents

    # Alternatively
    #for pagenum in range(0, pagecount):
        # Get text from each page
    #    p = pdfReader.getPage(pagenum).extractText().split("  ")

        # Loop through each line in page and add each line to rows
        #for i in range(len(p)):
        #    print(p[i], end="\n")

        #print("Page " + pagenum) # To reference page number
# Any lines that need to be fixed/ignored? Multiple lines of information?

# Create database
import sqlite3

def createdb(db="normanpd.db"):
    # Connect to the database normanpd.db
    conn = sqlite3.connect(db)

    # Cursor
    cursor = conn.cursor()

    # SQL command to create table
    sql = """CREATE TABLE incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    );"""

    # Execute SQL  command using try/except clause
    try: 
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback() # Rollback in case of error

    # Close connection
    conn.close()

# Insert Data
def populatedb(incidents, db="normanpd.db"):
    # Takes rows created from extractincidents() function and puts them into normanpd.db
    # Connect to database again
    conn = sqlite3.connect(db)

    #Cursor
    cursor = conn.cursor()

    #SQL command to insert the data into every row in incidents
    for row in incidents:
        try: 
            cursor.execute("""INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)""", row)
            conn.commit()
        except:
            print(f"Error: {row} already exists in database.")
            conn.rollback()
    
    #Close connection
    conn.close()


# Print Status
def status(db="normanpd.db"):
    # Prints out list of incidents as directed:
    # Type of incident (alphabetically) | Total number of incidents of that type
    # Example: Noise Complaint | 4

    # Connect to the database again
    conn = sqlite3.connect(db)

    # Cursor
    cursor = conn.cursor()

    # SQL query to select counts of each type of incident
    sql_q = """SELECT nature, COUNT(*) FROM incidents GROUP BY nature"""
    rows = cursor.fetchall() # Fetchall retrieves the selected rows from the query
    for row in rows:
        nature, count = row
        print(f"{nature} | {count}")

    try:
        cursor.execute(sql_q)
        conn.commit()
    except:
        conn.rollback()

    #Close connection
    conn.close()
