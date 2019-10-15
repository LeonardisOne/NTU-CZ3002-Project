from django.conf.urls import include
from django.urls import path
from appOne import views

app_name = 'appOne'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('add_module/', views.add_module, name='add_module'),
    path('<str:pk>/addchapter/', views.add_chapter, name='add_chapter'),
    path('manage_module/', views.manage_module, name='manage_module'),
    path('<str:pk>/',views.manage_chapter, name='module_home'),
    path('<str:pk>/manage_chapter/',views.manage_chapter, name='manage_chapter'),
    path('<str:pk>/<str:pq>/',views.manage_question, name='chapter_home'),
    path('<str:pk>/<str:pq>/manage_question/',views.manage_question, name='manage_question'),
    path('<str:pk>/<str:pq>/add_question/',views.add_question,name='add_question'),
    path('prof/',views.prof_page, name = 'prof_page'),
    path('student/',views.student_page, name = 'student_page'),
    path('<str:pk>/<str:pq>/chat/', views.chat, name = 'chat'),
    path('delete_chapter/<module_pk>/<chapter_name>', views.delete_chapter, name="delete_chapter"),
    path('delete_question/<module_pk>/<chapter_name>/<question_name>',views.delete_question, name="delete_question"),
    path('delete_module/<module_pk>/',views.delete_module, name='delete_module'),
    path('<str:pk>/<str:pq>/publish/', views.publish_chapter, name='publish_chapter'),
    path('<m_name>/<ch_name>/start_quiz/',views.start_question, name='start_question'),
    path('<m_name>/<ch_name>/<int:q_num>/',views.view_question, name='view_question'),
    path('<m_name>/<ch_name>/view_result/', views.view_chapter_result, name='view_result'),
]
