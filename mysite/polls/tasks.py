
from celery import shared_task
from django.conf import settings
from io import BytesIO
from PIL import *
from PIL import Image
import os

@shared_task
def adding_task(x, y):
    return x + y

@shared_task
# def img_upload(myfile, this_entry):
def img_upload(data):
    # myf1 = request.FILES['document']
    res = 'Hello This is Celery tasks'
    print('this is data: ', data)
    # text, ext = os.path.splitext(myfile.name)
    # print('rr--> ', text)
    # img1 = Image.open(myfile)
    # img1.show()
    # size_100 = (100, 100)
    # img1.thumbnail(size_100)
    # newImg = 'media/' + text + '.mp3'
    #
    #
    #
    #
    # file = this_entry.document
    name, extn = os.path.splitext((data))
    data1 = name + '.png'
    # this_entry.document = file
    # this_entry.document.save(name + '{}.png', file)
    # # results = this_entry.save()
    #
    # return this_entry
    return data1