from django.urls import path
from . import views
from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register(r'users', views.api_detail_doc_view)
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home-page'),
    path('about-us', views.about, name='about-page'),
    path('upload-file', views.file_uplaod_view, name='file-upload'),
    path('api-auth', views.api_detail_doc_view, name='rest_framework'),

]