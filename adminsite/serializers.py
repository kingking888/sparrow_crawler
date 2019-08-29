
from rest_framework import serializers

import logging

from adminsite.models import CrawlProduct, CrawlTask, SCBrand

logger = logging.getLogger(__name__)

class CrawlProductSerializer(serializers.ModelSerializer):
     class Meta:
         model=CrawlProduct
         fields='__all__'

class SCTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlTask
        fields = '__all__'

class SCBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SCBrand
        fields = '__all__'