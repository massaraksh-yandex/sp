from genericpath import isfile
from os.path import split, abspath, join

__author__ = 'massaraksh'


def defaultBranch(cwd, project):
    import imp
    database = 'project_traits.py'
    def findProjectData(path):
        p = split(abspath(path))
        if not p[1]:
            return ''

        traits = join(p[0], 'data', database)
        if isfile(traits):
            return traits
        else:
            if p[1] == '':
                return ''
            else:
                return findProjectData(p[0])

    path = findProjectData(cwd)

    defBranch = ''
    try:
        module = imp.load_source('projectMainBranches', path)
        defBranch = module.projectMainBranches[project]['branch']
    except Exception:
        pass

    return defBranch