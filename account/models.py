from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class status(models.Model):
  status = models.CharField(max_length=30)
  MSG = models.CharField(max_length=30, blank=True)

  def __unicode__(self):
    return self.status + " : " + str(self.MSG)

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  hash = models.CharField(max_length=100, blank=True, null=True)
  pwdhash = models.CharField(max_length=100, blank=True, null=True)

  def __unicode__(self):
    return self.user.username
