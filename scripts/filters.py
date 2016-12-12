import datetime
import re

from datetime import datetime


class GitCommitDateRangeFilter(object):
    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate

    def filter(self, gitCommit):
        commitTime = datetime.fromtimestamp(gitCommit.commit_time)
        accepted = commitTime >= self.startDate and commitTime < self.endDate
        # print "Filtering commit on date: hash=", gitCommit.hex, "commitTime=", commitTime, "accepted", accepted
        return accepted


class GitCommitJiraFilter(object):
    def __init__(self, jiraIssueKeys):
        self.jiraIssueKeys = jiraIssueKeys
        # print "Filtering based on",len(jiraTickets), "JIRA tickets:\n",jiraTickets

    def filter(self, gitCommit):
        accepted = False
        for jiraIssueKey in self.jiraIssueKeys:
            if gitCommit.message.upper().find(jiraIssueKey) >= 0:
                accepted = True
                break

        # print "Filtering commit: accepted =", accepted, "hash =", gitCommit.hex, "author =", gitCommit.author.name
        # print gitCommit.message
        return accepted


class JavaFileFilter(object):
    def filter(self, gitFileStat):
        # Accepts only java files that aren't test files
        return re.search("(?<!Test)\.java$", gitFileStat.path) and re.search("(?<!IT)\.java$", gitFileStat.path)
