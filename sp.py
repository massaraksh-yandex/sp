#!/usr/bin/python3.4 -u
from platform import utils
from src.config import Config
import sys
sys.path.append('git/git')

if __name__ == "__main__":
    utils.main('sp', __file__, Config())

