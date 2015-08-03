from platform.commands.endpoint import Endpoint
from platform.utils.utils import registerCommands
from platform.params.params import Params
from platform.statement.statement import Statement, Rule
from src.utils import checkout


class Ch(Endpoint):
    def name(self):
        return 'ch'

    def _info(self):
        return [ '{path} - выбирает ветки в git-репозиториях' ]

    def _rules(self):
        return [ Statement(['{path} [--all] имя_ветки - во всех репозиториях переключиться на имя_ветки',
                            '{space}--all - показывать неудачные или бессмысленные попытки поменять ветку'],
                           self._checkoutSingle,
                           lambda p: Rule(p).empty().delimers()
                                            .check().optionNamesInSet('all')
                                            .size().equals(p.targets, 1)) ]

    def _checkoutSingle(self, p: Params):
        checkout(lambda dir: p.targets[0].value, failed_or_pointless='all' in p.options)


commands = registerCommands(Ch)
