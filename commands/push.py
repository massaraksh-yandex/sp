from platform.commands.endpoint import Endpoint
from platform.statement.statement import Statement, Rule
from platform.params.params import Params
from platform.color.color import Color, colored
from src.utils import dirs
from src.branch_repo import BranchRepo
from src.repo import Repo
from os import getcwd
from platform.utils.utils import registerCommands


class PushToGerrit(Endpoint):
    def name(self):
        return 'push'

    def _info(self):
        return ['{path} - посылает текущую ветку в gerrit-топик']

    def _rules(self):
        return [ Statement(['{path} [--branch=имя_топика] ветка - пушит в геррит проекты с указанной веткой',
                            '{space}--branch=имя_топика - название топика в геррите',
                            '{space}по умолчанию пушится в топик с названием ветки'], self._push,
                           lambda p: Rule(p).empty().delimers()
                                            .size().equals(p.targets, 1)
                                            .check().optionNamesInSet('branch'))
                 ]

    def _push(self, p: Params):
        branch = p.targets[0].value
        topic = p.options['branch'] or branch
        bs = BranchRepo()

        for d in dirs(getcwd()):
            r = Repo(d)

            if r.branch != branch:
                continue

            print('Проект: ' + colored(d, Color.green))
            try:
                print(r.gerpush(topic, bs[d]))
            except Exception as e:
                print(e)


commands = registerCommands(PushToGerrit)
