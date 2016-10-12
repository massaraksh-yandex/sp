from execute.run import Run
from platform.commands.endpoint import Endpoint
from platform.commands.command import Command
from platform.utils.utils import register_commands
from platform.statement.rule import Rule, Data, Op
from platform.statement.create import create
from platform.color.color import Color, colored
from src.branch_repo import BranchRepo
from src.utils import get_project_name
from platform.params.params import Params
from src.db import WorkspaceAndTasks


prepare_commit_msg = '''#!/bin/bash
sp task internal "$1"

'''


class Init(Endpoint):
    def name(self):
        return 'init'

    def _about(self):
        return '{path} - устанавливает в репозиторий в вокрспейсе для всех сабмодулей prepare-commit-msg'

    def _rules(self):
        return create('Устанавливает prepare-commit-msg').empty_command(self._act)

    def _act(self, p: Params):
        project_traits = BranchRepo()

        if project_traits.levels_to_project_traits == 1:
            tmp = Run().cmd('mktemp').call().strip('\r\n')

            with open(tmp, 'w') as f:
                f.write(prepare_commit_msg)

            Run().path('.git').cmd('find . -name "hooks" -exec cp {0} {{}}/prepare-commit-msg \\;'.format(tmp)).run()
            Run().path('.git').cmd('find . -name "prepare-commit-msg" -exec chmod +x {{}} \\;'.format(tmp)).run()


class Internal(Endpoint):
    def name(self):
        return 'internal'

    def _about(self):
        return '{path} - команда вызывается из хука prepare-commit-msg'

    def _rules(self):
        return create('').extended()\
            .statement('Первый параметр - файл с текстом коммит-месседжа',
                       result=self._act,
                       rule=Rule().empty(Data.Delimiter)
                                  .empty(Data.Option)
                                  .size(Data.Target, Op.eq(1)))\
            .product()

    def _act(self, p: Params):
        path = p.targets[0].value

        try:
            ws = BranchRepo().ws
            name = WorkspaceAndTasks.hash(ws)
            project = get_project_name(ws)
            tasks = self.database.get().element(WorkspaceAndTasks, name)

            number = tasks.task(project)
            if number is None:
                return

            task = '['+number+']'

            with open(path) as f:
                lines = f.readlines()
                if not lines[0].startswith(task):
                    lines[0] = task + ' ' + lines[0]
            with open(path, 'w') as f:
                f.writelines(lines)
        except:
            pass


class Set(Endpoint):
    def name(self):
        return 'set'

    def _about(self):
        return '{path} - устанавливает таск для проекта из текущего пути'

    def _rules(self):
        return create('Таск без квадратных скобок, cwd доджен быть WS/src/PROJECT').single_option_command(self._act)

    def _act(self, p: Params):
        project_traits = BranchRepo()
        if project_traits.levels_to_project_traits != 2:
            return

        ws = BranchRepo().ws
        name = WorkspaceAndTasks.hash(ws)
        project = get_project_name(ws)
        task = p.targets[0].value

        try:
            tasks = self.database.get().element(WorkspaceAndTasks, name)
        except:
            tasks = WorkspaceAndTasks(name, {})

        tasks.set_task(project, task)
        self.database.update().element(tasks)
        print('Проект {0} таск [{1}]'.format(colored(project, Color.red), colored(task, Color.green)))


class List(Endpoint):
    def name(self):
        return 'list'

    def _about(self):
        return '{path} - показывает все проекты и таски для них'

    def _rules(self):
        return create('cwd доджен быть WS/src/').empty_command(self._act)

    def _act(self, p: Params):
        project_traits = BranchRepo()
        if project_traits.levels_to_project_traits != 1:
            return

        try:
            ws = project_traits.ws
            name = WorkspaceAndTasks.hash(ws)
            tasks = self.database.get().element(WorkspaceAndTasks, name)
            for project, task in tasks.projects_and_tasks.items():
                print('{0}: -> {1}'.format(colored(project, Color.red), colored(task, Color.green)))
        except:
            pass


class Close(Endpoint):
    def name(self):
        return 'close'

    def _about(self):
        return '{path} - удаляет этот таск из всех проектов, для которых он установлен в хуке'

    def _rules(self):
        return create('cwd доджен быть WS/src/').single_option_command(self._act)

    def _act(self, p: Params):
        project_traits = BranchRepo()
        if project_traits.levels_to_project_traits != 1:
            return

        close = p.targets[0].value
        try:
            ws = project_traits.ws
            name = WorkspaceAndTasks.hash(ws)
            tasks = self.database.get().element(WorkspaceAndTasks, name)
        except:
            return

        ret = {}
        for project, task in tasks.projects_and_tasks.items():
            if close == task:
                print('Удалил {0} из {1}'.format(colored(close, Color.green), colored(project, Color.red)))
            else:
                ret[project] = task
        tasks.projects_and_tasks = ret
        self.database.update().element(tasks)


class Task(Command):
    def name(self):
        return 'task'

    def _about(self):
        return '{path} - работа с prepare-commit-msg'

    def _sub_commands(self):
        return [Init, Internal, Set, List, Close]


commands = register_commands(Task)
