from django.urls import path
from User import views
from django.contrib.auth import views as auth_views
app_name = 'Group' 
urlpatterns = [
   
    
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    
    

]
