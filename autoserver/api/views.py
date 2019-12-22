import json
import hashlib
import time
from django.shortcuts import render, HttpResponse
from repository import models

# Create your views here.
def decrypt(msg):
    from Crypto.Cipher import AES
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg)
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')

key_record = {}
def asset(request):
    if request.method == 'GET':
        server_token = 'ksdsfdlleel'
        client_md5_header = request.META.get('HTTP_TOKEN')
        client_md5_token, client_time = client_md5_header.split('|')
        client_time = float(client_time)
        if time.time() - client_time > 10:
            return HttpResponse('[第一关] 请求超时...')
        tmp = '%s|%s' % (server_token, client_time)
        m = hashlib.md5()
        m.update(bytes(tmp, encoding='utf-8'))
        server_md5_token = m.hexdigest()
        if client_md5_token != server_md5_token:
            return HttpResponse('[第二关] token被修改')
        for k in list(key_record.keys()):
            if time.time() > key_record[k]:
                del key_record[k]
        if client_md5_token in key_record:
            return HttpResponse('[第三关] 已经被别人访问过了')
        else:
            key_record[client_md5_token] = client_time + 10
        res = models.Server.objects.all()
        print(res)
        return HttpResponse(res)
    elif request.method == 'POST':
        res = decrypt(request.body)
        new_server_info = json.loads(res)
        hostname = new_server_info['basic']['data']['hostname']
        old_server_obj = models.Server.objects.filter(hostname=hostname).first()
        if not old_server_obj:
            return HttpResponse('该资产并未录入...')
        # 开始清理  disk  memory  nic  board
        if new_server_info['disk']['status'] != 10000:
            models.ErrorLog.objects.create(asset_obj=old_server_obj.asset, title="(%s)的硬盘采集出错了" % hostname, content=new_server_info['disk']['data'])
        old_disk_info = models.Disk.objects.filter(server_obj=old_server_obj)
        new_disk_info = new_server_info['disk']['data']
        new_slot_list = list(new_disk_info.keys())
        old_slot_list = []
        for v in old_disk_info:
            old_slot_list.append(v.slot)
        # 1.增加的slot
        add_slot_list = set(new_slot_list).difference(set(old_slot_list))
        if add_slot_list:
            recorder_list = []
            for v in add_slot_list:
                disk_res = new_disk_info[v]
                tmp = "增加磁盘槽位{slot}, 类型{pd_type}, 容量{capacity}, 型号{model}".format(**disk_res)
                disk_res['server_obj'] = old_server_obj
                models.Disk.objects.create(**disk_res)
                recorder_list.append(tmp)
            recorder_str = ";".join(recorder_list)
            models.AssetRecord.objects.create(asset_obj=old_server_obj.asset, content=recorder_str)
        # 2. 删除的slot
        del_slot_list = set(old_slot_list).difference(set(new_slot_list))
        if del_slot_list:
            models.Disk.objects.filter(slot__in=del_slot_list,server_obj=old_server_obj).delete()
            del_str = "删除的槽位是%s" % (";".join(del_slot_list))
            models.AssetRecord.objects.create(asset_obj=old_server_obj.asset, content=del_str)
        # 3. 更新的slot
        up_slot_list = set(old_slot_list).intersection(set(new_slot_list))
        if up_slot_list:
            recorder_list = []
            for slot in up_slot_list:
                old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=old_server_obj).first()
                new_disk_row = new_disk_info[slot]
                for k, new_v in new_disk_row.items():
                    old_v = getattr(old_disk_row, k)
                    if old_v != new_v:
                        tmp = "槽位:%s, %s由%s改为%s" % (slot, k, old_v, new_v)
                        recorder_list.append(tmp)
                        setattr(old_disk_row, k, new_v)
                        old_disk_row.save()
            if len(recorder_list) > 0:
                models.AssetRecord.objects.create(asset_obj=old_server_obj.asset, content=";".join(recorder_list))

        return HttpResponse('ok')