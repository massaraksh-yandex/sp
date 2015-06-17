from platform.check import emptyCommand
from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.project_info import defaultBranch
from src.utils import checkout


class Reset(Endpoint):
    def name(self):
        return 'reset'

    def _help(self):
        return ['{path} - выбирает в git-репозиториях ветки по-умолчанию',
                '{path}']

    def _rules(self):
        return emptyCommand(self._reset)

    def _reset(self, p: Params):
        answer = input('Выбрать для всех репозиториев ветки по-умолчанию? [yes/no] ')
        if answer == 'yes':
            checkout(lambda cwd, dir: defaultBranch(cwd, dir) or 'master')
        else:
            print('Отмена...')


module_commands = makeCommandDict(Reset)