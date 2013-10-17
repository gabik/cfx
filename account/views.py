from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from account.forms import UserForm #, UserProfileForm, AgreeForm, ProvProfileForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import simplejson as json
from account.models import status , UserProfile
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
import hashlib
from twilio.rest import TwilioRestClient

def is_login(request):
  if request.user.is_authenticated():
    json_data = status.objects.filter(status='OK')
  else:
    json_data = status.objects.filter(status='ERR', MSG='LGN')
  json_dump = serializers.serialize("json", json_data)
  return HttpResponse(json_dump)

def Plogin (request):
  json_data=list(status.objects.filter(status='ERR',MSG='PD'))
  if request.method == 'POST':
    json_data=list(status.objects.filter(status='WRN',MSG='NE'))
    new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if new_user :
      json_data = status.objects.filter(status='OK')
      if new_user.is_active:
        login(request, new_user)
      else:
        json_data=list(status.objects.filter(status='WRN',MSG='AC'))
  json_dump = serializers.serialize("json", json_data)
  return HttpResponse(json_dump)


def PNewUser(request):
  json_data=status.objects.filter(status='ERR',MSG='PD')
  errors=""
  if request.method == 'POST':
    #userprofile_form = UserProfileForm(request.POST)
    user_form = UserForm(request.POST)
    #if userprofile_form.is_valid() and user_form.is_valid():
    if user_form.is_valid():
      user_clean_data = user_form.cleaned_data
      created_user = User.objects.create_user(user_clean_data['username'], user_clean_data['email'], user_clean_data['password1'])
      created_user.first_name=request.POST['firstname']
      created_user.last_name=request.POST['lastname']
      #created_user.is_active = False
      created_user.save()
      pinHash = str(hash("CLT"+ created_user.username + created_user.email))[3:9]
      userprofile = UserProfile(user=created_user, hash=pinHash, pwdhash=0) #hash=hashlib.sha224("CLT" + created_user.username + created_user.email).hexdigest())
      #userprofile.user = created_user
      #userprofile.phone_num1 = userprofile_form.cleaned_data['phone_num1']
      #userprofile.hash = hashlib.sha224("CLT" + created_user.username + created_user.email).hexdigest()
      userprofile.save()
      textmessage="Hi " + request.POST['firstname'] + " and welcome to Cofix. This is your PIN code for activating your account: " + pinHash
      account_sid = "AC442a538b44777e2897d4edff57437a24"
      auth_token  = "be3a4e5fbf058c5b27a2904efd05d726"
      client = TwilioRestClient(account_sid, auth_token)
      message = client.sms.messages.create(body=textmessage,to="+"+created_user.username,from_="+16698005705")
      #new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
      #login(request, new_user)
      json_data = status.objects.filter(status='OK')
    else:
      json_data = status.objects.filter(status='WRN')
      if user_form.errors.items() :
        errors = ",[" + str(dict([(k, v[0].__str__()) for k, v in user_form.errors.items()])) + "]"
      #if userprofile_form.errors.items():
      # errors += ",[" + str(dict([(k, v[0].__str__()) for k, v in userprofile_form.errors.items()])) + "]"
  json_dump = "[" + serializers.serialize("json", json_data)
  json_dump += errors + "]"
  return HttpResponse(json_dump.replace('\'','"'))


