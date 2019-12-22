import requests
import time
import hashlib


client_time = time.time()
token = 'ksdsfdlleel'
tmp = '%s|%s' %(token,client_time)
m = hashlib.md5()
m.update(bytes(tmp, encoding='utf-8'))
client_md5_token = m.hexdigest()
header_token = '%s|%s' % (client_md5_token, client_time)
res = requests.get('http://127.0.0.1:8000/api/asset/', headers={'token':header_token})
print(res.text)