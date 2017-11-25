import re
from django.conf.urls import url, include
from csdn import views
from django.conf import settings  # 引入settings

urlpatterns = [

    url(r'^(?P<username>.*)', views.homeSite, name="aaa"),

]
