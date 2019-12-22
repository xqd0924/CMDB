import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODE = 'agent'

DEBUG = True

API_URL = 'http://127.0.0.1:8000/api/asset/'

KEY_STR = b'dfdsdfsasdfdsdfs'

PLUGINS_DICT = {
    'basic':'src.plugins.basic.Basic',
    'cpu':'src.plugins.cpu.Cpu',
    'disk':'src.plugins.disk.Disk',
    'memory':'src.plugins.memory.Memory',
    'nic':'src.plugins.nic.Nic',
}