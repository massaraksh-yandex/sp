from platform.color.color import colored, Color
from platform.commands.endpoint import Endpoint
from platform.utils.utils import registerCommands
from platform.params.params import Params
from platform.statement.statement import singleOptionCommand
from src.branch_repo import BranchRepo
from src.repo import Repo
from src.utils import dirs


class Rebase(Endpoint):
    def name(self):
        return 'rebase'

    def _info(self):
        return [ '{path} - ребейзит ветки в репозиториях' ]

    def _rules(self):
        return singleOptionCommand(
            ['{path} имя_ветки - во всех репозиториях с текущей веткой имя_ветки ребейзит её на основную'],
            self._rebase)

    def _rebase(self, p: Params):
        db = BranchRepo()
        for path in dirs():
            print(colored(path, Color.green))
            try:
                repo = Repo(path)
                print(repo.rebase(db[path]))
            except:
                pass




commands = registerCommands(Rebase)