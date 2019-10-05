from django.conf.urls import include
from django.urls import path
from appOne import views

app_name = 'appOne'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('add_module/', views.add_module, name = 'add_module'),
    path('modules/<str:pk>/addchapter/', views.add_chapter, name = 'add_chapter'),
    path('manage_module/', views.manage_module, name = 'manage_module'),
    path('modules/<str:pk>/manage_chapter/',views.manage_chapter, name = 'manage_chapter'),
    path('prof/',views.prof_page, name = 'prof_page'),
    path('student/',views.student_page, name = 'student_page'),
]
