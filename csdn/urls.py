import re
from django.conf.urls import url, include
from csdn import views
from django.conf import settings  # 引入settings

urlpatterns = [

    url(r'^(?P<username>.*)/(?P<condition>tag|date|category)/(?P<para>.*)', views.homeSite, name="aaa"),
    url(r'^(?P<username>.*)', views.homeSite, name="aaa"),

]
