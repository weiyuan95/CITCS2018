from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import Greeting


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


# TEST CODE BELOW:
@csrf_exempt
def test(request):
    return HttpResponse("Waow")


@csrf_exempt
def test2(request):
    return HttpResponse(json.dumps({"lol": "wow"}))

