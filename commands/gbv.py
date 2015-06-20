from os import getcwd
from git.exc import InvalidGitRepositoryError
from git import Repo
from platform.endpoint import Endpoint
from platform.utils import makeCommandDict
from platform.check import *
from platform.color import *
from src.project_info import BranchSelector
from src.utils import dirs


class RepoStatus(Enum):
    clear = 0,
    untracked = 1,
    cached = 1,
    diff = 2


class Gbv(Endpoint):
    def name(self):
        return 'gbv'

    def _help(self):
        return ['{path} - печатает информацию о состоянии git-репозиториев в подпапках',
                '{path} [--all] [имя_ветки]',
                '{space}ключ --all - печатает все директории, даже если они не репозиторий git',
                '{space}имя_ветки - печатает информацию только о репозиториях, в которых текущая ветка == имя_ветки']

    def _rules(self):
        withBranch = lambda p: self.printReposWithBranch if Size.equals(p.targets, 1) and \
                                                            Check.optionNamesInSet(p, 'all') and \
                                                            Empty.delimers(p) \
                                                         else raiseWrongParsing()

        allRepos = lambda p: self.printRepos if Empty.targets(p) and \
                                                Check.optionNamesInSet(p, 'all') and \
                                                Empty.delimers(p) \
                                             else raiseWrongParsing()
        return [withBranch, allRepos]

    def repoStatusString(self, repo: Repo):
        if len(repo.index.diff(None)):
            return RepoStatus.diff
        elif len(repo.index.diff(None, cached=True)):
            return RepoStatus.cached
        elif len(repo.untracked_files):
            return RepoStatus.untracked
        else:
            return RepoStatus.clear

    def printFolderInfo(self, name, status: RepoStatus, branch):
        st = '*'
        if status == RepoStatus.diff:
            st = colored(st, Color.red, Style.bold)
        elif status == RepoStatus.clear:
            st = colored(st, Color.green, Style.bold)
        else:
            st = colored(st, Color.yellow, Style.bold)

        db = self._defaultBranches[name]
        if db != branch and db != '':
            branch = colored(branch, Color.violent, Style.bold)

        print('{0:40} | {1} | {2}'.format(colored(name, Color.blue, Style.bold),
                                          st, branch))

    def _printRepos(self, params: Params, printWithBranch = None):
        printAll = 'all' in params.options
        self._defaultBranches = BranchSelector(getcwd(), 'master')

        for d in dirs(getcwd()):
            try:
                r = Repo(d)
                if not printWithBranch or r.active_branch.name == printWithBranch:
                    self.printFolderInfo(d, self.repoStatusString(r), r.active_branch.name)
            except InvalidGitRepositoryError:
                if printAll and not printWithBranch:
                    self.printFolderInfo(d, RepoStatus.diff, '<not a git repo>')

    def printReposWithBranch(self, p: Params):
        self._printRepos(p, p.targets[0])

    def printRepos(self, p: Params):
        self._printRepos(p)

module_commands = makeCommandDict(Gbv)
