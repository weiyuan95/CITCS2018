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


@csrf_exempt
def get_prime_sum(request):

    if request.method == "POST":
        data = json.loads(request.body)
        num = data["input"]
        # print(prime_sum(num)

        return JsonResponse(prime_sum(num), safe=False)


@csrf_exempt
def tally_expenses(request):

    if request.method == "POST":
        data = json.loads(request.body)
        people_list = data["persons"]
        # expenses is a list of dicts, with each dict representing an expense
        expenses_list = data["expenses"]
        payable_data = calculate_expenses(people_list, expenses_list)
        return JsonResponse(payable_data)


@csrf_exempt
def flight(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # expenses is a list of dicts, with each dict representing an expense
        result = MultipleRunways(data)
        return JsonResponse(result)
