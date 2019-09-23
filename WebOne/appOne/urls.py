from django.conf.urls import url
from appOne import views

urlpatterns = [
    url(r'^$', views.login_view, name="login"),
]
