from os import listdir, getcwd
from os.path import isdir, join
from git import Repo, InvalidGitRepositoryError
from platform.color import colored, Color


def dirs(path):
    return (dir for dir in listdir(path) if isdir(join(path, dir)) and not dir.startswith('.'))


def checkout(branchSelector):
    cwd = getcwd()
    for d in dirs(cwd):
        branchName = branchSelector(d)
        try:
            r = Repo(d)
            if r.active_branch.name != branchName and branchName in r.heads:
                print('{0}: {1} -> {2}'.format(d, colored(r.active_branch.name, Color.red),
                                               colored(branchName, Color.green)))
                r.head.reference = r.heads[branchName]
                r.head.reset(index=True, working_tree=True)
        except InvalidGitRepositoryError:
            pass