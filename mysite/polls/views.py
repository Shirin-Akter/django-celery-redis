import json

from django.shortcuts import render
from django.http import HttpResponse,  JsonResponse
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from io import BytesIO
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
        # seri = DocumentSerializer(form)

        # print('json print: ', seri.fields)
        # start of image
        myfile = request.FILES['document']


        if form.is_valid():
            print('hello')
            # file_path = os.path.join(settings.IMAGES_DIR, request.FILES['image_file'].name)
            #form1.save()


            # data = serializers.serialize('json', d)
            # print('data serializers: ', data)

            this_entry = form.save(commit=False)
            file = this_entry.document
            name, extn = os.path.splitext((file.name))
            # file1 = name + '.png'
            # file.name = file1
            # this_entry.document = file
            data = json.dumps(this_entry.description)
            print('this is document: ', json.dumps(this_entry.document.name))
            # file = this_entry.document
            # name, extn = os.path.splitext((this_entry.document.name))
            # this_entry.document = file
            # this_entry.document.save(name + '{}.png', file)



            # task = img_upload.delay(myfile, this_entry)

            # x = json.dumps(this_entry.document)
            task = img_upload.delay(json.dumps(this_entry.document.name))
            file1 = task.get()
            file.name = file1
            this_entry.document = file
            # task.save()
            print('this is celery task results: ', task.id , 'this is success: ', task.status, 'task get: ', task.get() )
            # this_entry.document = file1
            # name, extn = os.path.splitext((this_entry.document.name))
            this_entry.document.save(name + '{}.png', file)
            results = this_entry.save()




            # this_entry.document.name --> split this , then upadate this
            # this_entry.save()
            # this_entry.document = img1.save('name'+".thumbnail", "JPEG")
            print('this is udated entry ', vars(this_entry))
            # print('this is udated11 entry ', type(this_entry.document) )
    else:
        form = UploadFileForm()
        return render(request, 'blog/file_upload_temp.html', {'form': form})
#
#
#     name, extension = os.path.splitext(this_entry.document.name)
#     print('extension: ',extension)
#     print('name: ', name)
#     print('this entry: ',this_entry)
#     print('this entry document', this_entry.document)

    return HttpResponse('<p>Uploaded and printed to terminal</p>')



@api_view(['GET', 'POST'])
def api_detail_doc_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('hello api')
            this_entry = form.save(commit=False)
            file = this_entry.document
            data = this_entry.description
            #data = JSONParser().parse(des.read())
            #print(type(des))
            print('th si si des: ', this_entry.document.url)
            seri = DocumentSerializer(data = this_entry.document)
            # print(seri.is_valid)
            if seri.is_valid():
                print('this is valid serializer')
                seri.save()
                # print('thsi is ser-> ', seri.data)
                # seri.save()
                # print('this is seri data-> ', seri)
    else:
        form1 = UploadFileForm()
        # print(form1)
        # return JsonResponse(file_,status=201)
        return render(request, 'blog/file_upload_temp.html', {'form': form1})
    return HttpResponse('<p>Uploaded and printed to terminal</p>')
    # return Response({'form': form})




