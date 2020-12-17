
from celery import shared_task
from django.conf import settings
from io import BytesIO
from PIL import Image
import os
from django.core.files import File
import string
import json

@shared_task
def adding_task(x, y):
    return x + y

@shared_task
def img_upload(data):
    data = json.dumps(data)
    json_object = json.loads(data)
    url = json_object['digital_ocean_url']
    name, extn = os.path.splitext(os.path.basename(url))
    # initialising bad_chars list
    bad_chars = ['"',' ','!', ':', '*','}','{']
    # # using replace() to
    # # remove bad_chars
    for i in bad_chars:
        extn = extn.replace(i, '')

    if extn in ['.jpg', '.jpeg', '.tif', '.gif']:
        data1 = name + '.png'
        return data1
    elif extn in ['.avi','.mov','.mkv','.flv', '.webm']:
        data1 = name + '.mp4'
        return data1
    else:
        return data
