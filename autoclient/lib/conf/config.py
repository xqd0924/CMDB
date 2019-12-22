import os
import importlib
from lib.conf import global_settings


class Settings:
    def __init__(self):
        self.__setAttr(global_settings)
        try:
            custom_config = os.environ.get('CUSTOM_CONF')
            settings = importlib.import_module(custom_config)
            self.__setAttr(settings)
        except Exception as e:
            print('此配置不存在...')

    def __setAttr(self,conf):
        for key in dir(conf):
            if key.isupper():
                v = getattr(conf,key)
                setattr(self,key,v)

setting = Settings()