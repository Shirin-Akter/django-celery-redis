from django.urls import path
from . import views
from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register(r'users', views.api_detail_doc_view)
from .views import Addressables

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home-page'),
    path('home/<slug:post>/', views.post_single, name='post_single'),
    path('about-us', views.about, name='about-page'),
    path('upload-file', views.file_uplaod_view, name='file-upload'),
    path('post-create', views.create_post, name='post_create'),
    path('home/<slug:get>/edit/', views.update_post, name='post_update'),
    path('api-auth', views.api_detail_doc_view, name='rest_framework'),
    #path('api-auth', views.api_detail_doc_view, name='rest_framework'),
    path('tts', views.text_to_speech, name='tts'),



]