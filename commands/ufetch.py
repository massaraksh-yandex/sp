from execute.run import Run
from platform.commands.endpoint import Endpoint
from platform.utils.utils import register_commands
from platform.statement.create import create
from platform.color.color import Color, colored
from src.branch_repo import BranchRepo
from platform.params.params import Params


class Ufetch(Endpoint):
    def name(self):
        return 'ufetch'

    def _about(self):
        return '{path} - обновляет воркспейс'

    def _rules(self):
        return create('cwd доджен быть WS/src/').empty_command(self._act)

    def _exec_cmd(self, cmd):
        print(colored('$ '+cmd, Color.green))
        for l in Run().cmd(cmd).exec():
            print(l, end='')

    def _act(self, p: Params):
        project_traits = BranchRepo()
        if project_traits.levels_to_project_traits != 1:
            return

        self._exec_cmd('git fetch --all -p')
        self._exec_cmd('git pull')
        self._exec_cmd('git submodule foreach "git fetch --all -p; git pull; git submodule update; true"')


commands = register_commands(Ufetch)
