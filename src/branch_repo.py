from genericpath import isfile
from os.path import split, abspath, join
from os import getcwd
from platform.execute.run import Run


class BranchRepo(object):
    def _default_branches(self, cwd):
        database = 'project_traits.py'

        self.levels_to_project_traits = 0

        def find_project_data(p, levels_to_project_traits):
            p = split(abspath(p))
            if not p[1]:
                return '', levels_to_project_traits

            if isfile(join(p[0], 'data', database)):
                return p[0], levels_to_project_traits
            else:
                return find_project_data(p[0], levels_to_project_traits+1)

        self.ws, self.levels_to_project_traits = find_project_data(cwd, 1)
        cmd = "python -c 'import project_traits; print project_traits.projectMainBranches'"
        try:
            r = Run().path(join(self.ws, 'data')).cmd(cmd).join_err_and_out().call()

            from ast import literal_eval
            return literal_eval(r)
        except Exception as e:
            print(str(e))

        return {}

    def __init__(self, cwd=getcwd(), def_branch_name='master'):
        self._data = self._default_branches(cwd)
        self._defaultBranchName = def_branch_name

    def __getitem__(self, arg):
        return self._data[arg]['branch'] if arg in self._data else self._defaultBranchName
