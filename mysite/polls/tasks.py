
from celery import shared_task
from django.conf import settings
from io import BytesIO
from PIL import Image
import os
from django.core.files import File

@shared_task
def adding_task(x, y):
    return x + y

@shared_task
def img_upload(data):
    name, extn = os.path.splitext((data))
    if extn in ['.jpg', '.jpeg', '.tif', '.gif']:
        data1 = name + '.png'
        return data1
    elif extn in ['.avi']:
        data1 = name + '.mp4'
        return data1
    else:
        return data
