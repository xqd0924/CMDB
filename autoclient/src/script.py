from lib.conf.config import setting
from src.client import Agent,SSHSalt

def run():
    if setting.MODE == 'agent':
        obj = Agent()
    else:
        obj = SSHSalt()
    obj.collect()