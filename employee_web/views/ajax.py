import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def learn_ajax(request):
    return render(request, "learn_ajax.html")


@csrf_exempt  # 免除csrf的认证
def test_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True}
    return HttpResponse(json.dumps(data_dict))
    # return JsonResponse(data_dict)  效果一致
