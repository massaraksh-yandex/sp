from genericpath import isfile
from os.path import split, abspath, join


class BranchSelector(object):
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
        command = "cd {path} && python -c 'import project_traits; print project_traits.projectMainBranches'"
        try:
            from subprocess import Popen, PIPE
            process = Popen(command.format(path=path), shell=True, stdout=PIPE, stderr=PIPE)
            out, err = process.communicate()

            from ast import literal_eval
            return literal_eval(out.decode("utf-8"))
        except Exception:
            pass

        return {}

    def __init__(self, cwd, defaultBranchName = ''):
        self._data = self._defaultBranches(cwd)
        self._defaultBranchName = defaultBranchName

    def __getitem__(self, arg):
        return self._data[arg]['branch'] if arg in self._data else self._defaultBranchName
