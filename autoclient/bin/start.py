import os
os.environ['CUSTOM_CONF'] = 'config.settings'
from src.script import run


if __name__ == '__main__':
    run()