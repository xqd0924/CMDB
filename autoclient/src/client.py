import json
import os
import requests
from lib.conf.config import setting
from src.plugins import Plugins
from lib.utils import encrypt


class Base(object):
    def post_data(self, server_info):
        server_info = encrypt(server_info)
        requests.post(setting.API_URL, data=server_info)

class Agent(Base):
    def collect(self):
        server_info = Plugins().execute()
        hostname = server_info['basic']['data']['hostname']
        res = open(os.path.join(setting.BASE_DIR,'config/cert'), 'r', encoding='utf-8').read()
        if not res.strip():
            with open(os.path.join(setting.BASE_DIR,'config/cert'), 'w', encoding='utf-8') as fp:
                fp.write(hostname)
        else:
            server_info['basic']['data']['hostname'] = res
        for k,v in server_info.items():
            print(k,v)
        server_info = json.dumps(server_info)
        self.post_data(server_info)


class SSHSalt(Base):
    def get_hostnames(self):
        requests.get(setting.API_URL)
        return ['10.0.0.100',]

    def run(self,hostname):
        server_info = Plugins(hostname).execute()
        self.post_data(server_info)

    def collect(self):
        hostnames = self.get_hostnames()
        from concurrent.futures import ThreadPoolExecutor
        p = ThreadPoolExecutor(10)
        for hostname in hostnames:
            p.submit(self.run, hostname)

