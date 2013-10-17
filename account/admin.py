from django.contrib import admin
from account.models import UserProfile, status

#class areaAdmin(admin.ModelAdmin):
        #list_display = ['id', 'parent', 'name']

admin.site.register(UserProfile)
admin.site.register(status)

