from django.shortcuts import render


def index(request,template_name):
    return render(request,template_name,{"brand_id":request.GET.get('brand_id')})

