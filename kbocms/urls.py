"""kbocms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.urls import re_path as url ####open when you upload to server
#from django.conf.urls import url
#from django.conf import settings ####open when you upload to server
#from django.views.static import serve  ####open when you upload to server

from django.conf import settings

from django.contrib import admin
from django.urls import path,include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views #as auth_views is nicknanme

urlpatterns = [
    #url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),   ####open when you upload to server
    #url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), ####open when you upload to server

    path('kbo-admin-site/', admin.site.urls),
    path('captcha',include('captcha.urls')),
   
    path('',include('cmsapp.urls')),
    path('',include('cmsapp_backend.urls')),
    path('',include('server_mainten.urls')),
    path('',include('vdoconf_conclusion.urls')),
    path('login/', auth_views.LoginView.as_view(template_name ='cmsapp_backend/pages-login.html' ) ,name = 'login'),
    path('login/', auth_views.LogoutView.as_view() ,name = 'login'),

]
#url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
#url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
