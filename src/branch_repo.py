from genericpath import isfile
from os.path import split, abspath, join
from os import getcwd
from platform.execute.local import local
from platform.execute.run import run


class BranchRepo(object):
    def _defaultBranches(self, cwd):
        database = 'project_traits.py'

        def findProjectData(path):
            p = split(abspath(path))
            if not p[1]:
                return ''

            path = join(p[0], 'data')
            if isfile(join(path, database)):
                return path
            else:
                return findProjectData(p[0])

        path = findProjectData(cwd)
        cmd = "python -c 'import project_traits; print project_traits.projectMainBranches'"
        try:
            r = run(impl=local()).path(path).cmd(cmd).withstderr().call()

            from ast import literal_eval
            return literal_eval(r)
        except Exception:
            pass

        return {}

    def __init__(self, cwd = getcwd(), def_branch_name = 'master'):
        self._data = self._defaultBranches(cwd)
        self._defaultBranchName = def_branch_name

    def __getitem__(self, arg):
        return self._data[arg]['branch'] if arg in self._data else self._defaultBranchName
