from platform.commands.endpoint import Endpoint
from platform.utils.utils import register_commands
from platform.statement.rule import Rule, Data, Op
from platform.statement.create import create
from platform.color.color import Color, Style, colored
from src.branch_repo import BranchRepo
from src.repo import Repo
from src.utils import dirs
from platform.params.params import Params


class Gbv(Endpoint):
    def name(self):
        return 'gbv'

    def _about(self):
        return '{path} - печатает информацию о состоянии git-репозиториев в подпапках'

    def _rules(self):
        return create('').extended()\
            .statement('{path} [--all] - печатает информацию о состоянии git-репозиториев',
                       '{space}--all - печатает все директории, даже если они не репозиторий git',
                       result=self.printall,
                       rule=Rule().empty(Data.Delimiter)
                                  .empty(Data.Target)
                                  .maybe_option('all'))\
            .statement('{path} имя_ветки - печатает информацию о состоянии git-репозиториев',
                       '{space}показываются репозитории, в которых текущая ветка == имя_ветки',
                       result=self.printwithbranch,
                       rule=Rule().empty(Data.Delimiter)
                                  .size(Data.Target, Op.eq(1))
                                  .maybe_option('all'))\
            .product()

    def printwithbranch(self, p: Params):
        self._printRepos(p, p.targets[0].value)

    def printall(self, p: Params):
        self._printRepos(p)

    def _folder(self, repo: Repo):
        status = colored('*', Color.green, Style.bold)
        if repo.dirty:
            status = colored('*', Color.red, Style.bold)

        if repo.untracked or repo.cached:
            status = status+' '+colored('*', Color.yellow, Style.bold)
        else:
            status = ' '+status+' '

        branch = repo.branch
        if self._branchnames[repo.name] != branch:
            branch = colored(branch, Color.violent, Style.bold)

        return '{name:40} | {status} | {branch}' \
            .format(name=colored(repo.name, Color.blue, Style.bold),
                    status=status,
                    branch=branch)

    def _printRepos(self, p: Params, preferred=None):
        printAll = 'all' in p.options
        self._branchnames = BranchRepo()

        for path in dirs(show_hidden=printAll):
            repo = Repo(path)

            if preferred:
                if repo.branch == preferred:
                    print(self._folder(repo))
            else:
                if repo.valid or printAll:
                    print(self._folder(repo))


commands = register_commands(Gbv)
