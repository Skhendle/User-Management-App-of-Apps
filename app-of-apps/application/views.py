from django.shortcuts import render
from django.http import HttpResponse



def applications_list(request):
    return HttpResponse("Hello world!")