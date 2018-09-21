from django.shortcuts import render
from django.http import HttpResponse
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
def test(request):
    return HttpResponse("Waow")


def test2(request):
    return HttpResponse(json.dumps({"lol": "wow"}))

