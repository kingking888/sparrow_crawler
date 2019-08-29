from django.shortcuts import render


def index(request,template_name):
    return render(request,template_name)

