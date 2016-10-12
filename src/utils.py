from os import listdir, getcwd
from os.path import isdir, join
from platform.color.color import colored, Color
from src.repo import Repo


def get_project_name(ws: str):
    return getcwd()[len(ws) + 1:].split('/')[1]


def dirs(path=getcwd(), show_hidden=False):
    ret = []
    for d in listdir(path):
        if isdir(join(path, d)) and (not d.startswith('.') or show_hidden):
            ret.append(d)
    return ret


def checkout(branch_repo, cwd=getcwd(), show_failed_or_pointless=False):
    def fail(s='failed', col=Color.red):
        print(d + ': ' + colored(s, col))

    def success(frm, col_from=Color.red, col_to=Color.green):
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
            elif show_failed_or_pointless:
                    success(wannabe, col_from=Color.green)
        elif show_failed_or_pointless:
            fail()
