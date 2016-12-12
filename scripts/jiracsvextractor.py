# Parses a JIRA CSV dump and extract all the JIRA issues IDs (keys)
# Assumes key is the 2nd column

import csv

class CsvJiraKeysExtractor(object):
    def __init__(self, csvFilename):
        self.csvFilename = csvFilename

    def extract(self):
        with open(self.csvFilename, 'rb') as csvFile:
            return map(lambda row: row['Issue key'], csv.DictReader(csvFile))
