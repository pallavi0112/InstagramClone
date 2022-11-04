from django.contrib import admin
from .models import *
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user' , 'profile_picture']
    filter_horizontal=["following"]
admin.site.register(Profile, ProfileAdmin)

class POSTAdmin(admin.ModelAdmin):
    list_display = ['user' , 'Image', 'profile']
admin.site.register( POST, POSTAdmin )

class ReelsAdmin(admin.ModelAdmin):
    list_display = ['reels', 'profile']
admin.site.register(Reels , ReelsAdmin)

class StoryAdmin(admin.ModelAdmin):
    list_display = ['story' , 'story2', 'profile']
admin.site.register(Story , StoryAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender', 'reciepient','date', 'is_read']
admin.site.register(Message, MessageAdmin)