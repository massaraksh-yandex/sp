from platform import settings
from os.path import join


class Settings(settings.Settings):
    def __init__(self):
        super().__init__('.sp')

