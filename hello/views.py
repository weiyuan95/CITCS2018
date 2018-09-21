from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


# TEST CODE BELOW:
# @csrf_exempt
def test(request):
    return HttpResponse("Waow")


# @csrf_exempt
def test2(request):
    return HttpResponse(json.dumps({"lol": "wow"}))


def testing_get(request):
    if request.method == "GET":
        # example of getting the key "hello" from a GET request
        print(request.GET["hello"])
        return HttpResponse(request.GET)


# need to wrap method with csrf_exempt for post requests
@csrf_exempt
def testing_post(request):
    if request.method == "POST":
        return HttpResponse(request.POST)

    return HttpResponse("No post request received.")

# https://docs.djangoproject.com/en/2.1/ref/request-response/#httpresponse-objects
# for eg. return HttpResponseNotFound(...)
