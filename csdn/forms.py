from django import forms
from django.forms import widgets,ValidationError

from csdn import models


class RegForm(forms.Form):
    username=forms.CharField(max_length=12,min_length=5,required=True,error_messages={
        "required":"不能为空",
    },widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"username"}))

    password=forms.CharField(min_length=6,widget=widgets.PasswordInput(
        attrs={"class": "form-control", "placeholder": "password"}
    ))

    repeat_pwd=forms.CharField(min_length=6,widget=widgets.PasswordInput(
        attrs={"class": "form-control", "placeholder": "repeat_pwd"}
    ))

    email=forms.EmailField(widget=widgets.EmailInput(
        attrs={"class": "form-control", "placeholder": "email"}
    ))

    def clean_username(self):
        '''
        校验username字段
        '''

        ret = models.UserInfo.objects.filter(username=self.cleaned_data.get("username")) #在models进行验证
        if not ret:
            return self.cleaned_data.get("username")
        else:
            raise ValidationError("用户名已注册")

    def clean_password(self):
        '''
        校验password字段,怎么使用正则
        '''

        data=self.cleaned_data.get("password")

        if not data.isdigit():
            return self.cleaned_data.get("password")
        else:
            raise ValidationError("密码不能全是数字")

    def clean(self):
        '''
            全局钩子，判断两次密码是否一致
        '''
        if self.cleaned_data.get("password") == self.cleaned_data.get("repeat_pwd"):
            return self.cleaned_data

        else:
            raise  ValidationError("两次密码不一致")