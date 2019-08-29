import logging
import traceback

from django.db import transaction
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError

from adminsite.serializers import CrawlProductSerializer

logger = logging.getLogger(__name__)

def create(data):
    print(data)
    try:
        with transaction.atomic():
            serializer=CrawlProductSerializer(data=data)
            if serializer.is_valid():
                instance=serializer.save()
                print(instance)
                return model_to_dict(instance)
            else:
                raise ValidationError(serializer.errors)
    except Exception as e:
        traceback.print_exc()
        raise e

def noIncludeProducts(data):
    pass

