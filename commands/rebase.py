from platform.color.color import colored, Color
from platform.commands.endpoint import Endpoint
from platform.utils.utils import register_commands
from platform.params.params import Params
from platform.statement.create import create
from src.branch_repo import BranchRepo
from src.repo import Repo
from src.utils import dirs


class Rebase(Endpoint):
    def name(self):
        return 'rebase'

    def _about(self):
        return '{path} - ребейзит ветки в репозиториях'

    def _rules(self):
        return create('{path} имя_ветки - во всех репозиториях с текущей веткой имя_ветки ребейзит её на основную')\
            .single_option_command(self._rebase)

    def _rebase(self, p: Params):
        db = BranchRepo()
        for path in dirs():
            print(colored(path, Color.green))
            try:
                repo = Repo(path)
                print(repo.rebase(db[path]))
            except:
                pass


commands = register_commands(Rebase)
