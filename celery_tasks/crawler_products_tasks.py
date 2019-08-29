from datetime import datetime

import requests
import xlwt
from celery.schedules import crontab
import traceback
import xlrd
from lxml import etree

from adminsite.constants import TaskType, CrawlStatus
from adminsite.models import CrawlTask
from adminsite.utils import read_products_file
from sparrow_crawler.celery_app import app
import os

import logging

logger = logging.getLogger('crawler_products_tasks')

keywords = ["款号", "货号", "型号", ":", "："]

shop_rules = {
    "tmall": [
        "//div[@id='detail']//h1/text()",
        "//div[contains(@class,'tb-detail-hd')]//p/text()",
        "//li[contains(text(),'款号') or contains(text(),'货号') or contains(text(),'型号')]/text()",
        "//div[@class='tb-sku']//ul[contains(@data-property,'颜色')]/li/@title"
    ],
    "chin-chin": [
        "//div[@id='detail']//h3/text()",
        "//div[contains(@class,'tb-detail-hd')]//p/text()",
        "//li[contains(text(),'款号') or contains(text(),'货号') or contains(text(),'型号')]/text()",
        "//ul[contains(@data-property,'颜色')]/li//span/text()"
    ]
}


def crawl_one_simple(sheet,rule, idx, url):
    # 首先检查数据库

    try:
        r = requests.get(url)
        sheet.write(idx, 0, url)
        if int(r.status_code) == 200:
            content = etree.HTML(r.text)

            # 标题
            nodes = content.xpath(rule[0])
            h1 = ""
            for one in nodes:
                one = one.strip()
                if len(one) > 0:
                    h1 = h1 + one
            sheet.write(idx, 2, h1)

            # 副标题
            nodes = content.xpath(rule[1])
            h2 = ""
            for one in nodes:
                one = one.strip()
                if len(one) > 0:
                    h2 = h2 + one
            sheet.write(idx, 3, h2)

            # 款号
            nodes = content.xpath(rule[2])
            sku = ''
            for one in nodes:
                one = one.strip()
                if len(one) > 0:
                    for key in keywords:
                        one = one.replace(key, "")
                    sku = sku + one.strip()
            sheet.write(idx, 1, sku)

            # 颜色
            # colors=content.xpath("//div[@class='tb-sku']//ul[contains(@data-property,'颜色')]/li/@title")
            colors = content.xpath(rule[3])
            _color = ""
            if colors:
                _color = ",".join(colors)
            sheet.write(idx, 4, _color)

            # 尺码
            # sizes

            print("%s,%s,%s,%s,%s" % (url, sku, h1, h2, _color))
    except Exception as e:
        traceback.print_exc()


def crawl_thread(filename,rule_name, items):
    try:
        rule=shop_rules.get(rule_name)
        if not rule:
            rule=shop_rules.get('tmall')

        idx = 1
        f = xlwt.Workbook()
        sheet1 = f.add_sheet('商品列表', cell_overwrite_ok=True)
        row0 = ["链接", "货号", "标题", "副标题", "颜色"]
        # 写第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])

        for item in items:
            crawl_one_simple(sheet1,rule, idx, item)
            idx = idx + 1

        f.save(filename + '.xls')

        # 发送邮件

        # 提供下载


    except Exception as e:
        traceback.print_exc()


@app.task(name="crawl_list")
def crawl_list(filename,rule_name, data):
    print(filename)
    crawl_thread(filename, rule_name,data)
    print('~~~~~~~~')


@app.task(name="import_prod_list")
def import_prod_list(filename, brand_id):
    try:
        # 写入库
        task = CrawlTask()
        task.brand_id = brand_id
        task.filename = filename
        task.task_type = TaskType.EIMPORT
        task.url = '/download/'
        task.save()

        # 执行任务
        read_products_file(filename, brand_id)

        # 更新库
        task.status = CrawlStatus.DONE
        task.finished_time = datetime.now()
        task.save()
    except Exception as e:
        traceback.print_exc()


@app.task(name="crawl_prod_detaiol")
def crawl_prod_detail(product_id, brand_id):
    print('~~~~~~~~')
