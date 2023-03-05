# cs5293sp23-project0
Author: cggdonner (Catherine Donner)
Repo used for Project 0 in CS 5293 Text Analytics Spring 2023

### Project Description
The objective of this project is to take an incident report from the Norman Police Department website and to return a status report based on how many times each incident nature is included in the incident report. Each incident report is a pdf, and there are other types of reports included on the Police Department Website, therefore the main.py file that is executed in the terminal must meet the following requirements:
1. Ignore reading arrest summaries and case summaries.
2. Ignore reading in headers including "NORMAN POLICE DEPARTMENT", "Daily Incident Summary (Public)", and the table headers "Date/Time Incident Number Location Nature Incident ORI".
3. Each incident must include the fields incident_time, incident_number, incident_location, nature, and incident_ori.
4. For fields with multiple lines (i.e. location), accomodate to include that in the same incident.
5. Load the extracted data from the incident report pdf into an sqlite database with the aforementioned fields.
6. Return a status report in the format "Breathing Problems | 19".

### How to install
?

### How to run
In the terminal, the main.py file is executed using the following command:
pipenv run python project0/main.py --incidents <url>
where <url> = https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf or another related url

### Functions
###### incidentcounter.py (Please see for more detailed comments)
fetchincidents() - This function takes the parameter url, which can either be the incident summary url, the arrest summary url, or the case summary url; however, this method should only accept incident summary urls. After accepting the incident report url, it then reads in the data from the pdf and stores the incidents in a list object called incidents. After further regex splitting and ignoring headers, the incidents object is returned by fetchincidents(). This method also contains a print statement to show how many pages are in the pdf.
createdb() - This function takes no arguments. This function connects to the database normanpd.db and creates a table called incidents storing the fields incident_time, incident_number, incident_location, nature, and incident_ori. Nothing is returned from this function.
populatedb() - This function takes the argument incidents, which is the incident data that is returned from fetchincidents(). This function, using an SQL query, connects to the normanpd.db database again and inserts the incident data into the database. The incidents table is returned, in SQL format, from this method.
status() - This function takes no parameters. This uses an SQL query to select all the nature types and to group them by count, as well as to list them alphabetically. This method also uses the fetchall() function in Python to return all the incident natures and their counts.
Note: in main.py, there is an additional --incidents argument in which using the argparse package, the url is the primary input in the terminal command to run the main.py program.

### Database Development
From my job at DISC, I have worked with connecting to Postgres databases and executing SQL queries using Python commands, so that experience has shown me how to create the normanpd database and to create tables for it. There was no use for including "normanpd.db" as an argument in any of the functions createdb(), populatedb(), and status() because it would always be listed as the database conneciton for each of these functions. I also used the DROP TABLE incidents; query to accomodate for when the command would be run in the terminal every time (and with a different url input), the table would be recreated containing different data.

### Bugs and Assumptions
Because of the regex pattern, there is an empty '' field that appears before the incident_time field, so there are technically 6 fields in each incident in the incidents object in fetchincidents(). In addition, I could not figure out how to add the location information to the same incident in which the location contained multiple lines in the pdf, therefore there are some lines that are improperly formatted. There is also the final incident which contains the date and time that the incident report was written. To take into account those lines that contained less than 6 fields, I appended empty '' fields to these lists so that they would still be added to the incidents table without running into binding errors. 

