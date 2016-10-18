from execute.run import Run
from platform.commands.endpoint import Endpoint
from platform.utils.utils import register_commands
from platform.statement.create import create
from platform.color.color import Color, colored
from src.branch_repo import BranchRepo
from platform.params.params import Params


class Clean(Endpoint):
    def name(self):
        return 'clean'

    def _about(self):
        return '{path} - очищает репозиторий от артефактов сборки'

    def _rules(self):
        return create('cwd доджен быть WS/src/').empty_command(self._act)

    def _exec_cmd(self, cmd):
        print(colored('$ '+cmd, Color.green))
        for l in Run().cmd(cmd).exec():
            print(l, end='')

    def _act(self, p: Params):
        project_traits = BranchRepo()
        if not (1 <= project_traits.levels_to_project_traits < 3):
            return

        remove_this = [
            'CMakeFiles',
            'external',
            'CMakeCache.txt',
            'Makefile',
            'cmake_install.cmake',
            '*.a',
            '*.so'
        ]
        pattern = ' -o '.join(['-name "'+r+'"' for r in remove_this])

        self._exec_cmd('find . {0} | xargs rm -rf'.format(pattern))

        if project_traits.levels_to_project_traits == 1:
            self._exec_cmd('git submodule foreach "git checkout -- ."')
            self._exec_cmd('git submodule foreach "git submodule update -f"')

            cmd = 'rm -rf lib64 include'
            print(colored('$ ' + cmd, Color.green))
            for l in Run().path('..').cmd(cmd).exec():
                print(l, end='')


commands = register_commands(Clean)
