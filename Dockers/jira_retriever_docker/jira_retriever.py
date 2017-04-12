from jira import JIRA
import re
import csv
import sys
import os

PROJECT_KEY="AMQP"

options = {'server': 'https://jira.spring.io'}

PATH = 'csv_data/'

if(len(sys.argv) > 1):
	PROJECT_KEY=sys.argv[1]

if(len(sys.argv) > 2):
    options['server'] = sys.argv[2]

if(len(sys.argv) > 3):
	PATH=sys.argv[3]

jira = JIRA(options)

if not os.path.exists(PATH):
	os.makedirs(PATH)

# Get project
project = jira.project(PROJECT_KEY)

# Get components and version
print "Get versions..."
components = jira.project_components(project)
versions = jira.project_versions(project)

with open(PATH+'jira_versions.csv', 'wb') as csvfile:
    fieldnames = ["name", "release_date", "released"]
    writer = csv.DictWriter(csvfile,
        fieldnames=fieldnames)
    writer.writeheader()

    for version in versions:
        if(hasattr(version, 'releaseDate')):
            writer.writerow({ \
                "name" : version.name, \
                "release_date" : version.releaseDate, \
                "released" : int(version.released)
            })

# Get issues
print "Get issues..."
issues = jira.search_issues("project="+PROJECT_KEY,maxResults=50000)

# Write in csv
with open(PATH+'jira_issues_bugs.csv', 'wb') as csvfile:
    fieldnames = ["date", "summary"]
    writer = csv.DictWriter(csvfile,
        fieldnames=fieldnames)
    writer.writeheader()

    for issue in issues:
        # write only bugs
        if(issue.fields.issuetype.name == "Bug"):
            writer.writerow({ \
                "date" : issue.fields.created.replace(".000+0000", "Z"), \
                "summary" : issue.fields.summary
            })
# Open a file
fo = open(PATH+"jira_retriever.txt", "wb")

# Close opend file
fo.close()
