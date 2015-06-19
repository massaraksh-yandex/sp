from genericpath import isfile
from os.path import split, abspath, join


def defaultBranch(cwd, project):
    database = 'project_traits.py'
    def findProjectData(path):
        p = split(abspath(path))
        if not p[1]:
            return ''

        path = join(p[0], 'data')
        if isfile(join(path, database)):
            return path
        else:
            if p[1] == '':
                return ''
            else:
                return findProjectData(p[0])

    defBranch = ''
    path = findProjectData(cwd)
    command = "cd {path} && python -c 'import project_traits; print project_traits.projectMainBranches'"
    try:
        from subprocess import Popen, PIPE
        process = Popen(command.format(path=path), shell=True, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()

        import ast
        d = ast.literal_eval(out.decode("utf-8"))
        defBranch = d[project]['branch']
    except Exception:
        pass

    return defBranch
