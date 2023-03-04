

import re
from django import forms
from django.forms import ModelForm
from .models import *
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])

class CreateBookForm(ModelForm):
    class Meta:
        model = Book 
        fields = '__all__'

class CommentForm(forms.ModelForm):
    content = forms.CharField(label = "", widget=forms.Textarea(attrs={'class': 'form-control' , 'id' : 'exampleFormControlTextarea1', 'row' : '3'}), required=False)
    star = forms.ChoiceField(label = "",choices=STAR_CHOICES, widget=forms.Select(),required=True)
    
    def __init__(self, *args, **kwargs):
        self.assessor = kwargs.pop('assessor', None)
        self.book = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.assessor = self.assessor
        comment.book = self.book
        comment.save()

    class Meta:
        model = Comment
        fields = ('content', 'star')