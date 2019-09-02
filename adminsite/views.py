import os
import time
import traceback

from django.db.models import Q
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from lxml import etree
import xlwt
from rest_framework import status
import threading

from rest_framework.decorators import api_view, authentication_classes, permission_classes
import requests
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from adminsite.models import CrawlProduct, CrawlTask
from adminsite.repository import SCProductRepository
from adminsite.serializers import CrawlProductSerializer, SCTaskSerializer
from adminsite.utils import readFile, timefilename
from celery_tasks.crawler_products_tasks import crawl_list, import_prod_list

# 设置表格样式
from sparrow_crawler import settings


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


@authentication_classes([])
@permission_classes([])
class SCTaskView(APIView, LimitOffsetPagination):
    """
    关于任务的视图
    """
    serializer_class = SCTaskSerializer

    offset_query_param = "start"
    # 通过limit改变默认显示的个数
    limit_query_param = "length"
    # 一页最多显示的个数
    max_limit = 200

    def get(self, request, *args, **kwargs):
        """
        浏览产品列表
        """
        tasks = CrawlTask.objects.all()
        results = self.paginate_queryset(tasks, request, view=self)
        serializer = SCTaskSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


@authentication_classes([])
@permission_classes([])
class SCProductView(APIView, LimitOffsetPagination):
    """
    关于天猫产品的视图
    """
    serializer_class = CrawlProductSerializer

    offset_query_param = "start"
    # 通过limit改变默认显示的个数
    limit_query_param = "length"
    # 一页最多显示的个数
    max_limit = 200

    def get(self, request, *args, **kwargs):
        """
        浏览产品列表
        """
        filters=[]
        brand_id = request.GET.get('brand_id')
        if brand_id:
            filters.append(Q(brand_id=brand_id))
        name_like=request.GET.get('query')
        if name_like:
            filters.append(Q(title__icontains=name_like)|Q(subtitle__icontains=name_like))

        if len(filters)==0:
            products = CrawlProduct.objects.all()
        else:
            products = CrawlProduct.objects.filter(*filters)

        results = self.paginate_queryset(products, request, view=self)
        serializer = CrawlProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        """
        创建产品
        """
        try:
            product = SCProductRepository.create(request.data)
            print(product)
            return Response(product, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def crawl_brand_list(request):
    try:
        pass
    except Exception as e:
        traceback.print_exc()
    return Response({"status": True, "message": ""}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def action_crawl_list(request):
    try:
        items = request.data['urls']
        filename = request.data['filename']
        rule_name = request.data['rule_name']

        # 最简单的threading任务
        # thread = threading.Thread(target=crawl_list, args=(filename, items))
        # thread.start()

        # 调用celery的异步任务
        crawl_list.delay(filename, rule_name, items)
        # 调用scrapy的异步任务

    except Exception as e:
        traceback.print_exc()
    return Response({"status": True, "message": "已经提交任务，完成后会收到邮件提示"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def import_excel_prod_list(request):
    try:
        filename = request.data['filename']
        brand_id = request.data['brand_id']

        # 调用celery的异步任务
        import_prod_list.delay(filename, brand_id)
        # 调用scrapy的异步任务

    except Exception as e:
        traceback.print_exc()
    return Response({"status": True, "message": "已经提交任务，完成后会收到邮件提示"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def web_import_excel_prod_list(request):
    """
    通过bootstrap fileinput 上传文件
    """
    result = {"data": []}

    try:
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        ret = -1
        brand_id = request.data.get('brand_id')
        file = request.FILES.get("file_data", None)
        if file:
            print(file.name)

            filename = os.path.join(settings.SC_FILE_PATH, timefilename(file.name))
            print(filename)
            destination = open(filename, 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in file.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            # 写入这个xls文件
            import_prod_list.delay(filename, brand_id)
        return JsonResponse(result)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse(result)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def export_file(request):
    try:
        filename = request.GET.get('filename')
        the_file_name = filename
        ext_type = request.GET.get('exttype')
        response = StreamingHttpResponse(readFile(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        return response

    except Exception as e:
        traceback.print_exc()
        return Response({"status": True, "message": "下载失败"}, status=status.HTTP_200_OK)
