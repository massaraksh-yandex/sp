from platform.commands.endpoint import Endpoint
from platform.statement.create import create
from platform.statement.rule import Rule, Data, Op
from platform.utils.utils import register_commands
from platform.params.params import Params
from src.utils import checkout


class Ch(Endpoint):
    def name(self):
        return 'ch'

    def _about(self):
        return '{path} - выбирает ветки в git-репозиториях'

    def _rules(self):
        return create('').extended().statement(
                '{path} [--all] имя_ветки - во всех репозиториях переключиться на имя_ветки',
                '{space}--all - показывать неудачные или бессмысленные попытки поменять ветку',
                result=self._checkout_single,
                rule=Rule().empty(Data.Delimiter)
                           .maybe_option('all')
                           .size(Data.Target, Op.eq(1)))\
            .product()

    def _checkout_single(self, p: Params):
        checkout(lambda d: p.targets[0].value, show_failed_or_pointless='all' in p.options)


commands = register_commands(Ch)
