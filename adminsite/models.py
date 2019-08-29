from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from adminsite.constants import CrawlStatus, TaskType


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


STATUS_CHOICES = ((
                      CrawlStatus.DONE, "完成"
                  ), (
                      CrawlStatus.GOING, "正在进行"
                  ), (
                      CrawlStatus.TODO, "未开始"
                  ))

TASK_CHOICES = ((
                    TaskType.CRAWL, "爬取"
                ), (
                    TaskType.EEXPORT, "导出excel"
                ), (
                    TaskType.EIMPORT, "导入excel"
                ))


class SCBrand(BaseModel):
    brand_name = models.CharField("tianmao url", max_length=255, unique=True, blank=False, null=False)
    # 麻雀主库中品牌编号
    brand_id = models.PositiveIntegerField('品牌编号', blank=True, null=True)
    tianmao_url = models.CharField("tianmao url", max_length=255, blank=False, null=False)
    pass


class CrawlTask(BaseModel):
    url = models.CharField("tianmao url", max_length=255, blank=False, null=False)
    status = models.CharField("状态", max_length=12, blank=False, null=False, default=CrawlStatus.TODO,
                              choices=STATUS_CHOICES)
    filename = models.CharField("", max_length=60, unique=True, blank=False, null=False)
    # 品牌信息
    brand_id = models.PositiveIntegerField('品牌编号', blank=False, null=False, db_index=True)
    finished_time = models.DateTimeField("完成时间", blank=True, null=True)
    celery_result_id = models.CharField("celery任务编号", max_length=255, unique=True, blank=True, null=True)
    task_type = models.CharField("任务类型", max_length=24, blank=False, null=False, default=TaskType.CRAWL,
                                 choices=TASK_CHOICES)

    class Meta:
        db_table = "sparrow_crawl_task"
        verbose_name = _("sparrow crawl task")
        verbose_name_plural = _("sparrow crawl tasks")

    def __str__(self):
        return "%s,%s,%s" % (self.filename, self.brand_id, self.url)


class CrawlProduct(BaseModel):
    url = models.CharField("tianmao url", max_length=255, unique=True, blank=False, null=False)
    title = models.CharField("天猫产品标题", max_length=255)
    subtitle = models.CharField("天猫产品副标题", max_length=128)
    colors = models.CharField("天猫产品颜色", max_length=255, blank=True, null=True)
    sku = models.CharField("货号", max_length=36, blank=False, null=False)
    sizes = models.CharField("尺寸", max_length=128, blank=True, null=True)
    status = models.CharField("状态", max_length=12, blank=False, null=False, default=CrawlStatus.TODO,
                              choices=STATUS_CHOICES)
    # 品牌信息
    brand_id = models.PositiveIntegerField('品牌编号', blank=False, null=False, db_index=True)
    # 麻雀商品编号
    sparrow_product_id = models.PositiveIntegerField('主库中的商品编号', blank=True, null=True)

    class Meta:
        db_table = "sparrow_crawl_product"
        verbose_name = _("sparrow crawl product")
        verbose_name_plural = _("sparrow crawl products")

    def __str__(self):
        return "%s,%s,%s" % (self.sku, self.title, self.url)
