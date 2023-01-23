from django.urls import path,include
from .import views


urlpatterns = [
   path('user', views.User_Details.as_view(), name='User_Details'),
   path('', views.home),
   path('user_data', views.User_Details_Get.as_view(),name='User_Details_Get')

   # path('', views.home, name='home'),
   # path('save/', views.save_data, name='save'),
   # path('delete/', views.delete_data, name='delete'),
   # path('edit/', views.edit_data, name='edit'),
   # path('crud/', views.CrudView.as_view()),
   # path('add_subjects', views.add_subjects)

]