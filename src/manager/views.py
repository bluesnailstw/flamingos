from manager.celery_app import app
from django.http import HttpResponse, JsonResponse
from salt.salt_api import Pepper
from django.conf import settings


@app.task()
def test_async():
    print("async...")


def debug(request):
    async_task = test_async.delay()
    print(async_task.id)
    return HttpResponse(async_task.id)


def test(request):
    p = Pepper().login()
    # res = p.local(tgt='*', fun='grains.items')
    # res = p.local(tgt='*', fun='pillar.items')
    # res = p.local(tgt='*', fun='network.netstat')
    res = p.local(tgt='*', fun='network.ip_addrs')
    # res = p.local(tgt='*', fun='test.ping')
    return JsonResponse(res)
