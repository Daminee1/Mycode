from django.urls import path,include
from .import views


urlpatterns = [
   path('standard', views.Standard_Details.as_view(), name='Standard_Details')
]