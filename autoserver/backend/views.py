from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository import models

# Create your views here.
def server(request):
    return render(request, 'server_bt.html')

def ajax_server(request):
    table_config = [
        {
            "field": 'id',
            "title": 'id',
        },
        {
            "field": 'hostname',
            "title": '主机名',
        },
        {
            "field": 'sn',
            "title": 'sn号',
        }
    ]
    field_list = []
    for v in table_config:
        field_list.append(v['field'])
    res = models.Server.objects.values(*field_list)
    total = models.Server.objects.count()
    # ret = {
    #     "table_config": table_config,
    #     "data_list": list(res)
    # }
    ret = {
        'total': total,
        'rows': list(res)
    }

    return JsonResponse(ret,safe=False)

def asset(request):
    return render(request, 'asset.html')

def ajax_asset(request):
    table_config = [
        {
            "field": 'id',
            "title": 'id',
        },
        {
            "field": 'cabinet_num',
            "title": '机柜号',
        },
        {
            "field": 'cabinet_order',
            "title": '序号',
        }
    ]
    field_list = []
    for v in table_config:
        field_list.append(v['field'])
    res = models.Asset.objects.values(*field_list)
    ret = {
        "table_config": table_config,
        "data_list": list(res)
    }

    return JsonResponse(ret,safe=False)

def modify(request):
    print(request.POST.getlist('ids'))
    return HttpResponse('ok')