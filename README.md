# cs5293sp23-project0
Author: cggdonner (Catherine Donner)
Repo used for Project 0 in CS 5293 Text Analytics Spring 2023

### Project Description
This project is designed to read in information from an incident report from the Norman Police Department website and to return a status report based on how many times each incident nature is mentioned in the incident report. Each incident report is a pdf, and there are other types of reports included on the Norman Police Department website, therefore the main.py file that is executed in the terminal is expected to meet the following criteria:
1. Ignore reading arrest summaries and case summaries.
2. Ignore reading in headers including "NORMAN POLICE DEPARTMENT", "Daily Incident Summary (Public)", and the table headers "Date/Time Incident Number Location Nature Incident ORI".
3. Each incident must include the fields incident_time, incident_number, incident_location, nature, and incident_ori based on specified text formatting.
4. For fields with multiple lines (i.e. location), merge that line with the same field.
5. Load the extracted data from the incident report pdf into an sqlite database with the fields mentioned in 3.
6. Return a status report in the format "Nature | Count".

### How to install
You can install my Project 0 using the command:
git clone https://github.com/cggdonner/cs5293sp23-project0.git
You will have to sign into the repo as a collaborator using your credentials.
After signing in, use the command cd cs5293sp23-project0/ to access the repo.
To view all directories and files in the repo, use the command tree .

### How to run
In the terminal, you can use the following command to run the main.py file:
pipenv run python project0/main.py --incidents <url>
where <url> = https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf or another related url
To run test files in the directory tests, you can use the command:
pipenv run python -m pytest

### Functions
###### incidentcounter.py (Please see for more detailed comments)
fetchincidents() - This function takes the parameter url, which can either be the incident summary url, the arrest summary url, or the case summary url; however, this method should only accept reading in incident summary urls. After accepting the incident report url, it then reads in the data from the pdf and stores the incidents in a list object called incidents. After further text formatting using regex splitting and ignoring headers, the incident data in the incidents object is returned by fetchincidents(). This method also contains a print statement to show how many pages are in the pdf.
createdb() - This function takes no arguments. This function connects to the database normanpd.db and creates a table called incidents storing the fields incident_time, incident_number, incident_location, nature, and incident_ori. Nothing is returned from this function.
populatedb() - This function takes the argument incidents, which is the incident data that is returned from fetchincidents(). This function, using an SQL query, connects to the normanpd.db database again and inserts the incident data into the database. The incidents table is returned, in SQL format, from this method.
status() - This function takes no parameters. This uses an SQL query to select all the nature types and to group them by count, as well as to list them alphabetically. This method also uses the fetchall() function in Python to return all the incident natures and their counts from the SQL query.
Note: In main.py, there is an additional --incidents argument in which using the argparse package, the url is the primary input in the terminal command to run the main.py program.

### Database Development
For setting up the database, I used very simple sqlite3 commands to connect to the normanpd.db; from my job at DISC, I have connected to Postgres databases before that required credentials to connect, however since normanpd.db was a locally listed database, there was no need for complex credentials and it was very easy to connect to and set up. The normanpd.db database is listed as one of the files in this project. I had considered adding an additional argparse argument --db set to the default value of "normanpd.db", however there was no need for including "normanpd.db" as an argument in any of the functions createdb(), populatedb(), and status() because it would always be listed as the database connection when executing the SQL queries for each of these functions. I also used the DROP TABLE incidents; query in createdb() to accomodate for when the terminal command would be run every time (and likely with a different url input), the table would be recreated containing different data.

### Tests
I created test files for each function in main.py; all are listed under the tests directory. For test_fetch.py, I focused on asserting that at least one incident was extracted and loaded into the incidents list object in fetchincidents(). I also made sure that the fields of the first incident that was inserted into the incidents object were equivalent to what was read in by the fetchincidents() function. For test_create.py, if createdb() was executed, that meant that the normanpd.db database had been created and that the incidents table had been created inside that database as well, therefore this was an easy function to test. In test_populate.py, I asserted that the fields in the incidents table in the database were equivalent to the fields in the incident data extracted from the fetchincidents() function. Likewise, I also did a test to make sure that the term "Drunk Driver" had been inserted into the database table, and to make sure that the expected count of records containing the nature "Drunk Driver" was asserted as well. Finally, for test_status.py, the primary assertion that I focused on was making sure that the nature "Fireworks" appeared 5 times in the input incident summary. As in, the output "Fireworks | 5" was included in the output from the status() function. In conclusion, all of these tests passed. In addition, besides testing the functions in main.py using pytest, I also created a list of urls in a file called TEST_FILES in the docs directory. I used the urls in that file to make sure that my main.py rejected any arrest or case summaries, as well as produced a good output for other incident summaries.

### Bugs and Assumptions
Because of the regex pattern, there is an empty '' field that appears before the incident_time field, so there are technically 6 fields in each incident in the incidents object in fetchincidents(). Unfortunately, I was not able to merge location information to the same incident in which the location contained multiple lines in the pdf, therefore it is to be assumed that there are some lines that are improperly formatted. There is a block of code in incidentcounter.py where I attempted to account for this case using an if statement (I also tried regex formatting), however the methods that I attempted did not do anything to fix the fields with multiple lines of information. There is also the final incident which contains the date and time that the incident report was written (at the end of every pdf file), another improper formatting. To take into account those lines that contained less than 6 fields, I appended empty '' fields to these lists so that they would still be added to the incidents table using populatedb() without running into binding errors. In the test_fetch.py, the test fields that I had asserted were correctly extracted by the fetchincidents() function, however in order for the test to pass, the fields also have to include any spaces that were read in before or after the field, otherwise the test will not pass. There are also other tests that I could have used to solidify my program's effectiveness, however since the fields with multiple lines were not accounted for, some proposed tests would likely fail due to those flaws in the code. Finally, a bug to note is when running any arrest or case summary urls in the terminal, it will print out the statement that I made in fetchincidents() saying that "URL is not valid because it does not contain incidents", however after that output there will be an error output as well.

