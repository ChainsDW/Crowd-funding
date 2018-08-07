from django.contrib import admin
from django.conf.urls import url, include
from Audit import views


urlpatterns = [
    url(r'^login.html$', views.login),
    url(r'^listProject.html$', views.project),
    url(r'^project.html$',views.project_profile),
    url(r'^download.html$', views.download)
]
