from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def index(request):
    return render(request, 'index.html')


# Below is a working example for a solution.
@csrf_exempt
def squares(request):
    if request.method == "POST":
        data = json.loads(request.body)

        return JsonResponse(data["input"] ** 2, safe=False)
