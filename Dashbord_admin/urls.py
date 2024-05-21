from django.urls import path
from . import views

app_name = 'Dashbord_admin'

urlpatterns = [
    path('', views.dashbord, name='dashbord'),
    
    
     
]


