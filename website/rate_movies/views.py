# from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

# create our index function for view which we set in urls.py
def index(request):
	return HttpResponse("<h1>This is Home Page")