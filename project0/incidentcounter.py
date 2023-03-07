# Authored by: cggdonner (Catherine Donner)
# Functions to be used for main.py

# Packages
import urllib
import urllib.request
import tempfile
import PyPDF2  # be sure to pipenv install pypdf2
from PyPDF2 import PdfReader
import re

# Read and extract incident data
def fetchincidents(url):
    # Condition to accept only urls containing incident summaries
    if re.search(r"incident", url):
        headers = {}
        headers[
            "User-Agent"
        ] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        # Download and read incident data
        incident_data = urllib.request.urlopen(
            urllib.request.Request(url, headers=headers)
        ).read()
    else:
        print(
            f"URL not valid because does it not contain incidents"
        )  # Otherwise reject any url that does not contain incidents

    # Create temporary file to store incident data in
    fp = tempfile.TemporaryFile()

    # Write pdf data to temporary file
    fp.write(incident_data)

    # Set cursor of file back to beginning
    fp.seek(0)

    # Read pdf file using PyPDF2 PdfReader
    pdfReader = PdfReader(fp)

    # Get number of pages in pdf
    pagecount = len(pdfReader.pages)
    #print("Number of pages: ", pagecount)  # Print statement to verify number of pages

    # Store incident data in a list object
    incidents = []

    # Loop through number of pages and extract text
    for pagenum in range(0, pagecount):
        p = (
            pdfReader.pages[pagenum].extract_text().split("\n")
        )  # Split each line based on the newline character

        for i in range(
            len(p)
        ):  # Then include a nested for loop for each incident line on each page

            # Condition to ignore unwanted headers
            if (
                "Daily Incident Summary (Public)" in p[i]
                or "Date / Time Incident Number Location Nature Incident ORI" in p[i]
                or "NORMAN POLICE DEPARTMENT" in p[i]
            ):
                continue

            # Regex pattern to break each line (p[i]) into date_time, number, location, nature, and origin
            # (\d{1,2}\/\d{1,2}\/\d{4}\s\d{1,2}:\d{2}) to recognize date and time using 1 or 2 digits for month and day, then 4 digits for year, then 1 or 2 digits for hour and 2 digits for minute
            # \s(\d{4}-\d{8}) to recognize incident number using 4 digits followed by a hyphen, then followed by 8 digits
            # Then split based on listed incident natures and then by incident origin
            regex_pattern = r"(\d{1,2}\/\d{1,2}\/\d{4}\s\d{1,2}:\d{2})\s(\d{4}-\d{8})\s(.*?)(Chest Pain|Assault EMS Needed|Stroke|Supplement Report|Drug Violation|COP Relationships|Item Assignment|Animal Injured|Hit and Run|Animal Trapped|Traumatic Injury|Reckless Driving|Fireworks|Open Door\/Premises Check|Shots Heard|Mutual Aid|Loud Party|Contact a Subject|Public Assist|Check Area|Follow Up|Convulsion\/Seizure|Medical Call Pd Requested|Alarm|Hemorrhage\/Lacerations|Barking Dog|Harrassment \/ Threats Report|Unconscious\/Fainting|Sick Person|MVA With Injuries|MVA Non Injury|Debris in Roadway|Unknown Problem\/Man Down|Officer Needed Nature Unk|Parking Problem|Motorist Assist|Breathing Problems|Civil Standby|Heart Problems\/AICD|Vandalism|Animal Livestock|Diabetic Problems|Animal Bite|Found Item|Animal Dead|Falls|Cardiac Respritory Arrest|Runaway or Lost Child|Foot Patrol|Warrant Service|Traffic Stop|911 Call Nature Unknown|Welfare Check|Suspicious|Disturbance\/Domestic|Assist Officer|Information|Miscellaneous|Burglary Alarm|Robbery Alarm|Fire|911 Hang Up|Vehicle Lockout|Animal Call|Noise Disturbance|Citizen Assist|Transport|Domestic\/Familial|Narcotics|Hazardous Condition|Missing Person|Business Check|Lost Property|Threats|Property|Public Intoxication|Trespassing|Drunk Driver|Assault|Suicide|Assist Citizen|Hit & Run|Stolen Vehicle|Fight|Assault w/ Deadly Weapon|Indecent Exposure|Forgery\/Counterfeit|Sex Offense|Child Abuse\/Neglect|Embezzlement|Fraud|Forgery|Identity Theft|Auto Theft|Civil Matter|Criminal Mischief|Violation Of Court Order|Weapons Offense|Probation\/Parole|Arson|Kidnapping\/Abduction|Homicide|Sexual Assault|Burglary|Breaking & Entering|Larceny|Robbery|Transfer\/Interfacility|EMSSTAT|OK0140200|14005|14009)"
            components = re.split(
                regex_pattern, p[i]
            )  # Split each p[i] into the specified fields
            #print(components) # Print statement to verfify fields
            
            # Note: this block of code attempts to fix improperly formatted lines in incidents that are split due to multiple lines in address field
            # However, it does not work, I also tried regex formatting and it did not work as well.
            # Add an if condition to format lines that are improperly formatted due to multiple lines in address field
            #prev_line = "" # Initialize tracking previous line
            
            #for components in p:
            #    if(components.startswith(('RD', 'HWY', 'BLVD'))):
            #        incident = components + prev_line
            #        incidents.append(re.split(regex_pattern, incident.strip()))
            #    else: prev_line = components
            
            incidents.append(
                components
            )  # Add each p[i] incident to the incidents list object 

    return incidents
    #print(incidents) #Print statement to verify population of incidents
    fp.close()  # Close the temporary file


# Note: this regex pattern still creates an empty field '' before creating the date_time field. Also the location with multiple lines has not been accounted for, thereby some lines in incidents are still improperly formatted.

# Create database
import sqlite3


def createdb():
    # Connect to the database normanpd.db
    conn = sqlite3.connect("normanpd.db")

    # Cursor
    cursor = conn.cursor()

    # SQL command to drop table so it can be recreated with the empty column
    # This can also be a good measure to recreate the table containing different incident reports every time the main.py file is run
    cursor.execute("""DROP TABLE incidents;""")

    # SQL command to create table
    sql = """CREATE TABLE IF NOT EXISTS incidents (
        empty TEXT,
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    );"""  # had to add empty field to accomodate the additional '' field before date_time

    # Execute SQL command
    cursor.execute(sql)
    conn.commit()  # Commit changes to database

    # Close connection
    conn.close()


# Insert Data
def populatedb(incidents):
    # Takes rows created from fetchincidents() function and puts them into normanpd.db
    # This condition adds any empty fields if the length of each incident[i] is less than 6; this makes it easier to insert the incidents data without having binding errors in the case that 1 or more incidents[i] happened to have less than 6 fields
    for i in range(len(incidents)):
        while len(incidents[i]) < 6:
            incidents[i].append("")

    # Connect to database again
    conn = sqlite3.connect("normanpd.db")

    # Cursor
    cursor = conn.cursor()

    # SQL command to insert the data into every row in incidents
    cursor.executemany(
        """INSERT INTO incidents (empty, incident_time, incident_number, incident_location, nature, incident_ori) VALUES (?, ?, ?, ?, ?, ?)""",
        incidents,
    )
    conn.commit()

    # Print rows of incidents table using python function fetchall()
    cursor.execute("""SELECT * FROM incidents""")

    # This to verify that rows have been inserted into the table
    #rows = cursor.fetchall()
    #for row in rows:
    #    print(row)

    # Close connection
    conn.close()


# Print Status
def status():
    # Prints out list of incidents as directed:
    # Type of incident (alphabetically) | Total number of incidents of that type
    # Example: Noise Complaint | 4

    # Connect to the database again
    conn = sqlite3.connect("normanpd.db")

    # Cursor
    cursor = conn.cursor()

    # SQL query to select counts of each type of incident while also ordering by alphabetically
    sql_q = (
        """SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature ASC"""
    )
    cursor.execute(sql_q)
    incident_counts = (
        cursor.fetchall()
    )  # Fetchall retrieves the selected rows from the query

    # Print each nature with its count
    for row in incident_counts:
        nature, count = row
        print(f"{nature} | {count}")

    conn.commit()

    # Close connection
    conn.close()


# End of incidentcounter.py
