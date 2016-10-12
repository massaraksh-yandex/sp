from platform.statement.rule import Rule, Data
from platform.statement.create import create
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import register_commands, read_line_with_prompt
from src.branch_repo import BranchRepo
from src.utils import checkout


class Reset(Endpoint):
    def name(self):
        return 'reset'

    def _about(self):
        return '{path} - выбирает в git-репозиториях ветки по-умолчанию'

    def _rules(self):
        return create('').extended()\
            .statement('{path} [--all]- данные берутся из файла project_traits.py',
                       '{space}если файла нет, то выбирается ветка master',
                       '{space}--all - показывать неудачные или бессмысленные попытки поменять ветку',
                       result=self._reset,
                       rule=Rule().empty(Data.Delimiter)
                                  .empty(Data.Target)
                                  .maybe_option('all'))\
            .product()

    def _reset(self, p: Params):
        ans = read_line_with_prompt('Выбрать для всех репозиториев ветки по-умолчанию? [yes/no]', 'yes')

        if ans == 'yes':
            db = BranchRepo()
            checkout(lambda d: db[d], show_failed_or_pointless='all' in p.options)
        else:
            print('Отмена...')


commands = register_commands(Reset)
