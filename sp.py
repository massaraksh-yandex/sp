#!/usr/bin/python3 -u
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'platform'))
from platform.utils.main import main
from platform.db.scheme import SchemeFactory
from src.db import WorkspaceAndTasks

if __name__ == '__main__':
    name = 'sp'
    info = '{path} - программа для манипуляции воркспейсом'
    scheme = SchemeFactory('sp', None)\
        .add_folder('workspace_and_tasks', WorkspaceAndTasks)\
        .product()

    main(name, info, scheme)
