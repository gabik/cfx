from django import forms
import re
from django.forms import ModelForm
from account.models import UserProfile, User

class UserForm(forms.Form):
  username = forms.CharField(max_length=100, label = 'Username')
  email = forms.EmailField(label = 'E-Mail', required=True)
  password1 = forms.CharField(max_length=20, widget = forms.PasswordInput, label = 'Password')
  password2 = forms.CharField(max_length=20, widget = forms.PasswordInput, label = 'Confirm Password')

  def clean_password1(self):
    password1 = self.cleaned_data['password1']
    if len(password1) < 5:
      raise forms.ValidationError('Minimus 5 chars')
    return password1

  def clean_password2(self):
    password2 = self.cleaned_data['password2']
    try:
      password1 = self.cleaned_data['password1']
    except KeyError:
      return password2
    if password1 != password2:
      raise forms.ValidationError('Password not match')
    return password2

  def clean_email(self):
    try:
      User.objects.get(email=self.cleaned_data['email'])
      raise forms.ValidationError('Email address already already')
    except User.DoesNotExist:
      return self.cleaned_data['email']

  def clean_username(self):
    username = self.cleaned_data['username']
    r = re.compile('^\d{10,20}$')
    if not r.match(username):
      raise forms.ValidationError('Illigle phone number')
    try:
      User.objects.get(username=self.cleaned_data['username'])
      raise forms.ValidationError('Number already already')
    except User.DoesNotExist:
      return self.cleaned_data['username']

