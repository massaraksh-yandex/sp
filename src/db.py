import json


class WorkspaceAndTasks:
    def __init__(self, name, projects_and_tasks):
        self.name = name
        self.projects_and_tasks = projects_and_tasks

    def task(self, project):
        return self.projects_and_tasks[project] if project in self.projects_and_tasks else None

    def set_task(self, project, task):
        self.projects_and_tasks[project] = task

    def __repr__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def hash(path: str):
        return path.replace('/', '_')

    @staticmethod
    def load_from(mmap):
        return WorkspaceAndTasks(mmap['name'], mmap['projects_and_tasks'])