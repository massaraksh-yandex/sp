from platform import config
from src.settings import Settings

class Config(config.Config):
    def __init__(self, m = None):
        super().__init__(map=m, settings=Settings())

