from django.urls import path,include
from .import views


urlpatterns = [
   path('subjects', views.Subjects_Details.as_view(), name='Subjects_Details')
]