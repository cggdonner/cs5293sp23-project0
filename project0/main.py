# Catherine Donner
# Project 0

# Example main.py, this is not the final version. More or less steps needed
import argparse #imports argument parser package

import incidentcounter #imports functions from incidentcounter.py

def main(url, db):
    # Download data
    incident_data = incidentcounter.fetchincidents(url)

    # Extract data
    incidents = incidentcounter.extractincidents(incident_data)

    # Create new database
    db = incidentcounter.createdb(db)

    # Insert data
    incidentcounter.populatedb(incidents, db)

    # Print incident counts
    incidentcounter.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                         help="Incident summary url.") #adds incident argument

    parser.add_argument("--db", type=str, default="normanpd.db",
                         help="Database name.") #adds db argument

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents, args.db) #Parses parameters to pass through code

#**TO RUN IN COMMAND LINE: pipenv run python project0/main.py --incidents <url>
