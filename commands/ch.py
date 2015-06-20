from platform.endpoint import Endpoint
from platform.utils import makeCommandDict
from platform.check import *
from src.utils import checkout


class Ch(Endpoint):
    def name(self):
        return 'ch'

    def _help(self):
        return ['{path} - выбирает ветки в git-репозиториях',
                '{path} название_топика']

    def _rules(self):
        return singleOptionCommand(self._checkoutSingle)

    def _checkoutSingle(self, p: Params):
        checkout(lambda dir: p.targets[0])


module_commands = makeCommandDict(Ch)
