import json
import os
from io import BytesIO
from ibm_watson import DiscoveryV1
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


from PIL import *
from PIL import Image
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ibm_watson.speech_to_text_v1 import SpeechToTextV1
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UploadFileForm, BlogForm, CommentForm
from .models import Document, Blog
from .serializers import DocumentSerializer
from .tasks import img_upload, tts, stt

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
    return render(request, 'blog/index.html', context)
    #return HttpResponse('<h1>Hello world! Index </h1>')
def home(request):
    user = request.user
    context = {
        'posts': posts
    }

    all_posts = Blog.objects.filter(status = 'Published')
    # st = all_posts.filter(status = 'published')
    return render(request, 'blog/home.html', {'posts': all_posts})

    # return render(request, 'blog/home.html', {'user': user})


def post_single(request, post):
    post = get_object_or_404(Blog, slug = post, status= 'Published')

    return render(request, 'blog/single.html', {'post':post})
def create_post(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            blog_form.save(commit = True)
    else:
        blog_form = BlogForm()
        return render(request, 'blog/blog_create_form.html', {'blog_form': blog_form})
    return HttpResponse('<p>Uploaded and printed to terminal</p>')
def update_post(request, get):
    object = Blog.objects.get(slug=get)
    blog_form = BlogForm(instance=object)

    print('this is object: ', object)
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, instance=object)
        if blog_form.is_valid():
            blog_form.save(commit=True)
    # if request
    return render(request, 'blog/blog_create_form.html', {'blog_form': blog_form})
    return HttpResponse('<p>Updated and printed to terminal</p>')

def add_comment_to_post(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            result = comment_form.save(commit= False)
            result.post = post
            comment_form.save(commit = True)
            return redirect('post_single', post = slug)
    else:
        comment_form = CommentForm()
        return render(request, 'blog/comment_form.html', {'comment_form' : comment_form})

def about(request):
        form = UploadFileForm()
        return render(request, 'blog/file_upload_temp.html', {'form': form})
def file_uplaod_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # start of image
        myfile = request.FILES['document']
        if form.is_valid():
            this_entry = form.save(commit=False)
            file = this_entry.document
            url = this_entry.document.url
            seri = DocumentSerializer(data=({'digital_ocean_url': url}))
            if seri.is_valid():
                print('this is valid serializer')
                seri.save()
                print('this is serializer data-> ', seri.data)

                task = img_upload.delay(seri.data)
                file1 = task.get()
                name, extn = os.path.splitext((file1))
                file.name = file1
                # it is is image then perform compression
                if extn == '.png':
                    output = BytesIO()
                    img1 = Image.open(file)
                    size_100 = (100, 100)
                    img1.thumbnail(size_100)
                    img1.save(output, 'PNG', quality=85)  # save image to BytesIO object
                    thumbnail = File(output, name=file.name)  # create a django friendly File object
                    file = thumbnail

                this_entry.document = file
                this_entry.document.save(file.name, file)
                results = this_entry.save()
                ins = Document(digital_ocean_url = url)
                print('this is ins: ', ins)
                ins.save()
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
            this_entry = form.save(commit=False)
            file = this_entry.document
            data = this_entry.description
            url = this_entry.document.url
            seri = DocumentSerializer(data = ({'digital_ocean_url' : url}) )
            if seri.is_valid():
                print('this is valid serializer')
                seri.save()
                print('this is serializer data-> ', seri.data)

                task = img_upload.delay(seri.data)
                file1 = task.get()
                success = task.status
                name, extn = os.path.splitext((file1))
                file.name = file1
                # it is is image then perform compression
                if extn == '.png':
                    output = BytesIO()
                    img1 = Image.open(file)
                    size_100 = (100, 100)
                    img1.thumbnail(size_100)
                    img1.save(output, 'PNG', quality=85)  # save image to BytesIO object
                    thumbnail = File(output, name=file.name)  # create a django friendly File object
                    file = thumbnail
                # video or audio file upload
                this_entry.document = file
                this_entry.document.save(file.name, file)
                results = this_entry.save()

    else:
        form1 = UploadFileForm()
        return render(request, 'blog/file_upload_temp.html', {'form': form1})
    # return HttpResponse('<p>Uploaded and printed to terminal</p>')
    return Response({'success': success})

class Addressables(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uid):
        print('this is get', uid)
       # value = 'hello this is get!'
        id = 163
        value = Document.objects.get(id= uid)
        print('value: ' , value)
        return Response({'value': value.digital_ocean_url})
    def post(self, request):
            if request.method =='POST':
                return Response({'value:': 'post method'})
        #     value_set = Document.object.filter(id_in = [])




def text_to_speech(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            success = 'fail'
            form_data = form.save(commit=False)
            # file = form_data.document
            # description = form_data.description
            # url = "https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/b85a7740-98a7-430b-a122-208a75c00cd7"
            # apikey = "kkMD8MeGj8_EkNdbfrnwYCH9A6N6PtrQlT5ebEes3W3M"
            # des is a form variable which will be fetched from the from data, for now its is hardcoded
            des = 'text to speech1'
            if(des == 'text to speech'):
                task = tts.delay()
                res1 = task.get()
                success = task.status
                print('this is res1: ', res1)

                # auth = IAMAuthenticator(apikey)
                # tts = TextToSpeechV1(authenticator=auth)
                # tts.set_service_url(url)
                # with open('C:/Dev/speechV1.mp3', 'wb') as audiofile:
                #     res = tts.synthesize('Hello ELS!', accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
                #     audiofile.write(res.content)

            else:
                task = stt.delay()
                res1 = task.get()
                success = task.status
                print('this is res1: ', res1)
                # url = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/52b1609a-5ee1-49db-afbb-f748c7a67b01"
                # apikey = "gn1zMcCSMotsWUP3C0OvF7oZAKsrLVKkoeRRkvZbgBtd"
                # auth = IAMAuthenticator(apikey)
                # stt = SpeechToTextV1(authenticator=auth)
                # stt.set_service_url(url)
                # with open('C:/Dev/speechV1.mp3', 'rb') as file:
                #     res = stt.recognize(audio=file, content_type='audio/mp3', model='en-US_NarrowbandModel',
                #                         continuous=True).get_result()
                # text = res['results'][0]['alternatives'][0]['transcript']
                # confidence = res['results'][0]['alternatives'][0]['confidence']
                # with open('C:/Dev/speech_txt.txt', 'w') as out:
                #     out.writelines(text)

    else:
        form1 = UploadFileForm()
        return render(request, 'blog/file_upload_temp.html', {'form': form1})
    return HttpResponse(success)



# test funtions

def func1(text):
    func2(text)
def func2(text1):
    func3(text1)
def func3(text2):
    return text2