import datetime

from datetime import datetime

class GitFileStat(object):

    def __init__(self, path):
        self.path = path
        self.commitHashes = []
        self.patches = []
        self.commiters = set()

    def __str__(self):
        return self.path + ", " + str(self.commitsCount()) + ", " + str(self.linesChanged()) + ", " + str(self.linesAdded()) + ", " + str(self.linesRemoved()) + ", " + str(self.commitersCount())

    def commitsCount(self):
        return len(self.commitHashes)

    def linesAdded(self):
        return reduce(lambda x,y: x + y.line_stats[1], self.patches, 0)

    def linesRemoved(self):
        return reduce(lambda x,y: x + y.line_stats[2], self.patches, 0)

    def linesChanged(self):
        return reduce(lambda x,y: x + y.line_stats[1] + y.line_stats[2], self.patches, 0)

    def commitersCount(self):
        return len(self.commiters)

    @staticmethod
    def fromCommits(repo, commits):
        fileStats = {}
        for commit in commits:
            addCommit(repo, commit, fileStats)

        return fileStats

    @staticmethod
    def addCommit(repo, commit, fileStats):
        commitTime = datetime.fromtimestamp(commit.commit_time)
        # print "Commit - hash =",commit.hex,"date =",commitTime,"author =",commit.author.name

        if not commit.parents:
            # print "No parent?"
            return

        diffs = repo.diff(commit.parents[0], commit)
        # print "\tStats - insertions =", diffs.stats.insertions, "deletions =", diffs.stats.deletions, "files_changed =", diffs.stats.files_changed

        for patch in diffs:
            # print "\tPath=",patch.delta.new_file.path,", Line stats: insertions=",patch.line_stats[1],"deletions=",patch.line_stats[2]

            fileStat = fileStats.get(patch.delta.new_file.path)
            if not fileStat:
                fileStat = GitFileStat(patch.delta.new_file.path)
                fileStats[ patch.delta.new_file.path ] = fileStat

            fileStat.commitHashes.append(commit.hex)
            fileStat.patches.append(patch)
            fileStat.commiters.add(commit.author.name)
