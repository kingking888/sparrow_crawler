# Generated by Django 2.2.1 on 2019-08-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsite', '0002_auto_20190824_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=255, unique=True, verbose_name='tianmao url')),
                ('status', models.CharField(choices=[('done', '完成'), ('going', '正在进行'), ('todo', '未开始')], default='todo', max_length=12, verbose_name='状态')),
                ('filename', models.CharField(max_length=60, unique=True, verbose_name='')),
                ('brand_id', models.PositiveIntegerField(db_index=True, verbose_name='品牌编号')),
                ('finished_time', models.DateTimeField(blank=True, null=True, verbose_name='完成时间')),
                ('celery_result_id', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='celery任务编号')),
                ('task_type', models.CharField(choices=[('crawl', '爬取'), ('eexport', '导出excel'), ('eimport', '导入excel')], default='crawl', max_length=24, verbose_name='任务类型')),
            ],
            options={
                'verbose_name': 'sparrow crawl task',
                'verbose_name_plural': 'sparrow crawl tasks',
                'db_table': 'sparrow_crawl_task',
            },
        ),
    ]
