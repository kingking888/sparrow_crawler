# Generated by Django 2.2.1 on 2019-08-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsite', '0004_auto_20190827_0550'),
    ]

    operations = [
        migrations.CreateModel(
            name='SCBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('brand_name', models.CharField(max_length=255, unique=True, verbose_name='tianmao url')),
                ('brand_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='品牌编号')),
                ('tianmao_url', models.CharField(max_length=255, verbose_name='tianmao url')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='crawlproduct',
            name='sparrow_product_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='主库中的商品编号'),
        ),
    ]
