import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = open(os.path.join(BASE_DIR, 'files/board.out'), 'r', encoding='utf-8').read()
map_key = {
    'Manufacturer': 'manufacturer',
    'Product Name': 'pname',
    'Serial Number': 'sn'
}
response = {}
for v in res.split('\n\t'):
    res = v.split(':')
    if len(res) == 2:
        if res[0] in map_key:
            response[map_key[res[0]]] = res[1].strip() if res[1].strip() else None
print(response)
