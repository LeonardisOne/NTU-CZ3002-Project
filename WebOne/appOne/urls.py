from django.conf.urls import include
from django.urls import path
from appOne import views

app_name = 'appOne'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('add_module/', views.add_module, name='add_module'),
    path('modules/<str:pk>/addchapter/', views.add_chapter, name='add_chapter'),
    path('manage_module/', views.manage_module, name='manage_module'),
    path('modules/<str:pk>/manage_chapter/',views.manage_chapter, name='manage_chapter'),
    path('modules/<str:pk>/chapters/<str:pq>/manage_question/',views.manage_question, name='manage_question'),
    path('modules/<str:pk>/chapters/<str:pq>/add_question/',views.add_question,name='add_question'),
    path('prof/',views.prof_page, name = 'prof_page'),
    path('student/',views.student_page, name = 'student_page'),
    path('chat/', views.chat, name = 'chat'),
    path('modules/delete_chapter/<module_pk>/<chapter_name>', views.delete_chapter, name="delete_chapter"),
    path('modules/delete_question/<module_pk>/<chapter_name>/<question_name>',views.delete_question, name="delete_question"),
    path('modules/delete_module/<module_pk>/',views.delete_module, name='delete_module'),
    path('modules/<str:pk>/chapters/<str:pq>/publish/', views.publish_chapter, name='publish_chapter'),
]
