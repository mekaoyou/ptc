from django.http import JsonResponse
from django.core import serializers
from models import *

# Create your views here.


def getClass(request):
    classes = PTCClass.objects.all()
    return toJSON(classes, True if len(classes) > 0 else False)


def toJSON(arr, seccuss):
    result = {r'seccuss': seccuss, r'data': serializers.serialize("json", arr, use_natural_foreign_keys=True), }
    return JsonResponse(result, safe=False)


