from django.shortcuts import render, redirect 
from django.http import HttpResponse 
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "index.html")


def inicio(request):
    return render(request, "inicio.html")