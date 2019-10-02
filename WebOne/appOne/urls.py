from django.conf.urls import include
from django.urls import path
from appOne import views

app_name = 'appOne'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('addmodule/', views.add_module, name = 'add_module'),
]
