import os
from lib.conf.config import setting

class Basic(object):
    def process(self, command_func, debug):
        if debug:
            res = open(os.path.join(setting.BASE_DIR, 'files/board.out'), 'r', encoding='utf-8').read()
        else:
            res = command_func('basic')
        return self.parse(res)

    def parse(self, res):
        map_key = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'pname',
            'Serial Number': 'sn',
            'Hostname': 'hostname'
        }
        response = {}
        for v in res.split('\n\t'):
            res = v.split(':')
            if len(res) == 2:
                if res[0] in map_key:
                    response[map_key[res[0]]] = res[1].strip() if res[1].strip() else None
        return response
