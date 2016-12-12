# hotspot-detector
Some Python hacks to dig in Git repo and get some code metrics such as code frequently changed etc.

## System requirements
Python 2 with libgit2 and pygit2
Developed using Python 2.7.12.

## Usage
    python scripts/hotcodedetector.py --git-repo <path_to_git_repo_root_dir> --start-date 2016-07-01 --end-date 2016-10-01 --jira-issues <path_to_jira_csv_export>

start/end date is optional - will default to start and end of 2016-Q3 respectively if omitted.
jira-issues is optional - if not specified no commit screening based on JIRA issues will be performed.

## Output
After some progress report, the script outputs one CSV line per non-test Java source file (filter can be changed in filters.py).
Each line contains:
* Path to source file
* Number of commits this file has been part of
* Total number of changed lines (insertions + deletions)
* Number of inserted lines
* Number of deleted lines
* Number of distinct authors
