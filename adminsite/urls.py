from django.conf.urls import url
from django.urls import path

from adminsite import views

app_name = 'crawl_site_api'
urlpatterns = [
    path('o/crawl/list/', views.action_crawl_list, name="crawl_list"),
    path('o/import/productlist/', views.web_import_excel_prod_list, name="web_import_prod_list"),
    path('o/crawl/import/productlist/', views.import_excel_prod_list, name="crawl_prod_list"),
    path('o/download/', views.export_file, name="export_file"),
    path('o/product/list/', views.SCProductView.as_view(), name="scproduct"),
    path('o/task/list/', views.SCTaskView.as_view(), name="sctask"),
]
