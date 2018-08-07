from django import forms
from jiuchai import models
import re


class SendMsgForm(forms.Form):
    email = forms.EmailField(error_messages={"invalid": "邮箱格式有误"})


class RegisterForm(forms.ModelForm):

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        exclude = ['name']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', phone):
            return phone
        else:
            raise forms.ValidationError("手机号码非法", code='mobile invalid')

    def clean_id_code(self):
        id_code = self.cleaned_data.get('id_code')
        if re.match(r'^[\d]{17}[0-9a-zA-Z]$', id_code):
            print(id_code)
            return id_code
        else:
            raise forms.ValidationError("身份证非法", code='id invalid')


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'invalid': '格式错误'})
    pwd = forms.CharField()
    # code = forms.CharField()


if __name__ == '__main__':
    id = '3201251992092823rf'
    print(re.match(r'^[\d]{17}[0-9a-zA-Z]$', id))