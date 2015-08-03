import git


class Repo:
    def __init__(self, path):
        self.repo = git.Git(path)
        self.name = path
        self.branch, self.branches, self.valid = self._branch()
        self.dirty, self.cached, self.untracked, self.valid = self._status()

    def _branch(self):
        try:
            branches = []
            branch = ''
            for b in self.repo.branch().split('\n'):
                if b.startswith('*'):
                    branch = b[2:]
                branches.append(b[2:])
            return branch, branches, True
        except Exception:
            return '', [], False

    def _status(self):
        untracked = cached = dirty = False
        valid = True
        try:
            status = self.repo.status(short=True)
            if status:
                for st in status.split('\n'):
                    if not st or dirty and cached and untracked:
                        break
                    first = st[0]
                    if first == '?':
                        untracked = True
                    elif first != ' ':
                        cached = True

                    if st[1] != '?':
                        dirty = True
        except Exception:
            valid = False
            dirty = untracked = True
        return dirty, cached, untracked, valid

    def checkout(self, branch):
        self.repo.checkout(branch)