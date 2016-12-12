import pygit2
import datetime
import sys
import argparse

from pygit2 import Repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_TIME, GIT_SORT_REVERSE
from datetime import datetime
from progress import printProgress

from gitfilestat import GitFileStat
from filters import GitCommitDateRangeFilter, GitCommitJiraFilter, JavaFileFilter
from jiracsvextractor import CsvJiraKeysExtractor

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--git-repo", help="Git repo base directory")
    parser.add_argument("-s", "--start-date", help="YYYY-MM-DD format, default to 2016-07-01")
    parser.add_argument("-e", "--end-date", help="YYYY-MM-DD format, default to 2016-10-01")
    parser.add_argument("-j", "--jira-issues", help="CSV file containing JIRA tickets to correlate commits with (optional)")

    args = parser.parse_args()
    if not args.git_repo:
        raise ValueError("git-repo mandatory")
    if not args.start_date:
        args.start_date = "2016-07-01"
    if not args.end_date:
        args.end_date = "2016-10-01"
    return args

args = parse_args()
repo = Repository(args.git_repo)
startDate = datetime.strptime(args.start_date, "%Y-%m-%d")
endDate = datetime.strptime(args.end_date, "%Y-%m-%d")
jiraIssuesCsvFilename = args.jira_issues

print "Analyzing repo", repo, "for commits between", startDate, "and", endDate
commits = [commit for commit in repo.walk(repo[repo.head.target].id, GIT_SORT_TOPOLOGICAL | GIT_SORT_TIME | GIT_SORT_REVERSE)]
print "Initial nb of commits: ", len(commits)
commits = filter(GitCommitDateRangeFilter(startDate, endDate).filter, commits)
print "Commits matching date range: ", len(commits)
if jiraIssuesCsvFilename:
    jiraKeysExtractor = CsvJiraKeysExtractor(jiraIssuesCsvFilename)
    commits = filter(GitCommitJiraFilter(jiraKeysExtractor.extract()).filter, commits)
    print "Commits matching JIRA tickets: ", len(commits)
else:
    print "No filtering based on JIRA tickets"

# print "Retained commits:"
# for commit in commits:
#    print "hash=", commit.hex, "author=", commit.author.name, "message=", commit.message

print "Analyzing", len(commits), "commits from", startDate, "to", endDate
fileStats = {}
printProgress(0, len(commits))
for i, commit in enumerate(commits):
    GitFileStat.addCommit(repo, commit, fileStats)
    printProgress(i+1, len(commits))

print "Result:"
for fileStat in sorted(filter(JavaFileFilter().filter, fileStats.values()), key=GitFileStat.commitsCount, reverse=True):
    print fileStat
