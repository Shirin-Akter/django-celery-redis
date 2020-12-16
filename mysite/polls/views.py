import json

from django.shortcuts import render
from django.http import HttpResponse,  JsonResponse
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.files import File
from PIL import Image
from PIL import *
import os
from .tasks import img_upload


from rest_framework.decorators import api_view
from .serializers import DocumentSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Document
from rest_framework.response import Response





te = {'hello' : 'ruhi'}
posts = [
    {
        'author' : 'Shirin',
        'title' : 'blog post1',
        'content' : 'first post content',
        'date_posted' : '14th of august 2010'

    },
    {
            'author' : 'Ruhi',
            'title' : 'blog post2',
            'content' : 'second post content',
            'date_posted' : '15th of august 2010'

    }


]

def index(request):
    #this is the dictionary
    context = {
        'posts' : posts
    }
    return render(request, 'blog/home.html', context)
    #return HttpResponse('<h1>Hello world! Index </h1>')
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
        form = UploadFileForm()
        return render(request, 'blog/file_upload_temp.html', {'form': form})
    # return render(request, 'blog/about.html', {'title' : 'about title working!'})

def file_uplaod_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # start of image
        myfile = request.FILES['document']
        if form.is_valid():
            this_entry = form.save(commit=False)
            file = this_entry.document
            print('file size> ', vars(file))

            data = json.dumps(this_entry.description)
            task = img_upload.delay(json.dumps(file.name))

            file1 = task.get()
            name, extn = os.path.splitext((file1))
            file.name = file1
            if extn == 'PNG':
                output = BytesIO()
                img1 = Image.open(file)
                size_100 = (100, 100)
                img1.thumbnail(size_100)
                img1.save(output, 'PNG', quality=85)  # save image to BytesIO object
                thumbnail = File(output, name=file.name)  # create a django friendly File object
                file = thumbnail

            this_entry.document = file
            print('file1 size :> ', file.size)

            print('this is celery task results: ', task.id , 'this is success: ', task.status, 'task get: ', task.get() )
            this_entry.document.save(file.name, file)
            results = this_entry.save()
    else:
        form = UploadFileForm()
        return render(request, 'blog/file_upload_temp.html', {'form': form})
    return HttpResponse('<p>Uploaded and printed to terminal</p>')



@api_view(['GET', 'POST'])
def api_detail_doc_view(request):
    if request.method == 'POST':
        success = 'fail'
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('hello api')
            this_entry = form.save(commit=False)
            file = this_entry.document
            data = this_entry.description
            url = this_entry.document.url
            #data = JSONParser().parse(des.read())
            #print(type(des))
            print('th si si des: ', this_entry.document.url)
            seri = DocumentSerializer(data = ({'digital_ocean_url' : url}) )
            # print(seri.is_valid)
            if seri.is_valid():
                print('this is valid serializer')
                seri.save()
                print('thsi is ser-> ', seri.data)
                # seri.save()
                # print('this is seri data-> ', seri)
                name, extn = os.path.splitext((file.name))
                data = json.dumps(this_entry.description)
                task = img_upload.delay(json.dumps(this_entry.document.name))
                file1 = task.get()
                success = task.status
                file.name = file1
                this_entry.document = file
                print('this is celery task results: ', task.id, 'this is success: ', task.status, 'task get: ',
                      task.get())
                this_entry.document.save(file.name, file)
                results = this_entry.save()
    else:
        form1 = UploadFileForm()
        # print(form1)
        # return JsonResponse(file_,status=201)
        # return Response({'form': form1})
        return render(request, 'blog/file_upload_temp.html', {'form': form1})
    # return HttpResponse('<p>Uploaded and printed to terminal</p>')
    return Response({'success': success})




