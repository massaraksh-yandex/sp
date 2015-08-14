from platform.statement.statement import Statement, Rule
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import registerCommands, readLineWithPrompt
from src.branch_repo import BranchRepo
from src.utils import checkout


class Reset(Endpoint):
    def name(self):
        return 'reset'

    def _info(self):
        return ['{path} - выбирает в git-репозиториях ветки по-умолчанию']

    def _rules(self):
        return [ Statement(['{path} [--all]- данные берутся из файла project_traits.py',
                            '{space}если файла нет, то выбирается ветка master',
                            '{space}--all - показывать неудачные или бессмысленные попытки поменять ветку'],
                           self._reset,
                           lambda p: Rule(p).empty().delimers()
                                            .empty().targets()
                                            .check().optionNamesInSet('all')) ]

    def _reset(self, p: Params):
        ans = readLineWithPrompt('Выбрать для всех репозиториев ветки по-умолчанию? [yes/no]', 'yes')

        if ans == 'yes':
            db = BranchRepo()
            checkout(lambda dir: db[dir], failed_or_pointless='all' in p.options)
        else:
            print('Отмена...')


commands = registerCommands(Reset)