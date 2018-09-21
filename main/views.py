from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from main.wy.solutions import *
from main.ted.solutions import *
from main.randy.solutions import *
import json


# Create your views here.
def index(request):
    return render(request, 'index.html')


# Below is a working example for a solution.
@csrf_exempt
def squares(request):

    if request.method == "POST":
        data = json.loads(request.body)

        return JsonResponse(get_square(data["input"]), safe=False)

    return HttpResponseBadRequest(request)
