#!/usr/bin/env python3.4 -u
from platform import utils
from src.config import Config

if __name__ == "__main__":
    utils.main('sp', __file__, Config())

