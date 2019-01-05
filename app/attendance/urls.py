from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
]