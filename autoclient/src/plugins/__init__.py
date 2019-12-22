from lib.conf.config import setting
import importlib
import traceback

class Plugins(object):
    def __init__(self, hostname=None):
        self.hostname = hostname
        self.plugins_dict = setting.PLUGINS_DICT
        self.mode = setting.MODE
        if self.mode == 'ssh':
            self.ssh_user = setting.SSH_USER
            self.ssh_pwd = setting.SSH_PWD
            self.ssh_port = setting.SSH_PORT
            self.ssh_key = setting.SSH_KEY

    def execute(self):
        response = {}
        for k,v in self.plugins_dict.items():
            ret = {'status':None,'data':None}
            try:
                module_name,class_name = v.rsplit('.',1)
                m = importlib.import_module(module_name)
                if hasattr(m,class_name):
                    cls = getattr(m,class_name)
                    res = cls().process(self.__cmd_run, setting.DEBUG)
                    ret['status'] = 10000
                    ret['data'] = res
            except Exception as e:
                ret['status'] = 10001
                ret['data'] = "[%s] 采集 [%s] 报错 错误信息是：%s" % (self.hostname if self.hostname else "Agent", k, str(traceback.format_exc()))
            response[k] = ret
        return response

    def __cmd_run(self, cmd):
        if self.mode == 'agent':
            return self.__agent_run(cmd)
        elif self.mode == 'ssh':
            return self.__ssh_run(cmd)
        elif self.mode == 'salt':
            return self.__salt_run(cmd)
        else:
            print('现在只支持agent/ssh/salt模式')

    def __agent_run(self, cmd):
        import subprocess
        res = subprocess.getoutput(cmd)
        return res

    def __ssh_run(self, cmd):
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        print(result)
        ssh.close()

    def __salt_run(self, cmd):
        import subprocess
        cmd = "salt '%s' cmd.run '%s'" % (self.hostname, cmd)
        res = subprocess.getoutput(cmd)
        return res