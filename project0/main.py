# Authored by: cggdonner (Catherine Donner)
# CS 5293 Project 0

# Packages
import argparse  # Imports argument parser package

import incidentcounter  # Imports functions from incidentcounter.py


def main(url):
    # Download and extract data given the url of the incident report (or arrest report, etc. even though this should only accept incident reports)
    incident_data = incidentcounter.fetchincidents(url)

    # Create sqlite database table to store the extracted data
    db = incidentcounter.createdb()

    # Insert data into the table given the incident data retrieved from fetchincidents()
    incidentcounter.populatedb(incident_data)

    # Print incident natures (alphabetically) with their counts
    incidentcounter.status()


# Use argument parser package to add incidents argument which corresponds to the input url
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--incidents", type=str, required=True, help="Incident summary url."
    )

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)  # Parses parameters to pass through code

# **TO RUN IN COMMAND LINE: pipenv run python project0/main.py --incidents <url>

# End of main.py
