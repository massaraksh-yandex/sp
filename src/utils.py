from os import listdir, getcwd
from os.path import isdir, join
from platform.color.color import colored, Color
from src.repo import Repo


def dirs(path = getcwd()):
    return (dir for dir in listdir(path) if isdir(join(path, dir)) and not dir.startswith('.'))


def checkout(branch_repo, cwd = getcwd(), failed_or_pointless = None):
    def fail(s = 'failed', col = Color.red):
        print (d + ': ' + colored(s, col))

    def success(frm, col_from = Color.red, col_to = Color.green):
        print('{0}: {1} -> {2}'.format(d, colored(frm, col_from), colored(wannabe, col_to)))

    for d in dirs(cwd):
        wannabe = branch_repo(d)
        repo = Repo(d)

        if repo.valid:
            if repo.branch != wannabe:
                try:
                    repo.checkout(wannabe)
                    success(repo.branch)
                except Exception:
                    fail()
            elif failed_or_pointless:
                    success(wannabe, col_from=Color.green)
        elif failed_or_pointless:
            fail()