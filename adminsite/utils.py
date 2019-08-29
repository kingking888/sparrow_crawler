import time
import traceback
import xlrd
from adminsite.models import CrawlProduct
from django.conf import settings

def readFile(filename, chunk_size=512):
    filename=settings.SC_FILE_PATH+filename
    print(filename)
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def read_products_file(filename,brand_id):
    myWorkbook = xlrd.open_workbook(filename)
    mySheets = myWorkbook.sheets()  # 获取工作表list。
    mySheet = mySheets[0]  # 通过索引顺序获取。
    nrows = mySheet.nrows
    ncols = mySheet.ncols
    for i in range(0,nrows):
        try:
            myRowValues = mySheet.row_values(i)  # i是行数，从0开始计数，返回list对象。
            _len=len(myRowValues)
            #是否数据库已有该产品
            existingProduct=None #CrawlProduct.objects.filter()

            #不用检测重复的URL？

            #若数据库中没有记录则插入新记录
            if not existingProduct:
                product=CrawlProduct()
                product.url=myRowValues[0]
                product.sku=myRowValues[1]
                product.title=myRowValues[2]
                if _len>3:
                  product.subtitle=myRowValues[3]
                if _len>4:
                    product.colors=myRowValues[4]
                if _len>5:
                    product.sizes=myRowValues[5]
                product.brand_id=brand_id
                product.save()
        except Exception as e:
            traceback.print_exc()


def timefilename(filename):
    if filename:
        idx=filename.rfind(".")
        ext=""
        if idx>=0:
            ext=filename[idx:]
        _n = "%d" % (time.time() * 1000)
        _f = time.strftime("%Y%m%d", time.localtime())

        file_name = _f + _n+ext
        return file_name
    return None

if __name__=='__main__':
    read_products_file("/Users/tinawang/Documents/xls/包小姐鞋先生.xls")