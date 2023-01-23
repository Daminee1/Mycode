from django.urls import path,include
from .import views


urlpatterns = [
   path('file', views.File_Upload.as_view(), name='File_Upload')


]