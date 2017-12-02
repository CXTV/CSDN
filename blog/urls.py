"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from csdn import views

from django.views.static import serve  # 引入配置media的路径
from django.conf import settings  # 引入settings
from app01 import views as app01_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r'^regist/', views.regist),
    url(r'^logout/', views.logout),
    url(r'^demo/', views.demo),

    #滑动验证码
    url(r'^pc-geetest/register', app01_views.pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/validate$', app01_views.pcvalidate, name='pcvalidate'),
    url(r'^pc-geetest/ajax_validate', app01_views.pcajax_validate, name='pcajax_validate'),

    # 个人站点首页
    url(r'^blog/', include('csdn.urls')),
    # media 配置,专门放用户上传的文件
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
