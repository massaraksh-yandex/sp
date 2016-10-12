from platform.commands.endpoint import Endpoint
from platform.statement.rule import Rule, Data, Op
from platform.statement.create import create
from platform.params.params import Params
from platform.color.color import Color, colored
from src.utils import dirs, get_project_name
from src.branch_repo import BranchRepo
from src.repo import Repo
from platform.utils.utils import register_commands
import os


class PushToGerrit(Endpoint):
    def name(self):
        return 'push'

    def _about(self):
        return '{path} - посылает текущую ветку в gerrit-топик'

    def _rules(self):
        return create('').extended()\
            .statement('{path} [--branch=имя_топика] ветка - пушит в геррит проекты с указанной веткой',
                       result=self._push,
                       rule=Rule().empty(Data.Delimiter)
                                  .size(Data.Target, Op.eq(1))
                                  .maybe_option('branch', ''))\
            .statement('{path} [--branch=имя_топика] - пушит текущий проект в геррит',
                       result=self._push_project,
                       rule=Rule().empty(Data.Delimiter)
                                  .empty(Data.Target)
                                  .maybe_option('branch', ''))\
            .info('{space}--branch=имя_топика - название топика в геррите\n' +
                  '{space}по умолчанию пушится в топик с названием ветки')\
            .product()

    def _call_push(self, repo, name, topic, default_branch):
        print('Проект: {0}\t'.format(colored(name, Color.green)), end='')
        try:
            result = repo.gerpush(topic, default_branch)
        except Exception as e:
            result = str(e)
            print('[' + colored('FAILED', Color.red) + ']')
        else:
            print('[  ' + colored('OK', Color.green) + '  ]')
        print(result)

    def _push_project(self, p: Params):
        project_traits = BranchRepo()

        if project_traits.levels_to_project_traits > 1:
            name = get_project_name(project_traits.ws)
            repo = Repo(os.path.join(project_traits.ws, 'src', name))
            topic = p.options['branch'] or repo.branch

            self._call_push(repo, name, topic, project_traits[name])

    def _push(self, p: Params):
        branch = p.targets[0].value
        topic = p.options['branch'] or branch
        bs = BranchRepo()

        for d in dirs():
            r = Repo(d)

            if r.branch != branch:
                continue

            self._call_push(r, d, topic, bs[d])


commands = register_commands(PushToGerrit)
