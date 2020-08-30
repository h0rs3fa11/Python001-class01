from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def phone(request):
    return HttpResponse("show phone result here")
